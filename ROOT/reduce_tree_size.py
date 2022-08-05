import os
import argparse
import ROOT

def reduce_tree_size(infile, tname, nentries):
    f_old = ROOT.TFile.Open(infile, 'READ')
    t_old = f_old.Get(tname)

    base, ext = infile.split('.')
    outfile = base + '_reduced.' + ext

    f_new = ROOT.TFile(outfile, 'RECREATE')
    t_new = t_old.CloneTree(0)
     
    for entry in range(0,t_old.GetEntries()):
        t_old.GetEntry(entry)
        t_new.Fill()
        if entry > nentries:
            break
     
    f_new.Write()
    print('Skimmed tree written at {}.'.format(outfile))

if __name__ == '__main__':
    usage = '\n'.join(('Reduces the number of entries in a TTree.',
                       'Keeps the first `n` entries.'))
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('-i', '--infile', dest='infile',
                        required=True, help='input file')
    parser.add_argument('-t', '--treename', dest='tname',
                        required=True, help='name of the TTree')
    parser.add_argument('-n', '--nentries', dest='nentries',
                        type=int, default=100, help='number of entries to be kept')
    FLAGS = parser.parse_args()

    reduce_tree_size(FLAGS.infile, FLAGS.tname, FLAGS.nentries)
