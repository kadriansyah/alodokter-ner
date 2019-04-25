import nltk
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

        self.file = file
        self.start_tag = ''

    def empty_line(self):
        self.file.write('\n')

    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        self.start_tag = tag

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        self.start_tag = ''

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        tokens = nltk.word_tokenize(data)
        for idx,token in enumerate(tokens):
            if self.start_tag == '':
                print(token + '\t' + 'O')
                self.file.write(token + '\t' + 'O' + '\n')
            else:
                print(token + '\t' + 'B-' + self.start_tag.upper())
                if idx == 0:
                    self.file.write(token + '\t' + 'B-' + self.start_tag.upper() + '\n')
                else:
                    self.file.write(token + '\t' + 'I-' + self.start_tag.upper() + '\n')

file = open('alodokter/data/train.txt','w')
parser = MyHTMLParser()
with open('alodokter/data/raw_ner_train.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print('PROCESSING: '+ line)
        parser.feed(line)
        parser.empty_line()
f.close()
file.close()
