import os
def clearPrint(string, end="\n"):
    os.system("clear")
    print(string, end=end)

def clearInput(prompt):
    os.system("clear")
    return input(prompt)