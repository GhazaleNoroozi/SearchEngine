import re

REPLACE_MAP = {'[\u200c:;?!,؟،.؛\'"\[\](){}<>«»/\\-&$@#*\n]': ' ',
               # '[۰٠]': '0', '[۱١]': '1', '[۲٢]': '2', '[۳٣]': '3', '[۴٤]': '4',
               # '[۵٥]': '5', '[۶٦]': '6', '[۷٧]': '7', '[۸٨]': '8', '[۹٩]': '9',
               '[۰٠0۱١1۲٢2۳٣3۴٤4۵٥5۶٦6۷٧7۸٨8۹٩9]| می ': ' ',
               ' صد | یکصد | دویست | سیصد | چهارصد | پانصد | ششصد | هفتصد | هشتصد | نهصد | هزار | میلیون | میلیارد '
               ' ده | بیست | سی | چهل | پنجاه | شصت | هفتاد | هشتاد | نود '
               ' یک | دو | سه | چهار | پنج | شش | هفت | هشت | نه ': ' ',
               #' صد | دویست | سیصد | چهارصد | پانصد | ششصد | هفتصد | هشتصد | نهصد | هزار | میلیون | میلیارد ' + و قبلش
               #' ده | بیست | سی | چهل | پنجاه | شصت | هفتاد | هشتاد | نود ' + و قبلش
               #' یک | دو | سه | چهار | پنج | شش | هفت | هشت | نه ' + و قبلش
               # هفتادو | هشتادو | نودو | صدو | هزارو | میلیاردو | دومیلیارد | دومیلیون | دوهزار | چهارمیلیارد | چهارمیلیون | چهارهزار
               '[ي]': 'ی', '[ك]': 'ک', '[آ]': 'ا', '[\s]+': ' '}

STOP_INDEX = 10


class IIM:
    def __init__(self, texts):
        self.texts = texts
        self.t_texts = []
        self.dict = {}
        self.preprocess()
        self.tokenize()
        self.stop_words()

    def preprocess(self):
        for i in range(0, len(self.texts)):
            for replacement in REPLACE_MAP:
                self.texts[i] = re.sub(replacement, REPLACE_MAP[replacement], self.texts[i])
        self.normalize()

    def tokenize(self):
        vocab = []
        for text in self.texts:
            t = text.split()
            self.t_texts.append(t)
            vocab.extend(t)

        vocab = sorted(set(vocab))

        for word in vocab:
            self.dict[word] = []

        for i in range(0, len(self.t_texts)):
            t_text = self.t_texts[i]
            for j in range(0, len(t_text)):
                word = t_text[j]
                self.dict[word].append((i, j))

    def stop_words(self):
        frequencies = []
        for word in self.dict:
            count = len(self.dict[word])
            frequencies.append((word, count))

        frequencies = sorted(frequencies, key=lambda tup: tup[1])
        # print(frequencies)
        stop_words = frequencies[-1 * STOP_INDEX:]
        # print(stop_words)

        for stop_word in stop_words:
            del self.dict[stop_word[0]]
        # print(self.dict)

    def stemming(self):
        #TODO
        pass

    def remove_plural_signs(self):
        #TODO
        pass

    def remove_suffixes(self):
        #TODO
        pass

    def normalize(self):
        #TODO idea
        self.stemming()
        self.remove_plural_signs()
        self.remove_suffixes()
        pass
