import sys

def hello(name):
    print(f"Hello {name}!")

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "hello":
        print("Usage: python my_cli.py hello --name <YourName>")
    else:
        try:
            name_index = sys.argv.index("--name") + 1
            name = sys.argv[name_index]
            hello(name)
        except (ValueError, IndexError):
            print("Error: Please provide a name after --name")
