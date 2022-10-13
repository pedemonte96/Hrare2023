import ROOT
import os
import sys
import json

ROOT.ROOT.EnableImplicitMT()
from utilsHrare import getMClist, getDATAlist, getSkims
from utilsHrare import plot, computeWeigths, getTriggerFromJson, getMesonFromJson, pickTRG, getMVAFromJson
from utilsHrare import loadCorrectionSet

doPlot = False
doMVA = False

isGF = False
isZinv = False
isZ = False
isW = False
isVBF = False
isVBFlow = False

isPhiCat = "false"
isRhoCat = "false"

if sys.argv[1]=='isGFtag': isGF = True
if sys.argv[1]=='isZinvtag': isZinv = True
if sys.argv[1]=='isZtag': isZ = True
if sys.argv[1]=='isWtag': isW = True
if sys.argv[1]=='isVBFtag': isVBF = True
if sys.argv[1]=='isVBFtaglow': isVBFlow = True

if sys.argv[2]=='isPhiCat': isPhiCat = "true"
if sys.argv[2]=='isRhoCat': isRhoCat = "true"

if sys.argv[4]=='2018': year = 2018
if sys.argv[4]=='2017': year = 2017
if sys.argv[4]=='2016': year = 2016
if sys.argv[4]=='12016': year = 12016

lumis={
    '12016': 19.52, #APV #(B-F for 2016 pre)
    '22016': 16.80, #postVFP
    '2016': 35.9,
    '2017': 36.4, #41.5, #(C,D,E,F for 2017)
    '12017': 7.7, #(F for 2017)
    '2018': 59.70,
    '12018': 39.54,
    'all': 86.92,      #19.52 + 7.7 + 59.70
}

#$$$$
#$$$$
#$$$$

PRESELECTION = "(nPhoton>0 && (nphi>0 or nrho>0) && PV_npvsGood>0)"
CLEAN_LepMes = "{}".format("(Sum(goodMeson)>0 and isMuorEle==1) ? deltaR(Muon_eta[goodMuons][0], Muon_phi[goodMuons][0], goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]]):(Sum(goodMeson)>0 and isMuorEle==2) ? deltaR(Electron_eta[goodElectrons][0], Electron_phi[goodElectrons][0], goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]]): -999")

CLEAN_JetMes = "{}".format("Sum(goodMeson)>0 ? std::min(deltaR(Jet_eta[goodJets][0], Jet_phi[goodJets][0], goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]]),deltaR(Jet_eta[goodJets][1], Jet_phi[goodJets][1], goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]])):-999")

CLEAN_JetPH = "{}".format("Sum(goodPhotons)>0 ? std::min(deltaR(Jet_eta[goodJets][0], Jet_phi[goodJets][0], goodPhotons_eta[index_pair[1]], goodPhotons_phi[index_pair[1]]),deltaR(Jet_eta[goodJets][1], Jet_phi[goodJets][1], goodPhotons_eta[index_pair[1]], goodPhotons_phi[index_pair[1]])):-999")


