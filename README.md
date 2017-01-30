# Quickstart

    Compound Splitter

    Usage:
        splitter.py [options] <file>

    Options:
        --lang=<lang>      Specify the language [default: de].
        -v                 Be verbose
        --stopwords=<sw>   Use stopword list [default: yes].
        --force-split=<fs> Try always splitting [default: no].
        --use-counts=<uc>  Use frequencies to rank splitting [default: yes].
        --use-vectors=<uv> Use vectors to rank splitting [default: yes].
        --min-freq=<mf>    Minimum frequency to consider word [default: 2].
        --encoding=<enc>   Encoding the lexicon uses [default: latin-1].

You also see this text when running `splitter.py --help`.

# Installation

If you don't want to use the word embedding method, you can install only the
two then required methods using:

    pip3 install ftfy docopt

If you want to install the full dependencies including gensim, you can instead
do:

    pip3 install -r requirements.txt

# Advanced Usage

## Using standard input
If you prefer to use standard input instead of a file, you can create a named
pipe using the `mkfifo` command use this as the argument to the splitter and
pipe your requests into that file.

## Extending `Splitter`
For advanced usage, you can write a class that extends `Splitter` and implement
either of these methods:

- If you want to change the ranking system, call your method `custom_ranking`,
  taking the three arguments `self`, `clean` (the set of cleaned splits), and
  `word` (the original word). Your method should return your highest ranked
  split.
- If you want to change the cleaning system, call your method
  `custom_cleaning`, taking the three arguments `self`, `clean` (the set of
  already cleaned splits), and `word` (the original word). Return a possibly
  further cleaned set of splits.
