from nltk.tokenize import sent_tokenize

with open('article.txt') as file:
    file_contents = file.read()
    sentences = sent_tokenize(file_contents)
    clean_sentences = ' '.join(sentences).replace('\n', ' ')
    print(clean_sentences)