import ROOT

inputfiles = os.path.join('full_path_list_of_files.txt')

#### Parse input list
filelist = []
with open(inputfiles) as fIn:
    for line in fIn:
        if '.root' in line:
            if not os.path.exists(line[:-1]):
                raise ValueError('[' + os.path.basename(__file__) + '] The input file does not exist: {}'.format(line))
            filelist.append(line[:-1])

#### Add files to the TChain
chain = ROOT.TChain('TreeName') #tree name, the same in all input files
for line in filelist:
    if args.debug:
        print("Adding file: " + line)
        chain.Add(line)

rdf = ROOT.RDataFrame(chain)
rdf = rdf.Display({'var1', 'var2'}, 30) #variables and number of entries to display
rdf.Print()
