import xml.etree.ElementTree as ET
import os
import hazm
import csv

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
                unique_tokens = []  # per document
                for token in tokens:
                    if token not in unique_tokens:
                        unique_tokens.append(token)

                for unique_token in unique_tokens:
                    try:
                        bow[unique_token] += 1
                    except KeyError:
                        bow[unique_token] = 1

bow = {k: v for k, v in sorted(bow.items(), key=lambda item: item[1],reverse=True)}

with open('bow.csv', 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['Words', 'Document Frequency'])
    writer.writeheader()
    for word, df in bow.items():
        writer.writerow({'Words': word, 'Document Frequency': df})
