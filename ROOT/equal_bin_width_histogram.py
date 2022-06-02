import array
from ROOT import (
    TCanvas,
    TPad,
    TH1D,
    TGraphAsymmErrors,
    kRed,
    gROOT,
)
gROOT.SetBatch(True)

npoints = 6
xvals = [1,3,10,20,50,100]
yvals = [.5,.4,1.2,0.9,0.1,0.3]
eyu = [.1 for _ in range(npoints)]
eyd = [.1 for _ in range(npoints)]
g = TGraphAsymmErrors( npoints,
                       array.array('d', xvals),
                       array.array('d', yvals),
                       array.array('d', [3. for _ in range(npoints)]),
                       array.array('d', [3. for _ in range(npoints)]),
                       array.array('d', eyu),
                       array.array('d', eyd) )

gnew = TGraphAsymmErrors( npoints )
gnew.GetXaxis().SetNdivisions(108)
for ip in range(g.GetN()):
    gnew.SetPoint(ip, ip, g.GetPointY(ip) )
    gnew.SetPointError(ip, .5, .5,
                       g.GetErrorYlow(ip), g.GetErrorYhigh(ip) )

gax = gnew.GetXaxis();
for i,elem in enumerate(g.GetX()):
   gax.ChangeLabel(i+2,-1,-1,-1,-1,-1,str(int(elem)));
gax.ChangeLabel(1,-1,-1,-1,-1,-1,' ')
gax.ChangeLabel(-1,-1,-1,-1,-1,-1,' ')

c = TCanvas('c', 'c', 600, 600)
c.cd()

pad1 = TPad('pad1', 'pad1', .0, 0.5, 1, 1)
pad1.SetBottomMargin(0.1)
pad1.SetLeftMargin(0.1)
pad1.Draw()
pad1.cd()

g.SetTitle('')
g.GetXaxis().SetTitle('X [units]')
g.GetYaxis().SetTitle('Y [units]')
g.SetLineColor(1)
g.SetLineWidth(2)
g.SetMarkerColor(kRed)
g.SetMarkerSize(1.3)
g.SetMarkerStyle(20)
g.SetLineColor(kRed)
g.Draw('ap')

c.cd()

pad2 = TPad('pad2', 'pad2', 0, 0., 1, .5)
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.2)
pad2.SetLeftMargin(0.1)
pad2.Draw()
pad2.cd()

gnew.SetTitle('')
gnew.GetXaxis().SetTitle('X [units]')
gnew.GetYaxis().SetTitle('Y [units]')
gnew.SetLineWidth(2)
gnew.SetMarkerColor(kRed)
gnew.SetMarkerSize(1.3)
gnew.SetMarkerStyle(20)
gnew.SetLineColor(kRed)
gnew.GetXaxis().SetLabelSize(.05)
gnew.Draw('ap')

c.SaveAs('equal_bin_width_histogram.png')
