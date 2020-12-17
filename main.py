import os
from IIM import IIM


def main():
    file_names = os.listdir('Documents')
    texts = []
    for file_name in file_names:
        file = open('Documents' + '/' + file_name, 'rt',  encoding="utf8")
        texts.append(file.read())
        file.close()

    iim = IIM(texts)

    # query = '^^'
    # while query != '':
    #     query = input()


if __name__ == "__main__":
    main()
