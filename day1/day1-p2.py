
inputfile = open('day1/input', 'r')
Lines = inputfile.readlines()

current_index = 0
current_calorie_count = 0

top_elves = {}

def add_elf(new_index, new_calories, max_elves = 3):
    if len(top_elves) >= max_elves:
        min_elf_index = -1
        min_elf_count = -1
        for index in top_elves:
            if min_elf_index is -1:
                min_elf_index = index
                min_elf_count = top_elves[index]
            else:
                if top_elves[index] < min_elf_count:
                    min_elf_index = index
                    min_elf_count = top_elves[index]
    
        if new_calories > top_elves[min_elf_index]:
            del top_elves[min_elf_index]
            top_elves[new_index] = new_calories
    else:
        top_elves[new_index] = new_calories

for line in Lines:
    if line.strip() is "":
        add_elf(current_index, current_calorie_count)
        
        current_index += 1
        current_calorie_count = 0
        continue
    
    #print(line.strip())
    current_calories = int(line.strip())
    current_calorie_count += current_calories

top_3_count = 0
for index in top_elves:
    top_3_count += top_elves[index]

print(f'Top 3 elves were carrying {top_3_count} calories in total')
