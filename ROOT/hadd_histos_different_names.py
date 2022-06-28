"""
Creates histograms in different files with common and different names.
Useful to study the behaviour of the `hadd` command: it adds histograms
to the same file even when they only exist in one of the original files
"""
from ROOT import (
    TFile,
    TH1D,
    )
from array import array

nentries = 30
ext = '.root'
fnames = [ __file__.split('.')[0] + '_' + str(x) + ext for x in range(2) ]

# common histogram
for fname in fnames:
    f = TFile(fname, 'RECREATE')
    f.cd()

    nentries = 30
    hname = 'hcommon'
    h = TH1D(hname, hname, 2, 0.0, 2.0)
    for entry in range(nentries):
        h.Fill(0.5)
        if entry%3==0:
            h.Fill(1.5)
            
    h.Write()
    f.Close()

# file #1 histogram
f = TFile(fnames[0], 'UPDATE')
f.cd()

h1 = TH1D('h1', 'h1 title', 2, 0.0, 2.0)
for entry in range(nentries):
    h1.Fill(0.5)
    if entry%3==0:
        h1.Fill(1.5)
            
h1.Write()
f.Close()

# file #2 histogram
f = TFile(fnames[1], 'UPDATE')
f.cd()

h2 = TH1D('h2', 'h2 title', 2, 0.0, 2.0)
for entry in range(nentries):
    h2.Fill(0.5)
    if entry%3==0:
        h2.Fill(1.5)
            
h2.Write()
f.Close()
