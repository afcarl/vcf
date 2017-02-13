#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools for the VCF dataset.

Type `./vcf_tools.py --help` for the command line tools and `help(vcf_tools)`
in the interactive Python shell for the module options of vcf_tools.
"""

import csv
import glob
import logging
import os
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

__version__ = "v0.1"


def load_data():
    data = []
    for csv_filepath in glob.glob("vcf-data/*.csv"):
        data.append([])
        with open(csv_filepath, 'r') as fp:
            spamreader = csv.reader(fp, delimiter=',', quotechar='"')
            next(spamreader, None)
            for epoch, score in spamreader:
                data[-1].append((int(epoch), float(score)))
    return data


def mse(ys, ys_predicted):
    """Calculate the mean squared error."""
    sum_ = 0.0
    for y, pred in zip(ys, ys_predicted):
        sum_ += (y - pred)**2
    return sum_ / float(len(ys))


def last_diff(ys, ys_predicted):
    """Return the difference of the last element and the prediction of it."""
    return ys[-1] - ys_predicted[-1]


def _get_nonexistant_path(csv_filepath):
    csv_filepath_abs = os.path.abspath(csv_filepath)
    directory = os.path.dirname(csv_filepath_abs)
    filename_ext = os.path.basename(csv_filepath_abs)
    filename = os.path.splitext(filename_ext)[0]
    i = 1
    new_name = os.path.join(directory, "%s-%i.csv" % (filename, i))
    while os.path.isfile(new_name):
        i += 1
        new_name = os.path.join(directory, "%s-%i.csv" % (filename, i))
    return new_name


def _extract(csv_filepath):
    """Extract all normalized curves from csv."""
    # Read CSV file
    curve_train = []
    curve_test = []
    with open(csv_filepath, 'r') as fp:
        spamreader = csv.reader(fp, delimiter=';', quotechar='"')
        for epoch, train, test in spamreader:
            curve_train.append((epoch, train))
            curve_test.append((epoch, test))

    # Write CSV file
    for data in [curve_train, curve_test]:
        filename = _get_nonexistant_path(csv_filepath)
        with open(filename, 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [('epoch', 'accuracy')] + data
            a.writerows(data)

    return [curve_train, curve_test]


def _get_parser():
    """Get parser object for hasy_tools.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--extract",
                        dest="extract_dir",
                        default=None,
                        help="a CSV file")
    return parser


if __name__ == "__main__":
    args = _get_parser().parse_args()
    if args.extract_dir is not None:
        _extract(args.extract_dir)