with open("config/selection.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

with open("config/trigger.json") as trgJsonFile:
    trgObject = json.load(trgJsonFile)
    trgJsonFile.close()

GOODJETS = jsonObject['GOODJETS']
LOOSEmuons = jsonObject['LOOSEmuons']
LOOSEelectrons = jsonObject['LOOSEelectrons']
GOODMUON = jsonObject['GOODMUON']
GOODELE = jsonObject['GOODELE']
JSON = jsonObject['JSON']
BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']
METFLAG = jsonObject['METFLAG']

MVA = jsonObject['MVAweights']
TRIGGERS = trgObject['triggers']
mesons = jsonObject['mesons']

#$$$$
#$$$$
#$$$$

def selectionTAG(df):

    if isZ:
        dftag = (df.Define("goodMuons","{}".format(GOODMUON)+" and Muon_mediumId and Muon_pfRelIso04_all < 0.25")
                 .Define("ele_mask", "cleaningMask(Photon_electronIdx[goodPhotons],nElectron)")
                 .Define("goodElectrons","{}".format(GOODELE)+" and Electron_mvaFall17V2Iso_WP90")
                 .Define("vetoMu","{}".format(LOOSEmuons))
                 .Define("vetoEle","{}".format(LOOSEelectrons))
                 .Filter("(Sum(goodMuons)+Sum(goodElectrons))==2 and (Sum(vetoEle)+Sum(vetoMu))==2","at least two good muons or electrons, and no extra loose leptons")
                 .Define("isMuorEle","Sum(goodMuons)==2?1: Sum(goodElectrons)==2?2 :0")
                 .Define("V_mass", "(Sum(goodMuons)==2 and Sum(Muon_charge[goodMuons])==0)? Minv(Muon_pt[goodMuons], Muon_eta[goodMuons], Muon_phi[goodMuons], Muon_mass[goodMuons]) : (Sum(goodElectrons)==2 and Sum(Electron_charge[goodElectrons])==0) ? Minv(Electron_pt[goodElectrons], Electron_eta[goodElectrons], Electron_phi[goodElectrons], Electron_mass[goodElectrons]): 0.")
                 .Filter("(V_mass>(91-10) and V_mass<(91+15))","At least one good Z")
                 .Define("Z_veto1", "Sum(goodElectrons)==2 ? Minv2(Electron_pt[goodElectrons][0], Electron_eta[goodElectrons][0], Electron_phi[goodElectrons][0], Electron_mass[goodElectrons][0],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).first: -1")
                 .Define("Z_veto2", "Sum(goodElectrons)==2 ? Minv2(Electron_pt[goodElectrons][1], Electron_eta[goodElectrons][1], Electron_phi[goodElectrons][1], Electron_mass[goodElectrons][1],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).first: -1")
                 .Filter("abs(Z_veto1-91) > 10 and abs(Z_veto2-91) > 10","kill the Z recontructed as gamma + electron")
#                 .Define("Mu1_hasTriggerMatch", "hasTriggerMatch(Muon_eta[goodMuons][0], Muon_phi[goodMuons][0], TrigObj_eta, TrigObj_phi)")
#                 .Define("Mu2_hasTriggerMatch", "hasTriggerMatch(Muon_eta[goodMuons][1], Muon_phi[goodMuons][1], TrigObj_eta, TrigObj_phi)")
#                 .Define("Ele1_hasTriggerMatch", "Sum(goodElectrons)>1 ? hasTriggerMatch(Electron_eta[goodElectrons][0], Electron_phi[goodElectrons][0], TrigObj_eta, TrigObj_phi) : 0")
#                 .Define("Ele2_hasTriggerMatch", "Sum(goodElectrons)>1 ? hasTriggerMatch(Electron_eta[goodElectrons][1], Electron_phi[goodElectrons][1], TrigObj_eta, TrigObj_phi) : 0")
#                 .Filter("trigger>0 and ((Mu1_hasTriggerMatch and Muon_pt[goodMuons][0]>26) or (Mu2_hasTriggerMatch and Muon_pt[goodMuons][1]>26))","pass trigger")
        )
        return dftag

    if isW:
        dftag = (df.Define("goodMuons","{}".format(GOODMUON)+" and Muon_tightId and Muon_pfRelIso04_all < 0.15")
                 .Define("ele_mask", "cleaningMask(Photon_electronIdx[goodPhotons],nElectron)")
                 .Define("goodElectrons","{}".format(GOODELE)+" and Electron_mvaFall17V2Iso_WP80") ## tight
                 .Define("vetoEle","{}".format(LOOSEelectrons))
                 .Define("vetoMu","{}".format(LOOSEmuons))
                 .Filter("DeepMETResolutionTune_pt>20 and (Sum(goodMuons)+Sum(goodElectrons))==1 and (Sum(vetoEle)+Sum(vetoMu))==1","MET and one lepton")
                 .Define("isMuorEle","Sum(goodMuons)==1?1: Sum(goodElectrons)==1?2 :0")
                 .Define("V_mass","Sum(goodMuons)>0 ? mt(Muon_pt[goodMuons][0], Muon_phi[goodMuons][0], DeepMETResolutionTune_pt, DeepMETResolutionTune_phi) : mt(Electron_pt[goodElectrons][0], Electron_phi[goodElectrons][0], DeepMETResolutionTune_pt, DeepMETResolutionTune_phi)")
                 .Filter("V_mass>20","MT>20")
                 .Define("Z_veto", "Sum(goodElectrons)==1 ? Minv2(Electron_pt[goodElectrons][0], Electron_eta[goodElectrons][0], Electron_phi[goodElectrons][0], Electron_mass[goodElectrons][0],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).first: -1")
                 .Filter("abs(Z_veto-91) > 10","kill the Z recontructed as gamma + electron")
#                 .Define("trigger","{}".format(TRIGGER))
#                 .Define("Mu1_hasTriggerMatch", "hasTriggerMatch(Muon_eta[goodMuons][0], Muon_phi[goodMuons][0], TrigObj_eta, TrigObj_phi)")
#                 .Filter("trigger>0 and Mu1_hasTriggerMatch and Muon_pt[goodMuons][0]>26","pass trigger")
                 .Define("deltaLepMeson","{}".format(CLEAN_LepMes))
                 .Define("dPhiGammaMET","abs(deltaPhi(goodPhotons_phi[index_pair[1]], DeepMETResolutionTune_phi))")
                 .Define("dPhiMesonMET","abs(deltaPhi(goodMeson_phi[index_pair[0]], DeepMETResolutionTune_phi))")
        )
        return dftag

    if isVBF or isVBFlow:

        VBFcut = "mJJ>300 and dEtaJJ>3 and Y1Y2<0"
        if isVBFlow: VBFcut = "mJJ>250 and dEtaJJ>3. and Y1Y2<0"

        dftag = (df.Define("goodJets","{}".format(GOODJETS)+" and (Jet_puId > 1)")
                 .Define("nGoodJets","Sum(goodJets)*1.0f").Filter("Sum(goodJets)>1","two jets for VBF")
                 .Define("mJJ","Minv(Jet_pt[goodJets], Jet_eta[goodJets], Jet_phi[goodJets], Jet_mass[goodJets])")
                 .Define("dEtaJJ","abs(Jet_eta[goodJets][0] - Jet_eta[goodJets][1])")
                 .Define("dPhiJJ","abs(deltaPhi(Jet_phi[goodJets][0],Jet_phi[goodJets][1]))")
                 .Define("Y1Y2","Jet_eta[goodJets][0]*Jet_eta[goodJets][1]")
                 .Filter("{}".format(VBFcut),"Filter on MJJ , Deta, Y1Y2")
                 .Define("ele_mask", "cleaningMask(Photon_electronIdx[goodPhotons],nElectron)")
                 .Define("vetoEle","{}".format(LOOSEelectrons))
                 .Define("vetoMu","{}".format(LOOSEmuons))
                 .Filter("(Sum(vetoEle)+Sum(vetoMu))==0", "no leptons")
#                 .Define("trigger","{}".format(TRIGGER))
#                 .Filter("trigger>0", "pass triggers")
                 .Define("jet1Pt","Jet_pt[goodJets][0]")
                 .Define("jet2Pt","Jet_pt[goodJets][1]")
                 .Define("jet1Eta","Jet_eta[goodJets][0]")
                 .Define("jet2Eta","Jet_eta[goodJets][1]")
                 .Define("deltaJetMeson","{}".format(CLEAN_JetMes))
                 .Define("deltaJetPhoton","{}".format(CLEAN_JetPH))
                 .Define("zepVar","compute_jet_HiggsVars_var(Jet_pt[goodJets],Jet_eta[goodJets],Jet_phi[goodJets],Jet_mass[goodJets], goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], goodMeson_pt[index_pair[0]],goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]], goodMeson_mass[index_pair[0]], 0)")
                 .Define("detaHigJet1","compute_jet_HiggsVars_var(Jet_pt[goodJets],Jet_eta[goodJets],Jet_phi[goodJets],Jet_mass[goodJets], goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], goodMeson_pt[index_pair[0]],goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]], goodMeson_mass[index_pair[0]], 1)")
                 .Define("detaHigJet2","compute_jet_HiggsVars_var(Jet_pt[goodJets],Jet_eta[goodJets],Jet_phi[goodJets],Jet_mass[goodJets], goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], goodMeson_pt[index_pair[0]],goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]], goodMeson_mass[index_pair[0]], 2)")
                 )

                 .Filter("DeepMETResolutionTune_pt<75","DeepMETResolutionTune_pt<75")
                 .Define("SoftActivityJetNjets5F","SoftActivityJetNjets5*1.0f")
                 )
        return dftag

    if isZinv:
        dftag = (df.Define("ele_mask", "cleaningMask(Photon_electronIdx[goodPhotons],nElectron)")
                 .Define("vetoEle","{}".format(LOOSEelectrons))
                 .Define("vetoMu","{}".format(LOOSEmuons))
                 .Filter("(Sum(vetoEle)+Sum(vetoMu))==0", "no leptons")
#                 .Define("trigger","{}".format(TRIGGER))
#                 .Filter("trigger>0", "pass triggers")
                 .Filter("DeepMETResolutionTune_pt>50","MET>50")
                 .Define("dPhiGammaMET","abs(deltaPhi(goodPhotons_phi[index_pair[1]], DeepMETResolutionTune_phi))")
                 .Define("dPhiMesonMET","abs(deltaPhi(goodMeson_phi[index_pair[0]], DeepMETResolutionTune_phi))")
                 .Define("ptRatioMEThiggs","abs(DeepMETResolutionTune_pt-HCandPT)/HCandPT")
                 .Define("goodJets","{}".format(GOODJETS))
                 .Define("nGoodJets","Sum(goodJets)*1.0f")
                  ## cleanup
                 .Define("metFilter","{}".format(METFLAG))
                 .Filter("metFilter", "pass METfilter")
                 .Filter("ptRatioMEThiggs<0.8","ptRatioMEThiggs<0.8")
                 .Filter("dPhiGammaMET>1","dPhiGammaMET>1")
                 .Filter("dPhiMesonMET>1","dPhiMesonMET>1")

                 )
        return dftag

    if isGF:
        dftag = (df.Define("ele_mask", "cleaningMask(Photon_electronIdx[goodPhotons],nElectron)")
                 .Define("vetoEle","{}".format(LOOSEelectrons))
                 .Define("vetoMu","{}".format(LOOSEmuons))
                 .Filter("(Sum(vetoEle)+Sum(vetoMu))==0", "no leptons")
                 #                 .Define("trigger","{}".format(TRIGGER))
                 #                 .Filter("trigger>0", "pass triggers")
                 .Filter("DeepMETResolutionTune_pt<75","DeepMETResolutionTune_pt<75")
                 .Define("goodJets","{}".format(GOODJETS))
                 .Define("nGoodJets","Sum(goodJets)*1.0f")
                 .Filter("Sum(goodJets)<2 or (Sum(goodJets)>=2 and abs(Jet_eta[goodJets][0] - Jet_eta[goodJets][1])<3 )","0 or 1 jets (pt25, |eta|<4.7) or >=2 with dEta<3")
                 .Define("SoftActivityJetNjets5F","SoftActivityJetNjets5*1.0f")
                 )
        return dftag

