from datetime import datetime, date
import locale

now = datetime.now()
print(now)

try:
    locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, 'korean')

formatted_now = now.strftime("%Y년 %m월 %d일 %A %H시 %M분 %S초")
print(formatted_now)

formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_now)

today = date.today()
print("현재 날짜:", today)



