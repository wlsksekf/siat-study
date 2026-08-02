from dotenv import load_dotenv
from openai import OpenAI
import truststore

truststore.inject_into_ssl()

load_dotenv()

# OpenAI API 서버와 통신할 클라이언트 객체 생성합니다.
client = OpenAI()

# 업로드된 파일 확인합니다.
files = client.files.list()

for f in files:
    print(f.id, f.filename)

# file-C32xvQfZHaLwmKraBgWEBF page_high_res.png
# file-57SEa5ZqUQLUx5awHXUCws crop-model.pdf

# 위와 같이 출력되면 공백 앞의 문자열을 복사해서 인자로 사용합니다.
client.files.delete("file-57SEa5ZqUQLUx5awHXUCws")

print("삭제 후")

for f in files:
    print(f.id, f.filename)