def dfGammaMeson(df,PDType,isData):

    TRIGGER=pickTRG(TRIGGERS,year,PDType,isVBF,isW,isZ,(isZinv or isVBFlow or isGF))

    GOODphotons = ""
    if(isGF): GOODphotons = "({0} or {1}) and Photon_pt>38 and Photon_electronVeto".format(BARRELphotons,ENDCAPphotons) #90-80
    if(isVBF): GOODphotons = "{} and Photon_pt>75 and Photon_electronVeto".format(BARRELphotons)  #90
    if(isVBFlow): GOODphotons = "({0} or {1}) and Photon_pt>38 and Photon_pt<75 and Photon_electronVeto".format(BARRELphotons,ENDCAPphotons) #80-80
    if(isZinv): GOODphotons = "({0} or {1}) and Photon_pt>38 and Photon_electronVeto".format(BARRELphotons,ENDCAPphotons) #80-80
    if(isW or isZ): GOODphotons = "({0} or {1}) and (Photon_pixelSeed == false)".format(BARRELphotons,ENDCAPphotons) #90-80
    print("PHOTONS = ", GOODphotons)

    dfOBJ = (df.Filter("nPhoton>0 and PV_npvsGood>0","photon from nano >0 and PV_npvsGood > 0")
             .Define("triggerAna","{}".format(TRIGGER))
             .Filter("triggerAna>0", "pass triggers")
             .Define("goodPhotons", "{}".format(GOODphotons))
             .Define("nGoodPhotons","Sum(goodPhotons)*1.0f")
             .Filter("Sum(goodPhotons)>0", "At least one good Photon")
             .Define("goodPhotons_pt", "Photon_pt[goodPhotons]")
             .Define("goodPhotons_eta", "Photon_eta[goodPhotons]")
             .Define("goodPhotons_phi", "Photon_phi[goodPhotons]")
             .Define("goodPhotons_pfRelIso03_all", "Photon_pfRelIso03_all[goodPhotons]")
             .Define("goodPhotons_hoe", "Photon_hoe[goodPhotons]")
             .Define("goodPhotons_r9", "Photon_r9[goodPhotons]")
             .Define("goodPhotons_sieie", "Photon_sieie[goodPhotons]")
             .Define("goodPhotons_mvaID", "Photon_mvaID[goodPhotons]")
             .Define("goodPhotons_energyErr", "Photon_energyErr[goodPhotons]")
             .Define("jet_mask", "cleaningMask(Photon_jetIdx[goodPhotons],nJet)")
             )
    return dfOBJ

