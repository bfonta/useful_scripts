#include <iostream>
#include <vector>
#include "TString.h"
#include "TFile.h"
#include "TPad.h"
#include "TCanvas.h"
#include "TGaxis.h"
#include "TH1.h"
#include "TTree.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TLegend.h"

using namespace std;

void quick_tree_comp(bool doLog, bool doShape) {
  TString base = "/data_CMS/cms/alves/HHresonant_SKIMS";

  //"TTTo2L2Nu"; //"TTToHadronic"; "TTToSemiLeptonic";
  TString process = "GluGluToRadionToHHTo2B2Tau_M-1000_";

  TFile *f_new = new TFile(base+"/SKIMS_UL18_validateMETNoSF_Sig_V2/"+process+"/hadded.root");
  TFile *f_old = new TFile(base+"/SKIMS_UL18_validateMETNoSF_Sig_V2/"+process+"/hadded.root");

  TTree *t_new = (TTree*)f_new->Get("HTauTauTree");
  TTree *t_old = (TTree*)f_old->Get("HTauTauTree");

  TString sel_base = " && pairType == 2 && nleps == 0 && nbjetscand > 1";
  //TString sel_new = "isLeptrigger" + sel_base;
  TString sel_new = "isMETtrigger && !isLeptrigger && !isSingleTautrigger" + sel_base;
  TString sel_old = "isLeptrigger && !isSingleTautrigger" + sel_base;
  vector<TString> vars = {{
      // "HHKin_mass", "HH_mass"
      // "bjet1_JER", "bjet2_JER", "bjet1_pt", "bjet1_pt_raw", "bjet2_pt_raw",
      "dau2_pt", 
    }};
  // vector<float> mins = {{200., 0., 0., 15., -2.6, 15., -2.6}};
  // vector<float> maxs = {{800., 200., 200., 200., 2.6, 200., 2.6}};
  vector<float> mins = {{15.}};
  vector<float> maxs = {{200.}};

  TString istr = "";
  for(int i=0; i<vars.size(); ++i)
	{
	  istr = std::to_string(i).c_str();
	  
	  TH1F *h_new = new TH1F("hnew"+istr, "", 80, mins[i], maxs[i]);
	  TH1F *h_old = new TH1F("hold"+istr, "", 80, mins[i], maxs[i]);
	  h_old->SetLineColor(2);
    
	  t_new->Draw(vars[i] + ">>hnew"+istr, sel_new, "");
	  t_old->Draw(vars[i] + ">>hold"+istr, sel_old, "");
  
	  TCanvas *c = new TCanvas("c"+istr, "c"+istr, 600, 600);
	  gPad->SetLogx();
	  TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
	  pad1->SetBottomMargin(0); // Upper and lower plot are joined
	  pad1->SetGridx();         // Vertical grid
	  pad1->Draw();             // Draw the upper pad: pad1
	  pad1->cd();               // pad1 becomes the current pad
	  if (doLog)
		gPad->SetLogx();

	  if(doShape){
		cout << "old int = " << h_old->Integral() << " | " << "new int = " << h_new->Integral()<<endl;
		h_old->Scale(1./h_old->Integral());
		h_new->Scale(1./h_new->Integral());
	  }

	  double ymax = 1.1*h_old->GetMaximum();
	  ymax = std::max(ymax, 1.1*h_new->GetMaximum());
	  h_old->GetYaxis()->SetRangeUser(0., ymax);
	  h_new->GetYaxis()->SetRangeUser(0., ymax);

	  h_old->Draw("hist e");               // Draw h1
	  h_new->Draw("hist e same");         // Draw h2 on top of h1
  
	  TLegend *legend = new TLegend(0.52, 0.80, 0.89, 0.91);
	  legend->AddEntry(h_old, process + " (old)", "lp");
	  legend->AddEntry(h_new, process + " (new)", "lp");
	  legend->Draw("same");

	  // Do not draw the Y axis label on the upper plot and redraw a small
	  // axis instead, in order to avoid the first label (0) to be clipped.
	  // h_new->GetYaxis()->SetLabelSize(0.);
	  // TGaxis *axis = new TGaxis(250, 20, 250, 220, 20, 220, 510, "");
	  // axis->SetLabelFont(43); // Absolute font size in pixel (precision 3)
	  // axis->SetLabelSize(15);
	  // axis->Draw();

	  // lower plot will be in pad
	  c->cd();          // Go back to the main canvas before defining pad2
	  TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);   
	  pad2->SetTopMargin(0);
	  pad2->SetBottomMargin(0.3);
	  pad2->SetGridx(); // vertical grid
	  pad2->Draw();
	  pad2->cd();       // pad2 becomes the current pad
	  if (doLog)
		gPad->SetLogx();


	  // Define the ratio plot
	  TH1F *h3 = (TH1F*)h_new->Clone("h3");
	  h3->SetLineColor(kBlack);
	  // h3->SetMinimum(0.7);  // Define Y ..
	  // h3->SetMaximum(1.3); // .. range
	  h3->Sumw2();
	  h3->SetStats(0);      // No statistics on lower plot
	  h3->Divide(h_old);

	  h3->GetXaxis()->SetTitle(vars[i]);
	  h3->GetXaxis()->SetTitleSize(20);
	  h3->GetXaxis()->SetTitleFont(43);
	  h3->GetXaxis()->SetTitleOffset(1.45);

	  h3->Draw("hist e");       // Draw the ratio plot

	  // h_new settings
	  h_new->SetLineColor(kBlue+1);
	  h_new->SetLineWidth(2);
	  // Y axis h_new plot settings
	  h_new->GetYaxis()->SetTitleSize(20);
	  h_new->GetYaxis()->SetTitleFont(43);
	  h_new->GetYaxis()->SetTitleOffset(1.55);
	  // h_old settings
	  h_old->SetLineColor(kRed);
	  h_old->SetLineWidth(2);
	  // Ratio plot (h3) settings
	  h3->SetTitle(""); // Remove the ratio title
	  // Y axis ratio plot settings
	  h3->GetYaxis()->SetTitle("ratio hnew/hold ");
	  h3->GetYaxis()->SetNdivisions(505);
	  h3->GetYaxis()->SetTitleSize(20);
	  h3->GetYaxis()->SetTitleFont(43);
	  h3->GetYaxis()->SetTitleOffset(1.55);
	  h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
	  h3->GetYaxis()->SetLabelSize(15);
	  // X axis ratio plot settings
	  h3->GetXaxis()->SetTitleSize(20);
	  h3->GetXaxis()->SetTitleFont(43);
	  h3->GetXaxis()->SetTitleOffset(4.);
	  h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
	  h3->GetXaxis()->SetLabelSize(15);
  
	  c->SaveAs(process + "_" + vars[i] + "_testFromTrees.pdf");
	} 
}

//compile with g++ testFromTrees.cc -o tt.exe `root-config --cflags --glibs`
int main() {
  gStyle->SetOptStat(0);
  gROOT->SetBatch(true);

  bool doLog = false;
  bool doShape = false;

  quick_tree_comp(doLog, doShape);
  
  return 0;
}
