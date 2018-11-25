import helpers
import torch
from language import Language

"""
Data Extraction
"""

max_length = 20


def filter_pair(p):
    is_good_length = len(p[0].split(' ')) < max_length and len(p[1].split(' ')) < max_length
    return is_good_length


def filter_pairs(pairs):
    return [pair for pair in pairs if filter_pair(pair)]


def prepare_data(lang_name):

    # Read and filter sentences
    input_lang, output_lang, pairs = read_languages(lang_name)
    pairs = filter_pairs(pairs)

    # Index words
    for pair in pairs:
        input_lang.index_words(pair[0])
        output_lang.index_words(pair[1])

    return input_lang, output_lang, pairs


def read_languages(lang):

    # Read and parse the text file
    doc = open('./data/%s.txt' % lang).read()
    lines = doc.strip().split('\n')

    # Transform the data and initialize language instances
    pairs = [[helpers.normalize_string(s) for s in l.split('\t')] for l in lines]
    input_lang = Language('eng')
    output_lang = Language(lang)

    return input_lang, output_lang, pairs


"""
Data Transformation
"""


# Returns a list of indexes, one for each word in the sentence
def indexes_from_sentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(' ')]


def tensor_from_sentence(lang, sentence, device='cpu'):
    indexes = indexes_from_sentence(lang, sentence)
    indexes.append(Language.eos_token)
    tensor = torch.LongTensor(indexes).view(-1, 1).to(device)
    return tensor


def tensor_from_pair(pair, input_lang, output_lang, device='cpu'):
    input = tensor_from_sentence(input_lang, pair[0], device)
    target = tensor_from_sentence(output_lang, pair[1], device)
    return input, target
