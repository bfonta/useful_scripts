void get_trigbit_from_bigNtuple(){

  TString bigNtupleFileName = "bigntuple.root";

  TFile *f = TFile::Open(bigNtupleFileName);

  TH1F *htriggers = (TH1F*)f->Get("HTauTauTree/Counters");

  int offset = 4;
  for(size_t i = offset; i<=htriggers->GetNbinsX(); ++i)
    std::cout << i-4 << " - " << htriggers->GetXaxis()->GetBinLabel(i) << std::endl;

}
