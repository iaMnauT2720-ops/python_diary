#Exercises: Level 1
#Day 2: 30 Days of python programming
first_name = "Tuan"
last_name = "Tran"
full_name = f"{first_name} {last_name}"
country = "VietNam"
city = "Nam Dinh"
age = 19
year = 2007
is_married = False
is_light_on = True
hobby = ["playing game","cooking","playing guitar"]

#Exercises: Level 2
print(type(full_name))
print(type(last_name))
print(type(full_name))
print(type(country))
print(type(city))
print(type(age))
print(type(year))
print(type(is_married))
print(type(is_light_on))
print(type(hobby))

len(first_name)
len(last_name)

num1 = 5
num2 = 4
total = num1 + num2
diff= num1 - num2
product = num1 * num2
divison = num1 / num2
remainder = num1 % num2
exp = num1 ** num2
floor_divison = num1 // num2

import math
radius = float(input("Enter the circle's radius: "))
area_of_circle = 2 * math.pi * pow(radius,2)
circum_of_circle = math.pi * radius * 2
if radius <= 0:
    print("Radius must not be negative or equal to 0!")
else:
    print("The area of the circle = ", area_of_circle)

