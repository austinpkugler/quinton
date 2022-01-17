import re

import wikipedia
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def get_question():
    question = ''
    answer = ''

    while True:
        # summary = wikipedia.summary('Patrick Charles Scully') # wikipedia.random(1)
        summary = "Patrick Charles Scully (16 August 1887 - 6 February 1951) was an Australian politician. He was born at Tamworth to Thomas James Scully and Sarah Lucy, née Rutherford. After attending Bective Superior Public School he passed the teachers' examination and taught at various country schools from 1909 to 1920. On 25 January 1911 he married Nellie Evans. A supporter of the New England New State Movement, he served as a Labor member of the New South Wales Legislative Assembly for Namoi from 1920 to 1923, when he resigned and was replaced by his brother William. Scully died in Melbourne in 1951."
        summary = re.sub(r'([A-Za-z0-9]\.)([A-Za-z])', r'\1 \2', summary)

        sentence = sent_tokenize(summary)[0]
        words = nltk.pos_tag(word_tokenize(sentence))
        noun = [i for i in words if i[1] == 'NN']
        if noun:
            break

    for word in words:
        if word[1] == 'NN':
            answer = word[0]
            question += '_____ '
        else:
            question += word[0] + ' '

    question += '\n'
    answer = f'||{answer}||\n'

    return question + answer

get_question()