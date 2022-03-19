import os
import glob
import ROOT

file_name = os.path.join( os.environ['HOME'], 'Downloads',
                     'trigSF_MET2018_TT_etau_dau1_pt_Ele32_default_CUTS_NoCut.root' )
afile = ROOT.TFile.Open(file_name)
graph_name = 'Data'
graph = afile.Get(graph_name)
for point in range(graph.GetN()):
    print('X value of point {}: {}'.format(point, graph.GetPointX(point)))
    print('Y value of point {}: {}\n'.format(point, graph.GetPointY(point)))
    

