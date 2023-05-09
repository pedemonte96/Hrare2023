import ROOT

ROOT.ROOT.EnableImplicitMT()

chain = ROOT.TChain("events");
chain.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY09/2018/outname_mc1039_GFcat_D0StarCat_2018.root")

df = ROOT.RDataFrame(chain)

ROOT.gInterpreter.Declare('''
using Vec_i = ROOT::VecOps::RVec<int>;
using Vec_f = ROOT::VecOps::RVec<float>;
typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > PtEtaPhiMVector;

Vec_f getPTParticleMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_pt, int idParticle, int idMother){
    Vec_f selection = {};
    int indexMother = 9999;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother){//this is the D0*, mother of D0
            indexMother = i;
        }
        if(genPart_pdgId[i] == idParticle && genPart_genPartIdxMother[i] == indexMother){//get D0 son of D0Star
            selection.push_back(genPart_pt[i]);
        }
    }
    return selection;
}

float deltaPhi(float phi1, float phi2) {
  float result = phi1 - phi2;
  while (result > float(M_PI)) result -= float(2*M_PI);
  while (result <= -float(M_PI)) result += float(2*M_PI);
  return result;
}

float deltaR2(float eta1, float phi1, float eta2, float phi2) {
  float deta = eta1-eta2;
  float dphi = deltaPhi(phi1,phi2);
  return deta*deta + dphi*dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2) {
  return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
}


Vec_f getDRParticleMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, int idParticle1, int idMother1, int idParticle2, int idMother2){
    Vec_f selection = {};
    int indexMother1 = 9999;
    int indexMother2 = 9999;
	float phi1 = 0;
	float phi2 = 0;
	float eta1 = 0;
	float eta2 = 0;
	bool particle1 = false;
	bool particle2 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother1){
            indexMother1 = i;
        }
        if(genPart_pdgId[i] == idMother2){
            indexMother2 = i;
        }
        if(genPart_pdgId[i] == idParticle1 && genPart_genPartIdxMother[i] == indexMother1){//get particle 1
            phi1 = genPart_phi[i];
            eta1 = genPart_eta[i];
			particle1 = true;
        }
        if(genPart_pdgId[i] == idParticle2 && genPart_genPartIdxMother[i] == indexMother2){//get particle 2
            phi2 = genPart_phi[i];
            eta2 = genPart_eta[i];
			particle2 = true;
        }
    }
	if(particle1 && particle2){
		selection.push_back(deltaR(eta1, phi1, eta2, phi2));
	}
    return selection;
}

Vec_f getHCandMass(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, Vec_f& genPart_pt, Vec_f& genPart_mass, int idParticle1, int idMother1, int idParticle2, int idMother2){
    Vec_f selection = {};
    int indexMother1 = 9999;
    int indexMother2 = 9999;
    float phi1 = 0;
    float phi2 = 0;
    float eta1 = 0;
    float eta2 = 0;
	float pt1 = 0;
	float pt2 = 0;
	float mass1 = 0;
	float mass2 = 0;
    bool particle1 = false;
    bool particle2 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother1){
            indexMother1 = i;
        }
        if(genPart_pdgId[i] == idMother2){
            indexMother2 = i;
        }
        if(genPart_pdgId[i] == idParticle1 && genPart_genPartIdxMother[i] == indexMother1){//get particle 1
            phi1 = genPart_phi[i];
            eta1 = genPart_eta[i];
			pt1 = genPart_pt[i];
			mass1 = genPart_mass[i];
            particle1 = true;
        }
        if(genPart_pdgId[i] == idParticle2 && genPart_genPartIdxMother[i] == indexMother2){//get particle 2
            phi2 = genPart_phi[i];
            eta2 = genPart_eta[i];
			pt2 = genPart_pt[i];
			mass2 = genPart_mass[i];
            particle2 = true;
        }
    }
    if(particle1 && particle2 && pt1 > 25){
	//	cout << mass1 << " " << mass2 << endl;
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(5, eta1, phi1, 0.142);
        selection.push_back((p_part1 + p_part2 + p_part3).M());
    }
    return selection;
}




''')



