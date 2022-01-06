#include <iostream>
#include <TLorentzVector.h>

/*
Calculates the transverse mass for a three body system.
Used when inspecting events using Foreworks in the browser.
*/
void calculate_transverse_mass()
{
    TLorentzVector met, muon, jet, track;

    met.SetPtEtaPhiM(46.6, 0, -0.414, 0);
    muon.SetPtEtaPhiM(11, 1.292, -0.580, 0);
    jet.SetPtEtaPhiM(39.6, 1.453, 2.865, 0);
    track.SetPtEtaPhiM(32.6, 1.456, 2.869, 0);

    auto mtcalc = [&](TLorentzVector a, TLorentzVector b, TLorentzVector c)
    {
        return sqrt(pow(a.Pt() + b.Pt() + c.Pt(), 2) - pow((a+b+c).Pt(), 2));
    };

    std::cout <<  " mtcalc(muon,met,jet): " << mtcalc(muon,met,jet) <<  std::endl;
    std::cout <<  " mtcalc(muon,met,track): " << mtcalc(muon,met,track) <<  std::endl;
}

/*
Source ROOT if needed: ```source ${ROOTSYS}/bin/thisroot.sh```
Compile with ```g++ transverseMass.cc $(root-config --cflags --libs) -o tMass```
Run with ```./tMass```
*/
int main() {
  calculate_transverse_mass();
  return 0;
}
