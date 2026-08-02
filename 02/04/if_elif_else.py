time = "morning"

if time == "morning":
    print("좋은 아침")
elif time == "afternoon":
    print("좋은 점심")    
elif time == "evening":
    print("좋은 저녁")    
else:
    print("시간대가 인식 불가")

score = 95

if score < 70:
    print("F")
elif score >= 70 and score < 80:
    print("C")
elif score >= 80 and score < 90:
    print("B")
else:
    print("A")