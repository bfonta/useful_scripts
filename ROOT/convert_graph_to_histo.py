"""
Reference: https://root-forum.cern.ch/t/problem-in-fitting-in-function/38785/104
"""

import ROOT
from array import array

fnamein = 'Downloads/trigSF_mutau.root'
fnameout = 'test.root'
fin = ROOT.TFile(fnamein, 'READ')
fin.cd()
g = fin.Get('Data_VAR_dau2_eta_TRG_IsoMu24_CUT_NoCut');

n = g.GetN()
name = g.GetName()

# define x (bin centers)
x = array('d')
x.append((3.0 * g.GetX()[0] - g.GetX()[1]) / 2.0)
for i in range(1,n):
    x.append((g.GetX()[i-1] + g.GetX()[i]) / 2.0)
x.append((3.0 * g.GetX()[n-1] - g.GetX()[n-2]) / 2.0)
histo = ROOT.TH1D(name, name, n, x)

# fill y values (counts)
for i in range(n):
    histo.SetBinContent(i+1, g.GetY()[i])
    toterr = g.GetErrorYhigh(i)+g.GetErrorYlow(i)
    histo.SetBinError(i+1, toterr)

# write result to a new file
fout = ROOT.TFile(fnameout, 'RECREATE')
fout.cd()
histo.Draw()
histo.Write()

fout.Close()
fin.Close()
