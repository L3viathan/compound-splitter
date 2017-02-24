# Quickstart

    Compound Splitter

    Usage:
        splitter.py [-v ...] [options] <file>...

    Options:
        --help                   Display this help and exit.
        -L --lang=<...>          Specify the language [default: de].
        -v --verbose             Be verbose. Repeatable for more verbosity.
        -S --stopwords=<yes|no>  Use stopword list [default: yes].
        --force-split=<yes|no>   Try always splitting [default: no].
        --min-freq=<yes|no>      Minimum frequency to consider word [default: 2].
        --ranking=<...>          Comma-seperated list of ranking methods to use.
        --cleaning=<...>         Comma-seperated list of cleaning methods to use.

You also see this text when running `splitter.py --help`.

# Installation

If you don't want to use the word embedding method, you can install only the
one then required package using:

    pip3 install docopt

If you want to install the full dependencies including gensim, you can instead
do:

    pip3 install -r requirements.txt

# Advanced Usage

## Using standard input
If you prefer to use standard input instead of a file, the script supports the
convention of using a single dash (`-`) in place of a file name.

## Extending the Splitter class
...
