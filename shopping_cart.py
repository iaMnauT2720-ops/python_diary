foods = []
prices = []
total = 0

while True:
    food = input("Enter a food u want to buy (q to quit): ")
    if food.lower() == "q":
        break
    else:
        foods.append(food)
        price = float(input(f"Enter the price of a {food}(kVNĐ): "))
        prices.append(price)

print("---YOUR CART---")

print("You have bought: ", end="")
print(", ".join(foods))

for price in prices:
    total += price

print(f"Your total is: {total: .0f}" + ",000VNĐ")