def dfHiggsCand(df):

    GOODPHI = ""
    if(isVBF): GOODPHI = "{}".format(getMesonFromJson(mesons, "isVBF", "isPhiCat"))
    if(isVBFlow): GOODPHI = "{}".format(getMesonFromJson(mesons, "isVBFlow" , "isPhiCat"))
    if(isZinv or isGF): GOODPHI = "{}".format(getMesonFromJson(mesons, "isZinv", "isPhiCat"))
    if(isW or isZ): GOODPHI = "{}".format(getMesonFromJson(mesons, "VH", "isPhiCat"))

    GOODRHO = ""
    if(isVBF): GOODRHO = "{}".format(getMesonFromJson(mesons, "isVBF", "isRhoCat"))
    if(isVBFlow): GOODRHO = "{}".format(getMesonFromJson(mesons, "isVBFlow" , "isRhoCat"))
    if(isZinv or isGF): GOODRHO = "{}".format(getMesonFromJson(mesons, "isZinv", "isRhoCat"))
    if(isW or isZ): GOODRHO = "{}".format(getMesonFromJson(mesons, "VH", "isRhoCat"))

    if(isPhiCat=="true"):

        dfbase = (df.Filter("nphi>0").Define("goodMeson","({}".format(GOODPHI)+" && {}".format(isPhiCat)+")")
                  .Filter("Sum(goodMeson)>0", "one good Phi (ptPhi, validfit, ptTracks)")
                  .Define("goodMeson_pt", "phi_kin_pt[goodMeson]")
                  .Define("goodMeson_eta", "phi_kin_eta[goodMeson]")
                  .Define("goodMeson_phi", "phi_kin_phi[goodMeson]")
                  .Define("goodMeson_mass", "phi_kin_mass[goodMeson]")
                  .Define("goodMeson_iso", "phi_iso[goodMeson]")
                  .Define("goodMeson_vtx_chi2dof", "phi_kin_vtx_chi2dof[goodMeson]")
                  .Define("goodMeson_vtx_prob", "phi_kin_vtx_prob[goodMeson]")
                  .Define("goodMeson_sipPV", "phi_kin_sipPV[goodMeson]")
#                  .Define("goodMeson_bestVtx_idx", "phi_bestVtx_idx[goodMeson]")
#                  .Define("goodMeson_bestVtx_X", "phi_bestVtx_X[goodMeson]")
#                  .Define("goodMeson_bestVtx_Y", "phi_bestVtx_Y[goodMeson]")
#                  .Define("goodMeson_bestVtx_Z", "phi_bestVtx_Z[goodMeson]")
                  .Define("goodMeson_massErr", "phi_kin_massErr[goodMeson]")
                  .Define("goodMeson_trk1_pt", "phi_trk1_pt[goodMeson]")
                  .Define("goodMeson_trk2_pt", "phi_trk2_pt[goodMeson]")
                  .Define("goodMeson_trk1_eta", "phi_trk1_eta[goodMeson]")
                  .Define("goodMeson_trk2_eta", "phi_trk2_eta[goodMeson]")
                  .Define("goodMeson_DR","DeltaR(phi_trk1_eta[goodMeson],phi_trk2_eta[goodMeson],phi_trk1_phi[goodMeson],phi_trk2_phi[goodMeson])")
                  .Define("wrongMeson","({}".format(GOODRHO)+")")
                  .Define("wrongMeson_pt","Sum(wrongMeson) > 0 ? rho_kin_pt[wrongMeson]: ROOT::VecOps::RVec<float>(0.f)")
                  )

    if(isRhoCat=="true"):

        dfbase = (df.Filter("nrho>0").Define("goodMeson","({}".format(GOODRHO)+" && {}".format(isRhoCat)+")")
                  .Filter("Sum(goodMeson)>0", "one good Rho (ptPhi, validfit, ptTracks)")
                  .Define("goodMeson_pt", "rho_kin_pt[goodMeson]")
                  .Define("goodMeson_eta", "rho_kin_eta[goodMeson]")
                  .Define("goodMeson_phi", "rho_kin_phi[goodMeson]")
                  .Define("goodMeson_iso", "rho_iso[goodMeson]")
                  .Define("goodMeson_mass", "rho_kin_mass[goodMeson]")
                  .Define("goodMeson_vtx_chi2dof", "rho_kin_vtx_chi2dof[goodMeson]")
                  .Define("goodMeson_vtx_prob", "rho_kin_vtx_prob[goodMeson]")
                  .Define("goodMeson_sipPV", "rho_kin_sipPV[goodMeson]")
#                  .Define("goodMeson_bestVtx_idx", "rho_bestVtx_idx[goodMeson]")
#                  .Define("goodMeson_bestVtx_X", "rho_bestVtx_X[goodMeson]")
#                  .Define("goodMeson_bestVtx_Y", "rho_bestVtx_Y[goodMeson]")
#                  .Define("goodMeson_bestVtx_Z", "rho_bestVtx_Z[goodMeson]")
                  .Define("goodMeson_massErr", "rho_kin_massErr[goodMeson]")
                  .Define("goodMeson_trk1_pt", "rho_trk1_pt[goodMeson]")
                  .Define("goodMeson_trk2_pt", "rho_trk2_pt[goodMeson]")
                  .Define("goodMeson_trk1_eta", "rho_trk1_eta[goodMeson]")
                  .Define("goodMeson_trk2_eta", "rho_trk2_eta[goodMeson]")
                  .Define("goodMeson_DR","DeltaR(rho_trk1_eta[goodMeson],rho_trk2_eta[goodMeson],rho_trk1_phi[goodMeson],rho_trk2_phi[goodMeson])")
                  .Define("wrongMeson","({}".format(GOODPHI)+")")
                  .Define("wrongMeson_pt","Sum(wrongMeson) > 0 ? phi_kin_pt[wrongMeson]: ROOT::VecOps::RVec<float>(0.f)")
                  )

    dfFinal = (dfbase.Define("index_pair","HiggsCandFromRECO(goodMeson_pt,goodMeson_eta,goodMeson_phi,goodMeson_mass,wrongMeson_pt,goodPhotons_pt,goodPhotons_pt,goodPhotons_eta,goodPhotons_phi)").Filter("index_pair[0]!= -1", "at least a good meson candidate")
               .Define("jet_mask2", "cleaningJetFromMeson(Jet_eta, Jet_phi, goodMeson_eta[index_pair[0]], goodMeson_phi[index_pair[0]])")
               .Define("meson_pt", "(index_pair[0]!= -1) ? goodMeson_pt[index_pair[0]]: 0.f")
               .Define("photon_pt", "(index_pair[1]!= -1) ? goodPhotons_pt[index_pair[1]]: 0.f")
               .Define("photon_dEsigmaUp", "(1.f+Photon_dEsigmaUp[goodPhotons[index_pair[1]]])")
               .Define("photon_dEsigmaDown", "(1.f+Photon_dEsigmaDown[goodPhotons[index_pair[1]]])")
               .Vary("photon_pt", "ROOT::RVecF{photon_pt*photon_dEsigmaDown,photon_pt*photon_dEsigmaUp}", variationTags=["down","up"], variationName = "PhotonSYST")
	       .Define("HCandMass", "Minv2(goodMeson_pt[index_pair[0]],goodMeson_eta[index_pair[0]],goodMeson_phi[index_pair[0]],goodMeson_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).first")
               .Define("HCandPT",   "Minv2(goodMeson_pt[index_pair[0]],goodMeson_eta[index_pair[0]],goodMeson_phi[index_pair[0]],goodMeson_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).second")
               .Define("dPhiGammaMesonCand","abs(deltaPhi(goodPhotons_phi[index_pair[1]], goodMeson_phi[index_pair[0]]))")
               .Define("dEtaGammaMesonCand","abs(goodPhotons_eta[index_pair[1]] - goodMeson_eta[index_pair[0]])")
               .Define("sigmaHCandMass_Rel2","(goodPhotons_energyErr[index_pair[1]]*goodPhotons_energyErr[index_pair[1]])/(goodPhotons_pt[index_pair[1]]*goodPhotons_pt[index_pair[1]]) + (goodMeson_massErr[index_pair[0]]*goodMeson_massErr[index_pair[0]])/(goodMeson_mass[index_pair[0]]*goodMeson_mass[index_pair[0]])")
               )
    return dfFinal

