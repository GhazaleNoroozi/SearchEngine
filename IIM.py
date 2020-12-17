class IIM:
    def __init__(self, files):
        self.files = files
        self.tokenize()

    def stop_words(self):
        pass

    def unify(self):
        """TODO idea!"""
        pass

    def answer(self):
        pass

    def tokenize(self):
        texts = []
        vocab = []
        for file in self.files:
            text = file.read().split()
            vocab.extend(set(text))
            texts.append(text)
        vocab = sorted(set(vocab))

        dictionary = {}
        for word in vocab:
            dictionary[word] = []

        for i in range(0, len(texts)):
            text = texts[i]
            for j in range(0, len(text)):
                word = text[j]
                dictionary[word].append((i, j))

        for d in dictionary:
            print(d, dictionary[d])
