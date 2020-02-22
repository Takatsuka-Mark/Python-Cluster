import os

path = "../Logs/"


def main():
    file_list = []
    for root, directories, files in os.walk(path):
        file_list.extend(files)

    print("Welcome to the LogDecoder!")

    print_bars()
    i = 0
    for file in file_list:
        print(str(i) + ":\t" + file)
        i += 1
    print_bars()
    print()

    file = None
    while file is None:
        file = int(input("Enter the number of a file to interpret (default 0):\t"))
        if 0 <= file < len(file_list):
            file = file_list[file]
        else:
            file = None

    save = input("Would you like to save the output to a file? (default No) Y/N:\t").upper() == "Y"
    print()

    # TODO implement saving to a file

    file_reader = open(path + file)
    for line in file_reader:
        if "[" in line:
            # strip the line just to the results
            line = line[line.find("[") + 1: line.find("]")]
            print(line)

    print()
    # print("File selected: ", file)

    return None


def print_bars():
    for i in range(0, 80):
        print("=", end='')
    print("")


if __name__ == '__main__':
    main()
