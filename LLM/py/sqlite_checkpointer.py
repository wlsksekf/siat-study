import random
import sqlite3
from pathlib import Path
from typing import Any, Iterator, Sequence

from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    ChannelVersions,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
    get_checkpoint_id,
    get_checkpoint_metadata,
)
from langgraph.checkpoint.memory import WRITES_IDX_MAP
from langchain_core.runnables import RunnableConfig


LLM_DIR = Path(__file__).resolve().parent.parent
DB_DIR = LLM_DIR / "db"
DB_PATH = DB_DIR / "chat_memory.db"


class SqliteCheckpointSaver(BaseCheckpointSaver[str]):
    def __init__(self) -> None:
        super().__init__()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT NOT NULL,
                    checkpoint_ns TEXT NOT NULL,
                    checkpoint_id TEXT NOT NULL,
                    checkpoint_type TEXT NOT NULL,
                    checkpoint_blob BLOB NOT NULL,
                    metadata_type TEXT NOT NULL,
                    metadata_blob BLOB NOT NULL,
                    parent_checkpoint_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoint_blobs (
                    thread_id TEXT NOT NULL,
                    checkpoint_ns TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    version TEXT NOT NULL,
                    value_type TEXT NOT NULL,
                    value_blob BLOB NOT NULL,
                    PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoint_writes (
                    thread_id TEXT NOT NULL,
                    checkpoint_ns TEXT NOT NULL,
                    checkpoint_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    idx INTEGER NOT NULL,
                    channel TEXT NOT NULL,
                    value_type TEXT NOT NULL,
                    value_blob BLOB NOT NULL,
                    task_path TEXT NOT NULL DEFAULT '',
                    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
                )
                """
            )

    @staticmethod
    def _version_key(version: Any) -> str:
        return str(version)

    def _load_blobs(
        self, thread_id: str, checkpoint_ns: str, versions: ChannelVersions
    ) -> dict[str, Any]:
        if not versions:
            return {}

        keys = [(channel, self._version_key(version)) for channel, version in versions.items()]
        placeholders = ",".join(["(?, ?)"] * len(keys))
        params: list[Any] = [thread_id, checkpoint_ns]
        for channel, version_key in keys:
            params.extend([channel, version_key])

        query = (
            """
            SELECT channel, version, value_type, value_blob
            FROM checkpoint_blobs
            WHERE thread_id = ? AND checkpoint_ns = ?
              AND (channel, version) IN (
            """
            + placeholders
            + ")"
        )

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        blob_map = {
            (row["channel"], row["version"]): self.serde.loads_typed(
                (row["value_type"], row["value_blob"])
            )
            for row in rows
            if row["value_type"] != "empty"
        }
        return {
            channel: blob_map[(channel, self._version_key(version))]
            for channel, version in versions.items()
            if (channel, self._version_key(version)) in blob_map
        }

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = get_checkpoint_id(config)

        with self._connect() as conn:
            if checkpoint_id:
                row = conn.execute(
                    """
                    SELECT checkpoint_id, checkpoint_type, checkpoint_blob,
                           metadata_type, metadata_blob, parent_checkpoint_id
                    FROM checkpoints
                    WHERE thread_id = ? AND checkpoint_ns = ? AND checkpoint_id = ?
                    """,
                    (thread_id, checkpoint_ns, checkpoint_id),
                ).fetchone()
            else:
                row = conn.execute(
                    """
                    SELECT checkpoint_id, checkpoint_type, checkpoint_blob,
                           metadata_type, metadata_blob, parent_checkpoint_id
                    FROM checkpoints
                    WHERE thread_id = ? AND checkpoint_ns = ?
                    ORDER BY checkpoint_id DESC
                    LIMIT 1
                    """,
                    (thread_id, checkpoint_ns),
                ).fetchone()

            if row is None:
                return None

            checkpoint = self.serde.loads_typed(
                (row["checkpoint_type"], row["checkpoint_blob"])
            )
            metadata = self.serde.loads_typed((row["metadata_type"], row["metadata_blob"]))
            write_rows = conn.execute(
                """
                SELECT task_id, idx, channel, value_type, value_blob
                FROM checkpoint_writes
                WHERE thread_id = ? AND checkpoint_ns = ? AND checkpoint_id = ?
                ORDER BY task_id, idx
                """,
                (thread_id, checkpoint_ns, row["checkpoint_id"]),
            ).fetchall()

        pending_writes = [
            (
                write_row["task_id"],
                write_row["channel"],
                self.serde.loads_typed((write_row["value_type"], write_row["value_blob"])),
            )
            for write_row in write_rows
        ]

        hydrated_checkpoint = {
            **checkpoint,
            "channel_values": self._load_blobs(
                thread_id, checkpoint_ns, checkpoint["channel_versions"]
            ),
        }

        parent_config = None
        if row["parent_checkpoint_id"]:
            parent_config = {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": checkpoint_ns,
                    "checkpoint_id": row["parent_checkpoint_id"],
                }
            }

        return CheckpointTuple(
            config={
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": checkpoint_ns,
                    "checkpoint_id": row["checkpoint_id"],
                }
            },
            checkpoint=hydrated_checkpoint,
            metadata=metadata,
            parent_config=parent_config,
            pending_writes=pending_writes,
        )

    def list(
        self,
        config: RunnableConfig | None,
        *,
        filter: dict[str, Any] | None = None,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ) -> Iterator[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"] if config else None
        checkpoint_ns = config["configurable"].get("checkpoint_ns") if config else None
        before_checkpoint_id = get_checkpoint_id(before) if before else None

        query = """
            SELECT thread_id, checkpoint_ns, checkpoint_id
            FROM checkpoints
            WHERE 1=1
        """
        params: list[Any] = []

        if thread_id is not None:
            query += " AND thread_id = ?"
            params.append(thread_id)
        if checkpoint_ns is not None:
            query += " AND checkpoint_ns = ?"
            params.append(checkpoint_ns)
        if before_checkpoint_id is not None:
            query += " AND checkpoint_id < ?"
            params.append(before_checkpoint_id)

        query += " ORDER BY checkpoint_id DESC"
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        for row in rows:
            checkpoint_tuple = self.get_tuple(
                {
                    "configurable": {
                        "thread_id": row["thread_id"],
                        "checkpoint_ns": row["checkpoint_ns"],
                        "checkpoint_id": row["checkpoint_id"],
                    }
                }
            )
            if checkpoint_tuple is None:
                continue
            if filter and not all(
                checkpoint_tuple.metadata.get(key) == value for key, value in filter.items()
            ):
                continue
            yield checkpoint_tuple

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = checkpoint["id"]
        parent_checkpoint_id = config["configurable"].get("checkpoint_id")

        checkpoint_copy = checkpoint.copy()
        channel_values = checkpoint_copy.pop("channel_values", {})
        checkpoint_type, checkpoint_blob = self.serde.dumps_typed(checkpoint_copy)
        metadata_type, metadata_blob = self.serde.dumps_typed(
            get_checkpoint_metadata(config, metadata)
        )

        with self._connect() as conn:
            for channel, version in new_versions.items():
                value_type, value_blob = (
                    self.serde.dumps_typed(channel_values[channel])
                    if channel in channel_values
                    else ("empty", b"")
                )
                conn.execute(
                    """
                    INSERT OR REPLACE INTO checkpoint_blobs (
                        thread_id, checkpoint_ns, channel, version, value_type, value_blob
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        thread_id,
                        checkpoint_ns,
                        channel,
                        self._version_key(version),
                        value_type,
                        value_blob,
                    ),
                )

            conn.execute(
                """
                INSERT OR REPLACE INTO checkpoints (
                    thread_id, checkpoint_ns, checkpoint_id,
                    checkpoint_type, checkpoint_blob,
                    metadata_type, metadata_blob, parent_checkpoint_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    thread_id,
                    checkpoint_ns,
                    checkpoint_id,
                    checkpoint_type,
                    checkpoint_blob,
                    metadata_type,
                    metadata_blob,
                    parent_checkpoint_id,
                ),
            )

        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint_id,
            }
        }

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"]["checkpoint_id"]

        with self._connect() as conn:
            for idx, (channel, value) in enumerate(writes):
                write_idx = WRITES_IDX_MAP.get(channel, idx)
                if write_idx < 0:
                    existing = conn.execute(
                        """
                        SELECT 1
                        FROM checkpoint_writes
                        WHERE thread_id = ? AND checkpoint_ns = ? AND checkpoint_id = ?
                          AND task_id = ? AND idx = ?
                        """,
                        (thread_id, checkpoint_ns, checkpoint_id, task_id, write_idx),
                    ).fetchone()
                    if existing is not None:
                        continue

                value_type, value_blob = self.serde.dumps_typed(value)
                conn.execute(
                    """
                    INSERT OR REPLACE INTO checkpoint_writes (
                        thread_id, checkpoint_ns, checkpoint_id,
                        task_id, idx, channel, value_type, value_blob, task_path
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        thread_id,
                        checkpoint_ns,
                        checkpoint_id,
                        task_id,
                        write_idx,
                        channel,
                        value_type,
                        value_blob,
                        task_path,
                    ),
                )

    def delete_thread(self, thread_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
            conn.execute("DELETE FROM checkpoint_blobs WHERE thread_id = ?", (thread_id,))
            conn.execute("DELETE FROM checkpoint_writes WHERE thread_id = ?", (thread_id,))

    async def aget_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        return self.get_tuple(config)

    async def alist(
        self,
        config: RunnableConfig | None,
        *,
        filter: dict[str, Any] | None = None,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ):
        for item in self.list(config, filter=filter, before=before, limit=limit):
            yield item

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        return self.put(config, checkpoint, metadata, new_versions)

    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        self.put_writes(config, writes, task_id, task_path)

    async def adelete_thread(self, thread_id: str) -> None:
        self.delete_thread(thread_id)

    def get_next_version(self, current: str | None, channel: None) -> str:
        if current is None:
            current_v = 0
        elif isinstance(current, int):
            current_v = current
        else:
            current_v = int(str(current).split(".")[0])
        return f"{current_v + 1:032}.{random.random():016}"
