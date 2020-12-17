import os
from IIM import IIM


def main():
    file_names = os.listdir('Documents')
    files = []
    for file_name in file_names:
        file = open('Documents' + '/' + file_name, 'rt',  encoding="utf8")
        files.append(file)

    iim = IIM(files)

    for file in files:
        file.close()

    # query = '^^'
    # while query != '':
    #     query = input()


if __name__ == "__main__":
    main()
