import gensim


def build_sents():

    stoplist = set('when are if you your we should by it who very up just so about but many much her him would with no or for a of the and to in he she not they them is have be that this those these was has what been as i'.split())

    sentences = []
    with open('texts.txt') as f:

        for line in f:

            tokens = list(gensim.utils.tokenize(line, lowercase=True))

        sentences.append([t for t in tokens if t not in stoplist])

    return sentences
