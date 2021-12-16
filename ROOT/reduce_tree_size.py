import os
import ROOT

storedir = 'Downloads'
storepath = os.path.join(os.environ['HOME'], storedir)
f_old = ROOT.TFile.Open(os.path.join(storepath, 'hadd.root'), 'READ')
t_old = f_old.Get('FloatingpointThresholdDummyHistomaxnoareath20Genclustersntuple/HGCalTriggerNtuple')

outfile = os.path.join(storepath, 'skim.root')
f_new = ROOT.TFile(outfile, "recreate")
t_new = t_old.CloneTree(0)

for entry in range(0,t_old.GetEntries()):
    t_old.GetEntry(entry)
    t_new.Fill()
    if entry > 1000:
        break

f_new.Write()
print('Skimmed tree written at {}.'.format(outfile))
