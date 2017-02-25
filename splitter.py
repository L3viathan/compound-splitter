#!/usr/bin/env python3
"""
Compound Splitter

Usage:
    splitter.py [-v ...] [options] <file>...

Options:
    --help                      Display this help and exit.
    -L --lang=<...>             Specify the language [default: de].
    -v --verbose                Be verbose. Repeatable for more verbosity.
    -S --stopwords=<yes|no>     Use stopword list [default: yes].
    -f --force-split=<yes|no>   Try always splitting [default: no].
    -M --min-freq=<...>         Minimum frequency to consider word [default: 2].
    -l --limit=<n>              Consider only the top n words in the lexicon.
    --ranking=<...>             Comma-seperated list of ranking methods to use.
    --cleaning=<...>            Comma-seperated list of cleaning methods to use.

Possible values for the --ranking switch are methods of the Splitter class that
start with "rank_":

- semantic_similarity
- avg_frequency
- most_known
- longest
- shortest

The default is: --ranking=avg_frequency,semantic_similarity,shortest

Possible values for the --cleaning switch are methods of the Splitter class
that start with "clean_":

- general
- last_parts
- suffix
- prefix

"""
import os.path
import docopt
import pickle
from sys import stderr, version_info, exit
from math import sqrt, log2 as lg
from operator import itemgetter, mul
from collections import Counter
from fileinput import input as fileinput
from functools import reduce
__loc__ = os.path.realpath(os.path.join(os.getcwd(),
    os.path.dirname(__file__)))


def log0(x):
    return 0 if x == 0 else lg(x)

def pairwise(iterable):
    """Iterate over pairs of an iterable."""
    i = iter(iterable)
    j = iter(iterable)
    next(j)
    yield from zip(i, j)

def wrap_functions(fns):
    def wrapper(arg):
        for fn in fns:
            arg = fn(arg)
        return arg
    return wrapper

