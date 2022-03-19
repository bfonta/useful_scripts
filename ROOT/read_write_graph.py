import ROOT
from math import sin
from array import array

fname = 'test.root'

################################
# Create and save TGraph
################################
f1 = ROOT.TFile(fname, 'RECREATE')
f1.cd()

n = 20
x, y = array( 'd' ), array( 'd' )
 
for i in range( n ):
   x.append( 0.1*i )
   y.append( 10*sin( x[i]+0.2 ) )
 
gr = ROOT.TGraph( n, x, y )
gr.SetLineColor( 2 )
gr.SetLineWidth( 4 )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 21 )
gr.SetTitle( 'a simple graph' )
gr.GetXaxis().SetTitle( 'X title' )
gr.GetYaxis().SetTitle( 'Y title' )
gr.Draw( 'ACP' )

gr.Write('graph')

f1.Close()

################################
# Open and read TGraph
################################
print('Reading file...')

f1 = ROOT.TFile.Open(fname)
keyList = ROOT.TIter(f1.GetListOfKeys())

for key in keyList:
    cl = ROOT.gROOT.GetClass(key.GetClassName())
    if not cl.InheritsFrom("TGraph"):
        continue
    h = key.ReadObj()

    for datapoint in range(h.GetN()):
        print(h.GetPointX(datapoint), h.GetPointY(datapoint))
        print(h.GetErrorXlow(datapoint), h.GetErrorXhigh(datapoint))
        print(h.GetErrorYlow(datapoint), h.GetErrorYhigh(datapoint))
        print()