h1=df.Define("D0StarGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 423, 25)").Histo1D(("hist", "D0Star Gen PT", 100, 0, 300),"D0StarGenPT")

h2=df.Define("D0GenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 421, 423)").Define("D0GenPTgood","D0GenPT[D0GenPT>25]").Histo1D(("hist", "D0 Gen PT", 100, 0, 300),"D0GenPTgood")

h3=df.Define("HiggsPhotonGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 25)").Histo1D(("hist", "Photon from Higgs Gen PT", 100, 0, 300),"HiggsPhotonGenPT")

h4=df.Define("PhotonD0StarGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 423)").Define("PhotonD0StarGenPTGood", "PhotonD0StarGenPT[PhotonD0StarGenPT>0]").Histo1D(("hist", "Photon from D0Star Gen PT", 200, 0, 30),"PhotonD0StarGenPTGood")

h5=df.Define("Pi0D0StarGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 423)").Define("Pi0D0StarGenPTGood", "Pi0D0StarGenPT[Pi0D0StarGenPT>0]").Histo1D(("hist", "Pi0 from D0Star Gen PT", 200, 0, 30),"Pi0D0StarGenPTGood")
#print(h4.FindLastBinAbove(), h5.FindLastBinAbove())

h6=df.Define("PhotonGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 22, 423, 421, 423)").Histo1D(("hist", "Photon DR Gen", 200, 0, 0.5),"PhotonGenDR")
h7=df.Define("PionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 423, 421, 423)").Histo1D(("hist", "Pion DR Gen", 200, 0, 0.5),"PionGenDR")

h8=df.Define("KaonPionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 211, 421, -321, 421)").Histo1D(("hist", "Kaon-Pion DR Gen", 100, 0, 0.2),"KaonPionGenDR")

h9=df.Define("HCandMassGen", "getHCandMass(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 421, 423, 22, 25)").Histo1D(("hist", "H Cand Mass Gen", 100, 0, 200),"HCandMassGen")

canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)
canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h2.Draw("hist")
canvas.cd(3)
h3.Draw("hist")
p = canvas.cd(4)
#p.SetLogy()
#h4.Draw("hist")
#canvas.cd(5)
#h5.Draw("hist")
#canvas.cd(6)
stack = ROOT.THStack("stack", "PT Gen Photon/Pion from D0*->D0+x")
h4.SetFillColor(ROOT.kGreen-9)
h5.SetFillColor(ROOT.kRed-9)
stack.Add(h4.GetValue())
stack.Add(h5.GetValue())
stack.Draw()
stack.GetXaxis().SetRangeUser(0, 20)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h4.GetValue(), "Photon", "f")
legend.AddEntry(h5.GetValue(), "Pion", "f")
legend.Draw()

canvas.cd(5)
stack2 = ROOT.THStack("stack", "DR Gen Photon/Pion respect to D0")
h6.SetFillColor(ROOT.kGreen-9)
h7.SetFillColor(ROOT.kRed-9)
stack2.Add(h6.GetValue())
stack2.Add(h7.GetValue())
stack2.Draw()
stack2.GetXaxis().SetRangeUser(0, 0.2)
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(h6.GetValue(), "Photon", "f")
legend2.AddEntry(h7.GetValue(), "Pion", "f")
legend2.Draw()

#canvas.cd(7)
#h6.Draw("hist")
#canvas.cd(8)
#h7.Draw("hist")
p=canvas.cd(6)
#p.SetLogy()
h8.Draw("hist")

p=canvas.cd(7)
p.SetLogy()
h9.Draw("hist")

canvas.SaveAs("~/public_html/D0StarKinMassGEN.png")

