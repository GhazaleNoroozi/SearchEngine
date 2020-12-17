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


def merge(doc_lists):
    print(doc_lists)
    count = len(doc_lists)
    # index_docs = []
    # for i in range(0, count):
    #     index_docs.append((0, doc_lists[i]))

    related_docs_lists = [[] for i in range(0, count)]
    indexes = [0 for i in range(0, count)]

    while True:

        # find the doc list with min doc_id and increment it's index
        min_index = 0
        minimum = 99999999
        for i in range(0, count):
            # print(f'in doclist index is: {indexes[i]}')
            current_doc = doc_lists[i][indexes[i]]
            if indexes[i] != -1 and current_doc < minimum:
                minimum = current_doc
                min_index = i

        # print(f'min_index:{min_index}')

        # add this doc_id at the min index in the aggregate somewhere
        current_doc = doc_lists[min_index][indexes[min_index]]
        similarity_count = 0
        for i in range(0, count):
            if i != min_index and doc_lists[i][indexes[i]] == doc_lists[min_index][indexes[min_index]]:
                similarity_count += 1
        # print(similarity_count, ' ', current_doc)
        related_docs_lists[similarity_count].append(current_doc)

        # move forward one index for the min doc_id
        for i in range(0, count):
            if i != min_index and doc_lists[i][indexes[i]] == doc_lists[min_index][indexes[min_index]]:
                if indexes[i] >= len(doc_lists[i]) - 1:
                    indexes[i] = -1
                else:
                    indexes[i] += 1

        if indexes[min_index] >= len(doc_lists[min_index]) - 1:
            indexes[min_index] = -1
        else:
            indexes[min_index] += 1

        # check if all reached the end
        should_continue = False
        for index in indexes:
            if index != -1:
                should_continue = True

        if not should_continue:
            break

    return related_docs_lists


class IIM:
    def __init__(self, texts):
        texts = self.preprocess(texts)
        t_texts, vocab = self.tokenize(texts)
        self.dict = self.make_dict(t_texts, vocab)
        self.s_words = self.remove_stop_words()

    def preprocess(self, texts):
        for i in range(0, len(texts)):
            for replacement in REPLACE_MAP:
                texts[i] = re.sub(replacement, REPLACE_MAP[replacement], texts[i])
        self.normalize()

        return texts

    def tokenize(self, texts):
        vocab = []
        t_texts = []
        for text in texts:
            t = text.split()
            t_texts.append(t)
            vocab.extend(t)

        vocab = sorted(set(vocab))

        return t_texts, vocab

    def make_dict(self, t_texts, vocab):
        dictionary = {}
        for word in vocab:
            dictionary[word] = []

        for i in range(0, len(t_texts)):
            t_text = t_texts[i]
            for j in range(0, len(t_text)):
                word = t_text[j]
                dictionary[word].append((i, j))

        return dictionary

    def remove_stop_words(self):
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

        return stop_words

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

    def answer(self, query):
        t_queries, vocab = self.tokenize(self.preprocess([query]))
        t_query = t_queries[0]
        # print(t_query)

        if len(t_query) == 1:
            if t_query[0] in self.dict:
                indexes = self.dict[t_query[0]]
                return set([index[0] for index in indexes])
            else:
                return []

        count = 0
        if len(t_query) > 1:
            index_list = []
            for q_word in t_query:
                if q_word in self.dict:
                    index_list.append(sorted(list(set([pos_doc[0] for pos_doc in self.dict[q_word]]))))
                    count += 1

            res = merge(index_list)
            print(res)
            return res
