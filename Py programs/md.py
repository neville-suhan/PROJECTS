import os


directory_path="/hp"


contents=os.listdir(directory_path)

for item in contents:
    print(item)