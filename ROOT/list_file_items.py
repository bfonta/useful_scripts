import ROOT

fname = '~/Downloads/output_0.root'
f1 = ROOT.TFile.Open(fname)
keyList = ROOT.TIter(f1.GetListOfKeys())
for key in keyList:
    cl = ROOT.gROOT.GetClass(key.GetClassName())
    if not cl.InheritsFrom("TH1"):
        continue
    h = key.ReadObj()
    print(h.GetName())