def analysis(df,year,mc,sumw,isData,PDType):

    lumi = 1.
    weight = "{0}".format(1.)
    if mc>0: weight = "{0}*genWeight*{1}".format(lumi,sumw)

    lumiIntegrated = 1.
    print('isData = ',isData)
    if (isData == "false"):
        if(isVBF and year == 2018): lumiIntegrated = lumis['2018']
        if(isVBF and year == 2017): lumiIntegrated = lumis['12017']
        if(isVBF and year == 12016): lumiIntegrated = lumis['12016']
        if((isVBFlow or isGF or isZinv) and year == 2018): lumiIntegrated = lumis['12018']
        print('lumiIntegrated=',lumiIntegrated, ' year=',year)

    dfOBJ= dfGammaMeson(df,PDType,isData)
    dfbase = dfHiggsCand(dfOBJ)
    dfcandtag = selectionTAG(dfbase)

    MVAweights = ""
    if(isGF): MVAweights = "{}".format(getMVAFromJson(MVA, "isGF" , sys.argv[2] ))
    if(isVBF): MVAweights = "{}".format(getMVAFromJson(MVA, "isVBF" , sys.argv[2] ))
    if(isVBFlow): MVAweights = "{}".format(getMVAFromJson(MVA, "isVBFlow" , sys.argv[2] ))
    if(isZinv): MVAweights = "{}".format(getMVAFromJson(MVA, "isZinv" , sys.argv[2] ))
    print(MVAweights)

    NVar = "0"
    if(isGF): NVar = "10"
    if(isVBF): NVar = "13"
    if(isVBFlow): NVar = "17"
    if(isZinv): NVar = "11"

    s ='''
    TMVA::Experimental::RReader model("{0}");
    computeModel = TMVA::Experimental::Compute<{1}, float>(model);
    '''

    print(s.format(MVAweights,NVar))
    if doMVA : ROOT.gInterpreter.ProcessLine(s.format(MVAweights,NVar))

    if doMVA : variables = ROOT.model.GetVariableNames()
    if doMVA : print(variables)

    dfFINAL = (dfcandtag.Define("w","{}".format(weight))
               .Define("mc","{}".format(mc))
               .Define("isData","{}".format(isData))
               .Define("w","{}".format(weight))
               .Define("lumiIntegrated","{}".format(lumiIntegrated))
               .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
               .Filter("PV_npvsGood>0","one good PV")
               ## extra variables for MVA-SEPT7 GF-VBF-VBFlow below
               .Define("HCandPT__div_sqrtHCandMass", "(HCandMass>0) ? HCandPT/sqrt(HCandMass): 0.f")
               .Define("HCandPT__div_HCandMass", "(HCandMass>0) ? HCandPT/HCandMass: 0.f")
               .Define("photon_pt__div_HCandPT", "(index_pair[1]!= -1) ? goodPhotons_pt[index_pair[1]]/HCandPT: 0.f")
               .Define("photon_eta","(index_pair[1]!= -1) ? goodPhotons_eta[index_pair[1]]: 0.f")
               .Define("meson_DR__times_sqrtHCandMass", "(index_pair[0]!= -1) ? goodMeson_DR[index_pair[0]]*sqrt(HCandMass): 0.f")
               .Define("meson_pt__div_HCandPT", "(index_pair[0]!= -1) ? goodMeson_pt[index_pair[0]]/HCandPT: 0.f")
               .Define("meson_pt__div_sqrtHCandMass", "(index_pair[0]!= -1) ? goodMeson_pt[index_pair[0]]/sqrt(HCandMass): 0.f")
               ##
               .Define("meson_mass","(index_pair[0]!= -1) ? goodMeson_mass[index_pair[0]]: 0.f")
               .Define("meson_iso","(index_pair[0]!= -1) ? goodMeson_iso[index_pair[0]]: 0.f")
               .Define("meson_trk1_eta","(index_pair[0]!= -1) ? goodMeson_trk1_eta[index_pair[0]]: 0.f")
               .Define("meson_vtx_prob","(index_pair[0]!= -1) ? goodMeson_vtx_prob[index_pair[0]]: 0.f")
               #
               .Define("dPhiGammaMesonCand__div_sqrtHCandMass","(HCandMass>0) ? dPhiGammaMesonCand/sqrt(HCandMass): 0.f")
               .Define("dEtaGammaMesonCand__div_HCandMass","(HCandMass>0) ? dEtaGammaMesonCand/HCandMass: 0.f")
               #
               .Define("MVAdisc", ROOT.computeModel, ROOT.model.GetVariableNames())
               .Define("eventF","event*1.0f")
               )

    branchList = ROOT.vector('string')()
    for branchName in [
            "HCandMass",
            "HCandPT",
            "index_pair",
            "meson_pt",
            "photon_pt",
            "sigmaHCandMass_Rel2",
            #
            "goodPhotons_pt",
            "goodPhotons_eta",
            "goodPhotons_pfRelIso03_all",
            "goodPhotons_hoe",
            "goodPhotons_r9",
            "goodPhotons_sieie",
            "goodPhotons_mvaID",
            "goodPhotons_energyErr",
            #
            "trigger",
            "SoftActivityJetNjets5",
            "DeepMETResolutionTune_pt",
            "dPhiGammaMesonCand",
            "dEtaGammaMesonCand",
            #
            "w",
            "mc",
            "PV_npvsGood",
            "run",
            "luminosityBlock",
            "event",
            "lumiIntegrated",
    ]:
        branchList.push_back(branchName)

    for branchName in [
            "goodMeson",
            "goodMeson_DR",
            "goodMeson_mass",
            "goodMeson_massErr",
            "goodMeson_pt",
            "goodMeson_iso",
            "goodMeson_trk1_pt",
            "goodMeson_trk2_pt",
            "goodMeson_trk1_eta",
            "goodMeson_trk2_eta",
            "goodMeson_vtx_chi2dof",
            "goodMeson_vtx_prob",
            "goodMeson_sipPV",
#            "goodMeson_bestVtx_idx",
#            "goodMeson_bestVtx_X",
#            "goodMeson_bestVtx_Y",
#            "goodMeson_bestVtx_Z",
    ]:
        branchList.push_back(branchName)

    if isZ or isW:
        for branchName in [
                "V_mass",
                "isMuorEle",
        ]:
            branchList.push_back(branchName)

    if isW:
        for branchName in [
                "dPhiGammaMET",
                "dPhiMesonMET",
        ]:
            branchList.push_back(branchName)

    if isZinv:
        for branchName in [
                "dPhiGammaMET",
                "dPhiMesonMET",
                "ptRatioMEThiggs",
        ]:
            branchList.push_back(branchName)

    if (isGF or isVBF or isVBFlow) and doMVA:
        for branchName in [
                "MVAdisc",
        ]:
            branchList.push_back(branchName)

    if isGF or isZinv:
        for branchName in [
                "nGoodJets",
        ]:
            branchList.push_back(branchName)

    if isVBF or isVBFlow:
        for branchName in [
                "mJJ",
                "nGoodJets",
                "dEtaJJ",
                "dPhiJJ",
                "Y1Y2",
                "deltaJetMeson",
                "deltaJetPhoton",
                "jet1Pt",
                "jet2Pt",
                "jet1Eta",
                "jet2Eta",
                "zepVar",
                "detaHigJet1",
                "detaHigJet2"
        ]:
            branchList.push_back(branchName)

    outputFile = "outname_mc%d"%mc+".root"
    catM = ""
    if(isPhiCat=="true"): catM = "PhiCat"
    if(isRhoCat=="true"): catM = "RhoCat"
    catTag = ""
    if isZ: catTag = "Zcat"
    if isZinv: catTag = "Zinvcat"
    if isW: catTag = "Wcat"
    if isVBF: catTag = "VBFcat"
    if isVBFlow: catTag = "VBFcatlow"
    if isGF: catTag = "GFcat"
    outputFile = "MARCH30/{0}/outname_mc{1}_{2}_{3}_{0}.root".format(year,mc,catTag,catM,year)
    print(outputFile)

    if True:
        snapshot_tdf = dfFINAL.Snapshot("events", outputFile, branchList)
        print("snapshot_tdf DONE")
        print("*** SUMMARY :")
        print(outputFile)

    if False:
        print("---------------- SUMMARY -------------")
        ## this doens't work with the negative weights
        report = dfFINAL.Report()
        report.Print()


    if doPlot:
        hists = {
            #        "Z_mass":     {"name":"Z_mass","title":"Di Muon mass; m_{#mu^{+}#mu^{-}} (GeV);N_{Events}","bin":500,"xmin":70,"xmax":120},
#            "V_mass":     {"name":"V_mass","title":"transverse mass; m_{T}(#mu^{+} MET} (GeV);N_{Events}","bin":80,"xmin":40,"xmax":120},
            "HCandMass":  {"name":"HCandMass","title":"H mass;m_{k^{+}k^{-}#gamma} (GeV);N_{Events}","bin":500,"xmin":100,"xmax":150},
#            "phi_num":    {"name":"nphi","title":"Phi N;N {k^{+}k^{-}} (GeV);N_{Events}","bin":10,"xmin":0.,"xmax":10.},
#            "Phi_mass":   {"name":"phi_kin_mass","title":"Phi mass;m_{k^{+}k^{-}} (GeV);N_{Events}","bin":200,"xmin":0.95,"xmax":1.15},
#            "Phi_pt":     {"name":"phi_kin_pt","title":"Phi pt ;p^{T}_{k^{+}k^{-}} (GeV);N_{Events}","bin":1000,"xmin":0.25,"xmax":50.25},
#            "Phi_gen_mass":   {"name":"phi_gen_mass","title":"Phi gen mass;m_{k^{+}k^{-}} (GeV);N_{Events}","bin":100,"xmin":0.,"xmax":10.},
#            "Phi_mass_err":   {"name":"phi_kin_massErr","title":"Phi mass error;m_{k^{+}k^{-}} (GeV);N_{Events}","bin":100,"xmin":0.,"xmax":0.5},
#            "Phi_kin_vtx_chi2dof":   {"name":"phi_kin_vtx_chi2dof","title":"Phi vtx_chi2dof;m_{k^{+}k^{-}} (GeV);N_{Events}","bin":100,"xmin":0.,"xmax":5.0},
#        }

        outputFileHisto = "OCT12/{0}/histoname_mc{1}_{2}_{3}_{0}.root".format(year,mc,catTag,catM,year)
        myfile = ROOT.TFile(outputFileHisto,"RECREATE")

        for h in hists:
            model = (hists[h]["name"], hists[h]["title"], hists[h]["bin"], hists[h]["xmin"], hists[h]["xmax"])
            h = dfFINAL.Histo1D(model, hists[h]["name"],"w")

            hx = ROOT.RDF.Experimental.VariationsFor(h);
            hx["PhotonSYST:down"].SetName("HCandMass:PhotonSYST:down");
            hx["PhotonSYST:down"].Write();
            hx["PhotonSYST:down"].SetName("HCandMass:PhotonSYST:up");
            hx["PhotonSYST:up"].Write();

        myfile.Close()
        myfile.Write()

def readMCSample(sampleNOW):

    files = getMClist(sampleNOW)
    print(len(files))
    df = ROOT.RDataFrame("Events", files)

    w = computeWeigths(df, files, sampleNOW, True)
    analysis(df,sampleNOW,w,"false")


def readDataSample(year,type):

    files = getDATAlist(year,type)

    df = ROOT.RDataFrame("Events", files)

    w = computeWeigths(df, files, sampleNOW, False)

    analysis(df,type,w,"true")

def readDataSkims(datasetNumber,year,category):

    print("enum",datasetNumber)
    print("year",year)
    print("cat",category)
    if (category=="isZtag" or category=="isWtag"):
        pair = getSkims(datasetNumber,year,"VH")
    elif category=="isVBFtag":
        pair = getSkims(datasetNumber,year,"VBF")
    if (category=="isZinvtag" or category=="isVBFtaglow" or category=="isGFtag"):
        pair = getSkims(datasetNumber,year,"Zinv")

    files = pair[0]
    PDType = pair[1]
    print(len(files))
    print(PDType)

    df = ROOT.RDataFrame("Events", files)
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    analysis(df,year,datasetNumber,1.,"true",PDType)
    print("***ANALYSIS DONE ***")

def runTest():

    df = ROOT.RDataFrame("Events", "root://eoscms.cern.ch//eos/cms//store/group/phys_higgs/HiggsExo/dalfonso/Hrare/D01/vbf-hphigamma-powheg/NANOAOD_01/step7_VBS_Phigamma_8.root")

    w=1.
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    sampleNOW=-1
    analysis(df,-1,w,"false")

   
if __name__ == "__main__":

    runTest()
#    to run: python3 -i VGammaMeson_cat.py isVBFtag isPhiCat 12 2018
#    print(int(sys.argv[3]))

    if ( sys.argv[1]=="isVBFtag" and int(sys.argv[3]) in [ -31, -32, -33, -34, -76, -81, -82, -83, -84, -85, -86]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims VBF

    elif ( (sys.argv[1]=="isZinvtag" or sys.argv[1]=="isVBFtaglow" or sys.argv[1]=="isGFtag") and int(sys.argv[3]) in [-62, -63, -64]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims Tau

    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-1, -2, -3, -4, -5, -6, -7, -8]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims singleMu
    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-11, -12, -13, -14, -15, -16, -17, -18]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims doubleMu
    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-21, -22, -23, -24, -25, -26, -27, -28]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims MuEG
    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-31, -32, -33, -34, -35, -36, -37, -38]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims EG
    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-41, -42, -43, -44, -45, -46, -47, -48]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims DoubleEG
    elif ( (sys.argv[1]=="isWtag" or sys.argv[1]=="isZtag") and int(sys.argv[3]) in [-51, -52, -53, -54, -55, -56, -57, -58]):
        readDataSkims(int(sys.argv[3]),int(sys.argv[4]),sys.argv[1]) # skims SingleElectron
    elif(int(sys.argv[3]) < 0):
        readDataSample(int(sys.argv[4]),int(sys.argv[3]) )  # DATA
    else: readMCSample(int(sys.argv[4]),int(sys.argv[3])) # to switch sample
