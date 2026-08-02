const btn = document.getElementById("btn");
const input = document.getElementById("search");
const tbody = document.getElementById("tbody");
const st = document.getElementById("status");

let users = [];

async function getData() {
  st.textContent = "상태: 로딩 중...";
  try {
    const res = await fetch(
      "https://raw.githubusercontent.com/hiksyksy1234/json/refs/heads/main/users.json",
    );
    if (!res.ok) throw new Error(res.status);

    users = await res.json();
    show(users);
    st.textContent = "상태: 완료";
  } catch (err) {
    st.textContent = "상태: 에러";
    tbody.innerHTML = `<tr><td colspan="4">${err.message}</td></tr>`;
  }
}

function show(list) {
  let html = "";
  list.forEach((user) => {
    html += `<tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.age}</td>
            <td>${user.city}</td>
        </tr>`;
  });
  tbody.innerHTML = html || `<tr><td colspan="4">결과 없음</td></tr>`;
}

function search() {
  const val = input.value.toLowerCase();
  const filtered = users.filter((user) =>
    user.name.toLowerCase().includes(val) ||
    user.age.toString().includes(val) ||
    user.city.toLowerCase().includes(val)
  );
  show(filtered);
}

btn.addEventListener("click", getData);
input.addEventListener("input", search);

getData();