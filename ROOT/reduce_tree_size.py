import ROOT

f_old = ROOT.TFile.Open('/home/bruno/Downloads/hadd.root', 'READ')
t_old = f_old.Get('FloatingpointThresholdDummyHistomaxnoareath20Genclustersntuple/HGCalTriggerNtuple')

f_new = ROOT.TFile("Downloads/skim.root", "recreate")
t_new = t_old.CloneTree(0)

for entry in range(0,t_old.GetEntries()):
    t_old.GetEntry(entry)
    t_new.Fill()
    if entry > 1000:
        break

t_new.Print()
f_new.Write()