class Splitter(object):
    def log(self, level, *args, **kwargs):
        """Print to stderr if verbose mode is set"""
        if self.verbose >= level:
            print(*args, file=stderr, **kwargs)

    def __init__(self, *, language="de", verbose=False, args):
        """Initialize the Splitter."""
        self.verbose = verbose
        self.force_split = args.get('--force-split', 'no') == 'yes'
        self.use_stopwords = args.get('--stopwords', 'yes') == 'yes'
        self.min_freq = int(args.get('--min-freq', '2'))
        self.words = Counter()
        self.set_language(language)
        self.read_lexicon(limit=args.get('--limit', None))
        if '--ranking' in args and args['--ranking'] is not None:
            self.rankings = args['--ranking'].split(",")
        else:
            self.rankings = 'avg_frequency', 'semantic_similarity', 'shortest'
        if '--cleaning' in args and args['--cleaning'] is not None:
            self.cleanings = args['--cleaning'].split(",")
        else:
            self.cleanings = 'general', 'last_parts', 'suffix', 'prefix'
        self.clean = wrap_functions(getattr(self, 'clean_' + method) for method in self.cleanings)
        if 'semantic_similarity' in self.rankings:
            self.read_vectors()
        else:
            self.vec = None

    def set_language(self, language):
        """Set the language and its binding morphemes."""
        self.lang = language
        if language == "de":
            self.binding_morphemes = ["s", "e", "en", "nen", "ens", "es", "ns", "er", "n"]
            self.negative_morphemes = []#,"en,  "n"]
        elif language == "sv":
            self.binding_morphemes = ["s"]
            self.negative_morphemes = []
        elif language == "hu":
            self.binding_morphemes = ["ó", "ő", "ba", "ítő", "es", "s", "i", "a"]
            self.negative_morphemes = []
        else:
            raise NotImplementedError()

    def read_lexicon(self, limit=None):
        """Read the language-specific lexicon."""
        if limit is not None:
            limit = int(limit)
        self.log(
                1,
                "Loading " + os.path.join(__loc__, "lex", self.lang + ".lexicon.tsv"),
                end='',
                flush=True,
                )
        with open(os.path.join(__loc__, "lex", self.lang + ".lexicon.tsv")) as f:
            for index, line in enumerate(f):
                if limit is not None and index >= limit:
                    break
                word, count = line.split()  # fix_text() removed
                if len(word) < 4: continue  # filter out noise
                # if not word.isalpha(): continue
                count = int(count)
                if count < self.min_freq: continue
                self.words[word.lower()] += count
        if self.use_stopwords:
            with open(os.path.join(__loc__, "lex", self.lang + ".stopwords.txt")) as f:
                for line in f:
                    word = line.strip()
                    if word in self.words:
                        del self.words[word]
        if self.use_stopwords:
            with open(os.path.join(__loc__, "lex", self.lang + ".suffixes.txt")) as f:
                self.suffixes = set(map(str.strip, f))
            with open(os.path.join(__loc__, "lex", self.lang + ".prefixes.txt")) as f:
                self.prefixes = set(map(str.strip, f))
        else:
            self.suffixes = set()
            self.prefixes = set()
        self.log(1, "...done")

    def read_vectors(self):
        """Read the vector space into self.vec."""
        with open(os.path.join(__loc__, "lex", "{lang}.vectors.pkl".format(lang=self.lang)), "rb") as f:
            self.vec = pickle.load(f)

    def not_a_binding_morpheme(self, part):
        return part not in self.binding_morphemes

    @staticmethod
    def left_slices(word, *, minlen=1):
        """Yield every possible left slice of a word, starting with minlen."""
        for i in range(minlen, len(word)+1):
            yield word[:i], word[i:]

    def splits(self, word):
        """Split a given word in all possible ways."""
        for left, right in self.left_slices(word.lower()):
            if left in self.binding_morphemes or left in self.words:
                if right:  # not the last part
                    for right in self.splits(right):
                        yield (left, *right)
                else:
                    yield (left,)
            else:  # left part isn't a word, so continue
                for nm in self.negative_morphemes:
                    if left+nm in self.words:
                        for right in self.splits(right):
                            yield (left, *right)
                    break
                else:  # nobreak
                    if right:
                        continue
                    else:
                        # maybe unless it's the last part
                        yield (left,)

    def split(self, word, *, output="tuple"):
        """Split a given word in its parts."""
        # high-level method. This basically filters the output from splits
        word = word.lower()
        self.log(2, "Splitting", word)
        splits = self.splits(word)
        # if not splits:  # in case we change the returning of unknown things
        #     return (word,) if output == "tuple" else word

        clean = self.clean(splits)
        rank = self.rank(clean)

        if rank:
            best = rank[0]
        else:
            best = word

        self.log(2, "Best:", best)

        # if self.use_stopwords and len(best) > 1 and best[-1] in self.suffixes:
        #     best = best[:-2] + (best[-2]+best[-1],)

        return best[-1] if output == "tuple" else self.evalify(best[-1])

    def rank(self, clean):
        """
        Given an iterable of possible splits, return a sorted list.

        The list will contain tuples of various scores, where the last element
        of the tuple will be the corresponding split.

        >>> self.rank({('krankenhaus',), ('kranken', 'haus'), ...})
        [(1024751378, 1.0, -2, ('kranken', 'haus')), (748127142, 1.0, -3, ('krank', 'en', 'haus')), ...]

        The scoring methods are defined by self.rankings, which was initialized
        by command line or key word arguments.

        """
        ranked = []
        for split in clean:
            ranked.append((*(getattr(self, 'rank_' + method)(split) for method in self.rankings), split))
        ranked.sort(reverse=True)
        self.log(2, "Ranked:", ranked)
        if self.force_split:
            return [split for split in ranked if len(split[-1]) > 1]
        else:
            return ranked

    def clean_general(self, splits):
        for split in splits:
            cleaned = []
            i = 0
            last = len(split)-1
            while i <= last:
                if split[i] in self.words:
                    cleaned.append(split[i])
                elif i < len(split)-1 and split[i]+split[i+1] in self.words:
                    cleaned.append(split[i] + split[i+1])
                    i += 1
                elif i == 0 and len(split)>1 and split[i] in self.binding_morphemes:
                    cleaned.append(split[i] + split[i+1])
                    i += 1
                else:
                    cleaned.append(split[i])
                i += 1
            yield tuple(cleaned)

    def clean_last_parts(self, splits):
        for split in splits:
            if len(split[-1]) < 3:
                yield split[:-2] + (split[-2] + split[-1],)
            else:
                yield split

    def clean_suffix(self, splits):
        for split in splits:
            if any(split[-1].startswith(suf) for suf in self.suffixes):
                pass
            else:
                yield split

    def clean_prefix(self, splits):
        for split in splits:
            if any(part in self.prefixes for part in split):
                pass
            else:
                yield split

    @staticmethod
    def nth_root(x, n):
        if n==2:
            return sqrt(n)
        else:
            return x**(1/n)

    def vecsim(self, left, right):
        if self.vec is not None:
            return self.vec.similarity(left[:6], right[:6])
        else:
            return 0

    def rank_avg_frequency(self, split):
        # if self.force_split and len([*filter(self.not_a_binding_morpheme, split)]) == 1:
        #     multiplier = 0.0001
        # else:
        #     multiplier = 1

        return reduce(mul,
                map(lambda x: self.words[x],
                    filter(self.not_a_binding_morpheme, split)
                    )
                )  # * multiplier

    def rank_longest(self, split):
        return len(split)

    def rank_shortest(self, split):
        return -len(split)

    def rank_semantic_similarity(self, split):
        """
        Return the average semantic similarity between adjacent parts of a split.
        """
        sims = [0]  # initialize with 0
        for left, right in pairwise([x for x in split if x not in self.binding_morphemes]):
            try:
                sims.append(self.vecsim(left, right))
            except KeyError:
                sims.append(0)
        return sum(sims)/len(sims)

    def rank_most_known(self, split):
        parts = [*filter(self.not_a_binding_morpheme, split)]

        if len(parts) == 0:
            return 0

        return sum(
                1 for p in parts
                if p in self.words
                or any(
                    p+nm in self.words for nm in self.negative_morphemes
                    )
                )/len(parts)

    def evalify(self, split):
        """
        From a tuple of parts, return a string.

        Seperate compounds with plus symbols and linking morphemes with pipe
        symbols.
        """
        result = ""
        for part in split:
            result += ("|" if part in self.binding_morphemes else "+") + part
        return result[1:]

if __name__ == '__main__':
    if version_info < (3, 5):
        print("Error: Python >=3.5 required.", file=sys.stderr)
        exit(1)
    args = docopt.docopt(__doc__)
    spl = Splitter(language=args['--lang'], verbose=args['--verbose'], args=args)
    for line in fileinput(args['<file>']):
        if not line.strip(): break
        print(line.strip(), spl.split(line.strip(), output="eval"), sep="\t")
