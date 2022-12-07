from typing import List, Tuple, Optional
from os.path import join
import shlex

class Directory:
    def __init__(self, name: str = "", parent: Optional['Directory'] = None) -> None:
        self.parent: Optional['Directory'] = parent
        self.name: str = name
        self.dirs: List[Directory] = []
        self.files: List[Tuple[str, int]] = []
        self.size = -1
    
    def has_directory(self, name: str) -> bool:
        for dir in self.dirs:
            if dir.name == name:
                return True
        
        return False

    def get_directory(self, name: str) -> Optional['Directory']:
        for dir in self.dirs:
            if dir.name == name:
                return dir
        
        return None

    def calculate_size(self) -> int:
        if self.size != -1:
            return self.size

        self.size = 0
        for dir in self.dirs:
            self.size += dir.calculate_size()

        for file in self.files:
            self.size += file[1]
        
        return self.size


#inputfile = open('day7/test.txt', 'r')
inputfile = open('day7/input.txt', 'r')
Lines = inputfile.readlines()

cwd: List[str] = []
root_directory = Directory()

current_directory: Directory = root_directory

def pwd():
    dir_stack = []
    cd = current_directory
    while cd is not None:
        dir_stack.insert(0, cd.name)
        cd = cd.parent
    
    print(join("/", *dir_stack))


bListing = False
for line in Lines:
    line_values = shlex.split(line.strip())
    print(line_values)
    if line_values[0] == "$":
        bListing = False
        #command
        if line_values[1].lower() == "cd":
            #change directory
            if line_values[2] == "/":
                current_directory = root_directory
                pwd()
                continue
            if line_values[2] == "..":
                if current_directory.parent is None:
                    current_directory = root_directory
                else:
                    current_directory = current_directory.parent
                pwd()
                continue
            else:
                subdir = current_directory.get_directory(line_values[2])
                if subdir is not None:
                    current_directory = subdir
                    print(" Descending: " + line_values[2])
                else:
                    print("Warning: this directory doesn't exist, but it's being created, it probably should be discovered by LS first: " + line_values[2])
                    new_directory = Directory(line_values[2],current_directory)
                    current_directory.dirs.append(new_directory)
                    current_directory = new_directory
                pwd()
        if line_values[1].lower() == "ls":
            bListing = True
            pass
        
        #Do NOT fall through to next case, command finished processing
        continue

    if bListing:
        if line_values[0] == "dir":
            if current_directory.has_directory(line_values[1]):
                print("Warning: this directory already exists, despite ls wanting to create it again " + line_values[1])
                continue
            new_directory = Directory(line_values[1], current_directory)
            current_directory.dirs.append(new_directory)
        else:
            file_info = (line_values[1], int(line_values[0]))
            current_directory.files.append(file_info)
        
        continue

    print("ERROR: Unknown command")

root_size = root_directory.calculate_size()
print(root_size)

dirs_to_process: List[Directory] = [root_directory]

found_dirs: List[Directory] = []

while len(dirs_to_process) > 0:
    curr_dir = dirs_to_process.pop(0)
    dirs_to_process.extend(curr_dir.dirs)
    if curr_dir.calculate_size() < 100000:
        found_dirs.append(curr_dir)

total_size = 0

for dir in found_dirs:
    total_size += dir.calculate_size()

print(total_size)
