import os
import argparse
import ROOT
import array

def add_branch(infile, outfile, tname):
    f_old = ROOT.TFile.Open(infile, 'READ')
    t_old = f_old.Get(tname)

    f_new = ROOT.TFile(outfile, 'RECREATE')
    t_new = t_old.CloneTree(0)

    var = array.array('f', [1.0])
    bname = 'trigSF_inclMeth'
    bvar = t_new.Branch(bname, var, '{}/F'.format(bname))
    #t_new.SetBranchAddress(bname, var);
    
    for entry in range(0,t_old.GetEntries()):
        t_old.GetEntry(entry)
        var[0] = 1.
        t_new.Fill()
     
    f_new.Write()
    print('Branch {} added; tree stored at {}.'.format(bname, outfile))

if __name__ == '__main__':
    usage = 'Adds a branch to a tree'
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('-i', '--infile', dest='infile',
                        required=True, help='input file')
    parser.add_argument('-o', '--outfile', dest='outfile',
                        required=True, help='output file')
    parser.add_argument('-t', '--treename', dest='tname',
                        required=True, help='name of the TTree')
    FLAGS = parser.parse_args()

    add_branch(FLAGS.infile, FLAGS.outfile, FLAGS.tname)
