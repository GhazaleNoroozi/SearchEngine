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

    query = '^_^'
    while query != '':
        query = input()
        docs = iim.answer(query)
        for i in range(0, len(docs)):
            category = docs[len(docs) - i - 1]
            for j in range(0, len(category)):
                doc = category[len(category) - j - 1]
                print(doc)


if __name__ == "__main__":
    main()
