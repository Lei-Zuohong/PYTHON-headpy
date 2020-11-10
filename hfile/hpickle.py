# -*- coding: UTF-8 -*-
import pickle


def pkl_read(filename):
    with open(filename, 'rb') as infile:
        output = pickle.load(infile)
    return output


def pkl_dump(filename, target, protocol=2):
    with open(filename, 'wb') as outfile:
        pickle.dump(target, outfile, protocol=protocol)
