class Content:
    def __init__(self, type, text):
        self.type = type        # 예: "output_text"
        self.text = text        # 실제 텍스트 내용

class OutputItem:
    def __init__(self, type, content):
        self.type = type        # 예: "message"
        self.content = content  # Content 객체 리스트

class MyResponse:
    def __init__(self, output_items: list[OutputItem]):
        self.output = output_items

    @property
    def output_text(self) -> str:
        """output 리스트 안에서 type이 'output_text'인 text를 모두 합쳐서 반환"""
        texts: list[str] = []
        for output in self.output:
            if output.type == "message":
                for content in output.content:
                    if content.type == "output_text":
                        texts.append(content.text)

        return "".join(texts)

# ---------------------------------------
# 실제 사용
# ---------------------------------------

# (1) Content 객체 생성
content1 = Content("output_text", "Hello, ")
content2 = Content("output_text", "world!")
content3 = Content("other_type", "무시될 내용")

# (2) OutputItem 객체 생성
message_item = OutputItem("message", [content1, content2, content3])
other_item = OutputItem("log", [])  # message가 아니므로 무시됨

# (3) MyResponse 객체 생성
response = MyResponse([message_item, other_item])

# (4) @property 접근 (메서드 호출이 아님)
print(response.output_text)