import xml.etree.ElementTree as ET
import os
import hazm

tokenizer = hazm.WordTokenizer()
lemmatizer = hazm.Lemmatizer()
bow = dict()

directories = []
for subdir, dirs, files in os.walk("/home/mehdi/PycharmProjects/InformationRetrieval/NormalizerResult/"):
    directories += dirs

for directory in directories:

    fileroot = '/home/mehdi/PycharmProjects/InformationRetrieval/NormalizerResult/' + directory + '/'
    print(fileroot)
    for subdir, dirs, files in os.walk(fileroot):
        for file in files:
            print(files.index(file), ' out of ', len(files))
            if 'dtd' in file:
                continue
            try:
                tree = ET.parse(fileroot + file)
            except ET.ParseError:
                continue

            root = tree.getroot()
            for document in root.findall('DOC'):
                TEXT = document.find("TEXT")
                sent = TEXT.text
                tokens = tokenizer.tokenize(sent)
                tokens = [lemmatizer.lemmatize(token) for token in tokens]
                temp_tokens = []
                for token in tokens:
                    if '#' in token:
                        token = token.split('#')[0]
                    try:
                        bow[token] += 1
                    except KeyError:
                        bow[token] = 0

                    temp_tokens.append(token)
                tokens = temp_tokens

                sent = ' '.join(tokens)
                TEXT.text = sent

                TITLE = document.find("TITLE")
                sent = TITLE.text
                tokens = tokenizer.tokenize(sent)
                tokens = [lemmatizer.lemmatize(token) for token in tokens]
                temp_tokens = []
                for token in tokens:
                    if '#' in token:
                        token = token.split('#')[0]
                    temp_tokens.append(token)
                tokens = temp_tokens
                sent = ' '.join(tokens)
                TITLE.text = sent

            tree.write("LemmatizerResults/" + directory + '/' + str(file))
            files.index(file)
