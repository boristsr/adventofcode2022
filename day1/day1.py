
inputfile = open('day1/input', 'r')
Lines = inputfile.readlines()

current_index = 0
current_calorie_count = 0

max_index = 0
max_calorie_count = 0

for line in Lines:
    if line.strip() == "":
        if current_calorie_count > max_calorie_count:
            max_calorie_count = current_calorie_count
            max_index = current_index
        
        current_index += 1
        current_calorie_count = 0
        continue
    
    current_calories = int(line.strip())
    current_calorie_count += current_calories

print(f'Max Index: {max_index} with calorie count of {max_calorie_count}')