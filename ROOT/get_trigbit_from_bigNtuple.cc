#include <iostream>
#include "TFile.h"
#include "TH1F.h"

void get_trigbit_from_bigNtuple() {

  std::string big_ntuple_name = std::string(getenv("HOME")) + "/Downloads/Data_sample.root";
  TFile *f = TFile::Open(big_ntuple_name.c_str());
  if (f->IsZombie())
	throw std::runtime_error("File " + big_ntuple_name + " is corrupted.");
  TH1F *htriggers = (TH1F*)f->Get("HTauTauTree/Counters");

  int offset = 4; // skips non-trigger variables
  for(size_t i = offset; i<=htriggers->GetNbinsX(); ++i)
    std::cout << i-4 << " - " << htriggers->GetXaxis()->GetBinLabel(i) << std::endl;

}

// Compilation: 'g++ ROOT/get_trigbit_from_bigNtuple.cc -o trig $(root-config
// --cflags --libs)'
// Run: './trig'
int main(int argc, char** argv)
{
  get_trigbit_from_bigNtuple();
  return 0;
}
