#! /usr/bin/env python

import os
import sys
import argparse
from pybtex.database.input import bibtex
from pybtex.database import BibliographyData

def arg_is_file(path):
    try:
        if not os.path.isfile(path):
            raise
    except:
        msg = '{0!r} is not a file'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path

def main_cli():
    import argparse

    parser = argparse.ArgumentParser(
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bib_path',
            metavar = 'BIB_PATH',
            type = arg_is_file,
            help = ('Path to bibtex-formatted file.'))
    parser.add_argument('-k', '--keywords',
            nargs = '+',
            type = str,
            default = ["OaksPeerReviewed", "OaksCVPreprint"],
            help = ('Keywords for reference filter.'))

    args = parser.parse_args()

    bib_parser = bibtex.Parser()
    bib_data = bib_parser.parse_file(args.bib_path)

    filtered_bib_data = BibliographyData()
    for key, entry in bib_data.entries.items():
        kwords = [x.strip() for x in entry.fields.get('keywords', '').split(',')]
        for kw in args.keywords:
            if kw in kwords:
                filtered_bib_data.add_entry(entry.key, entry)

    s = filtered_bib_data.to_string("bibtex")
    s = s.replace("= \"", "= {")
    s = s.replace("\",\n", "},\n")
    s = s.replace("\"\n", "}\n")
    sys.stdout.write(s)

if __name__ == '__main__':
    main_cli()
