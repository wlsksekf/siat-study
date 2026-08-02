val = 1234567.89
print(f"{val:,.0f}")

amount = 9876543.21

print(f"금액: ₩{amount:>20,.0f}")
print(f"금액: {amount:>20,.2f}")
print(f"금액: {amount:*>20,.2f}")

print(f"금액: ₩{amount:<20,.0f}")
print(f"금액: {amount:<20,.2f}")
print(f"금액: {amount:*<20,.2f}")