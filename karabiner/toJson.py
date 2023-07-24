import json

with open("karabiner/karabiner.jsonc") as file:
    while line := file.readline():
        if line.strip().startswith("//"):
            continue
        print(line, end="")
