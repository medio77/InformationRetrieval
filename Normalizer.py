import xml.etree.ElementTree as ET
import os
import hazm

normalizer = hazm.Normalizer()

directories = []
for subdir, dirs, files in os.walk("/home/mehdi/Desktop/documents/IR/Corpus/"):
    directories += dirs

for directory in directories:

    fileroot = '/home/mehdi/Desktop/documents/IR/Corpus/' + directory + '/'
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
                TEXT.text = normalizer.normalize(TEXT.text)

                TITLE = document.find("TITLE")
                TITLE.text = normalizer.normalize(TITLE.text)

            tree.write("NormalizerResult/" + directory + '/' + str(file))
            files.index(file)
