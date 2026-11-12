import time

giay = int(input("Enter the time in seconds: "))

for i in range(giay, 0, -1):
    seconds = i % 60
    minutes = int(i / 60) % 60
    hours = int(i / 3600) % 24
    days = int(i / 86400)
    print(f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("HET GIO ROI DAY DI THANG NGU!!!")
