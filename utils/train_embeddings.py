"""
Usage: python3 train_embeddings.py raw_file [column]

This will read a gzipped training file that may have two or more tab-seperated
columns. In that case, the column argument dictates from which column to take
the sentences (starting with 0). Each line should contain one sentence.

The generated model will be pickled and written into a file in the vec/
directory.
"""
import gensim
import sys
import gzip
import pickle

class Streamer(object):
    '''For whatever reason, gensim is fine with iterators, but not with generators.'''
    def __init__(self, inp, index=0):
        if ".gz" in inp:
            self.inp = gzip.open(inp, "rt")
            self.gz = True
        else:
            self.inp = open(inp)
            self.gz = False
        self.index = index
    def __iter__(self):
        self.inp.seek(0)
        return self
    def __next__(self):
        if self.gz:
            sentence = next(self.inp).split("\t")[self.index]
            return [word[:6].lower() for word in sentence.split() if word.isalpha()]
        else:
            sentence = next(self.inp)
            return [word[:6].lower() for word in sentence.split() if word.isalpha()]
    def __del__(self):
        self.inp.close()

if len(sys.argv) > 2:
    index = int(sys.argv[2])
else:
    index = 0

stream = Streamer(sys.argv[1], index)

model = gensim.models.Word2Vec(stream, sg=1)

with open("output-" + sys.argv[1].split("/")[-1].split("-")[0] + ".pkl", "wb") as f:
    print("Writing to output-" + sys.argv[1].split("/")[-1].split("-")[0] + ".pkl")
    pickle.dump(model, f)
