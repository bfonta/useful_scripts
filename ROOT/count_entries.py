import os
import argparse
import ROOT

def count_entries(infile, tname):
    f_old = ROOT.TFile.Open(infile, 'READ')
    tree = f_old.Get(tname)
    print(tree.GetEntries())

if __name__ == '__main__':
    usage = 'Counts entries in a TTree.'
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('-i', '--infile', required=True, help='input file')
    parser.add_argument('-t', '--tname', required=True, help='name of the TTree')
    FLAGS = parser.parse_args()
    count_entries(FLAGS.infile, FLAGS.tname)
