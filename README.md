# Quickstart

    Compound Splitter

    Usage:
        splitter.py [-v ...] [options] <file>...

    Options:
        --help                      Display this help and exit.
        -L --lang=<...>             Specify the language [default: de].
        -v --verbose                Be verbose. Repeatable for more verbosity.
        --stopwords                 Use stopword list [default: True].
        --no-stopwords              Don't use stopword list.
        -f --force-split            Try always splitting [default: False].
        --no-force-split            Don't try always splitting.
        -M --min-freq=<...>         Minimum frequency to consider word [default: 2].
        -l --limit=<n>              Consider only the top n words in the lexicon [default: 125000].
        --ranking=<...>             Comma-seperated list of ranking methods to use.
        --cleaning=<...>            Comma-seperated list of cleaning methods to use.
        --evaluate                  Evaluate a given gold file and print the results.
        --inspect=<word>            Debugging method to see what happens to a specific word.
        -W --print-wrong            When evaluating, print every incorrect word.

You also see this text when running `splitter.py --help`.

# Installation

The splitter is written in Python and requires a recent version of Python to
run (>=3.5)
If you don't want to use the word embedding method, you can install only the
one then required package using:

    pip3 install docopt

If you want to install the full dependencies including gensim, you can instead
do:

    pip3 install -r requirements.txt

This will install the correct version of all dependencies.

When cloning this repository from Github, one thing will be missing: The lexica
of the three languages. This is because of Github's file size limit. While they
are included in the attachment on SIS, they are also publicly available for
download [here](http://static.l3vi.de/lexica.zip).

# Usage

The script requires one (or more) files as a command-line argument.

    python3 splitter.py words.txt

If you prefer to use standard input instead of a file, the script supports the
convention of using a single dash (`-`) in place of a file name.

    python3 splitter.py -

The default language is German, but this can be changed by specifying the `--lang`
argument:

    python3 splitter.py --lang=sv swedish_words.txt

Other command-line switches can be specified in a similar way. Here's an example
that uses many switches:

    python3 splitter.py --lang=hu --ranking=avg_frequency,longest --cleaning=suffix -f -l100000 --no-stopwords hungarian_words.txt

## Ranking methods

Possible values for the `--ranking` switch are shown here. They are explained in
more detail in the thesis.

- semantic_similarity
- avg_frequency
- most_known
- longest
- shortest
- no_suffixes

## Cleaning methods

Possible values for the `--cleaning` switch are shown here. They are explained in
more detail in the thesis.

- general
- last_parts
- suffix
- prefix
- fragments

# Advanced Usage

## Usage from within Python

The `Splitter` class can also be instantiated from within another Python script.
It takes a `language` argument that defaults to `"de"`, a `verbose` argument
that defaults to `False` and a dictionary argument `args` that corresponds to
the one returned by docopt. If you are unsure what to set `args` to, call the
script from the command line with verbosity 2 (with `-vv`); then the docopt
dictionary is automatically printed in the beginning.

## Extending the Splitter class

Subclassing `Splitter` can be done to add language support, add ranking or
cleaning methods, or change core aspects of the system. This is described in
detail in Section 6.4 of the thesis.
