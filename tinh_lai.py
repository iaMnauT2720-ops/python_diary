#compound interest caculator of an amount of money

principle = 0
rate = 0
time = 0

while principle <=0:
    principle = float(input("Enter your principal amount(VNĐ): "))
    if principle <=0:
        print("Principle cannot be less than zero")

while rate <=0:
    rate = float(input("Enter interest rate: "))
    if rate <=0:
        print("Interest cannot be less than zero")

while time <=0:
    time = float(input("Enter time(year): "))
    if principle <=0:
        print("Time cannot be less than zero")

total = principle * pow((1 + rate/100),time)
print(f"Your total balance is {total:,.0f} VNĐ")

