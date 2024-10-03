import datetime
import calendar

year = str(datetime.date.today())[0:4]

print("2024-06-01")

formatedDay = ""
for day in range(1, calendar.monthrange(int(year), 6)[1] + 1):
    if (len(str(day)) < 2): formatedDay = "0" + str(day)
    else: formatedDay = str(day)
    
    print(year + "-" + "06-" + formatedDay + "\n")