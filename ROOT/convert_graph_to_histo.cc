#include <iostream>
#include <vector>
#include <string>
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TH1D.h"

/*
Reference: https://root-forum.cern.ch/t/problem-in-fitting-in-function/38785/104
*/

int main(int argc, char** argv) {
  TFile* fin  = TFile::Open("~/Downloads/trigSF_mutau.root", "READ");
  TFile* fout = TFile::Open("test.root", "RECREATE");
  TGraphAsymmErrors *graph = (TGraphAsymmErrors*)fin->Get("Data_VAR_dau2_eta_TRG_IsoMu24_CUT_NoCut");

  int n = graph->GetN();
  std::string name = graph->GetName();

  // define x (bin centers)
  double *x = new double[n+1];
  x[0] = (3.0 * graph->GetX()[0] - graph->GetX()[1]) / 2.0;
  for (int i=1; i<n; ++i) {
	x[i] = (graph->GetX()[i-1] + graph->GetX()[i]) / 2.0;
  }
  x[n] = (3.0 * graph->GetX()[n-1] - graph->GetX()[n-2]) / 2.0;

  TH1D *histo = new TH1D(name.c_str(), name.c_str(), n, x);
  
  // fill y values (counts)
  for (int i=0; i<n; ++i) {
	histo->SetBinContent(i+1, graph->GetY()[i]);
	float toterr = graph->GetErrorYhigh(i)+graph->GetErrorYlow(i);
	histo->SetBinError(i+1, toterr);
  }

  // write result to a new file
  fout->cd();
  histo->Draw();
  histo->Write();
	
  fout->Close();
  fin->Close();
	
  return 0;
}
