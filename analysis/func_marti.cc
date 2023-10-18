#ifndef FUNCMARTI_H
#define FUNCMARTI_H


#include "TROOT.h"
#include "TFile.h"
#include "TH2.h"
#include "TH3.h"
#include "TF1.h"
#include "TH2Poly.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TSpline.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "TEfficiency.h"
#include "TVector2.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <cstdlib> //as stdlib.h      
#include <cstdio>
#include <cmath>
#include <array>
#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
#include <algorithm>
#include <limits>
#include <map>
#include <ROOT/RVec.hxx>
#include <ROOT/RDataFrame.hxx>


using Vec_b = ROOT::VecOps::RVec<bool>;
using Vec_d = ROOT::VecOps::RVec<double>;
using Vec_f = ROOT::VecOps::RVec<float>;
using Vec_i = ROOT::VecOps::RVec<int>;
using Vec_ui = ROOT::VecOps::RVec<unsigned int>;


using stdVec_i = std::vector<int>;
using stdVec_b = std::vector<bool>;
using stdVec_f = std::vector<float>;

typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > PtEtaPhiMVector;

const float pi0_mass = 0.1349766;
const float pi1_mass = 0.13957018;
const float D0_mass = 1.86484;
const float D0Star_mass = 2.00685;
const float phi_mass = 1.019461;
const float omega_mass = 0.78266;

const int pi0_id = 111;
const int pi1_id = 211;
const int D0_id = 421;


float getMass(int idParticle, float defaultMass){
	if (idParticle == pi0_id){
		return pi0_mass;
	} else if (idParticle == pi1_id || idParticle == -pi1_id){
		return pi1_mass;
	} else if (idParticle == D0_id){
		return D0_mass;
	} else{
		return defaultMass;
	}
}


Vec_f getPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother, int idGreatGrandMother){
	/*Get PtEtaPhiM with idParticle, idMother, idGrandMother and idGreatGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	Vec_i indexGreatGrandMother = {};
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		if(genPart_pdgId[i] == idGreatGrandMother){
            indexGreatGrandMother.push_back(i);
        }
		else if(std::find(indexGreatGrandMother.begin(), indexGreatGrandMother.end(), genPart_genPartIdxMother[i]) != indexGreatGrandMother.end()){
        	if(genPart_pdgId[i] == idGrandMother){
            	indexGrandMother.push_back(i);
        	}
		}
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
			if(genPart_pdgId[i] == idGrandMother){//this is for when the grandmother changes state, grandmother has 2 indexes
            	indexGrandMother.push_back(i);
        	}
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
        	if(genPart_pdgId[i] == idParticle){
            	selection.push_back(genPart_pt[i]);
				selection.push_back(genPart_eta[i]);
				selection.push_back(genPart_phi[i]);
				selection.push_back(getMass(idParticle, genPart_mass[i]));
				return selection;
        	}
		}
    }
    return selection;
}


Vec_f getPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother){
	/*Get PtEtaPhiM with idParticle, idMother and idGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idGrandMother){
            indexGrandMother.push_back(i);
        }
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
        	if(genPart_pdgId[i] == idParticle){
            	selection.push_back(genPart_pt[i]);
				selection.push_back(genPart_eta[i]);
				selection.push_back(genPart_phi[i]);
				selection.push_back(getMass(idParticle, genPart_mass[i]));
				return selection;
        	}
		}
    }
    return selection;
}


Vec_f getPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother){
	/*Get PtEtaPhiM with idParticle and idMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother){
            indexMother.push_back(i);
        }
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idParticle){
            	selection.push_back(genPart_pt[i]);
				selection.push_back(genPart_eta[i]);
				selection.push_back(genPart_phi[i]);
				selection.push_back(getMass(idParticle, genPart_mass[i]));
				return selection;
        	}
		}
    }
    return selection;
}


Vec_f getPt(Vec_f& genPart_pt, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother, int idGreatGrandMother){
	/*Get Pt with idParticle, idMother, idGrandMother and idGreatGrandMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_pt, genPart_pt, genPart_pt, genPart_pt, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother, idGrandMother, idGreatGrandMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[0]};
	}
	return out;
}


Vec_f getPt(Vec_f& genPart_pt, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother){
	/*Get Pt with idParticle, idMother and idGrandMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_pt, genPart_pt, genPart_pt, genPart_pt, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother, idGrandMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[0]};
	}
	return out;
}


Vec_f getPt(Vec_f& genPart_pt, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother){
	/*Get Pt with idParticle and idMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_pt, genPart_pt, genPart_pt, genPart_pt, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[0]};
	}
	return out;
}


Vec_f getEtaPhi(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother, int idGreatGrandMother){
	/*Get EtaPhi with idParticle, idMother, idGrandMother and idGreatGrandMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_phi, genPart_eta, genPart_phi, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother, idGrandMother, idGreatGrandMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[1], ptEtaPhiM[2]};
	}
	return out;
}


Vec_f getEtaPhi(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother, int idGrandMother){
	/*Get EtaPhi with idParticle, idMother and idGrandMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_phi, genPart_eta, genPart_phi, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother, idGrandMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[1], ptEtaPhiM[2]};
	}
	return out;
}


Vec_f getEtaPhi(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle, int idMother){
	/*Get EtaPhi with idParticle and idMother*/
	Vec_f ptEtaPhiM = getPtEtaPhiM(genPart_phi, genPart_eta, genPart_phi, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle, idMother);
	Vec_f out = {};
	if (ptEtaPhiM.size() != 0){
		out = {ptEtaPhiM[1], ptEtaPhiM[2]};
	}
	return out;
}


Vec_f getDR(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idMother1, int idParticle2, int idMother2){
	/*Get DR with idParticle1, idMother1, idParticle2 and idMother2*/
    Vec_f selection = {};
	Vec_f etaPhi1 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle1, idMother1);
	Vec_f etaPhi2 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle2, idMother2);

	if(etaPhi1.size() == 2 && etaPhi2.size() == 2){
        selection.push_back(ROOT::VecOps::DeltaR(etaPhi1[0], etaPhi2[0], etaPhi1[1], etaPhi2[1]));
	}

    return selection;
}


Vec_f getDR(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idMother1, int idGrandMother1, int idParticle2, int idMother2){
	/*Get DR with idParticle1, idMother1, idGrandMother1, idParticle2 and idMother2*/
	Vec_f selection = {};
	Vec_f etaPhi1 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle1, idMother1, idGrandMother1);
	Vec_f etaPhi2 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle2, idMother2);

	if(etaPhi1.size() == 2 && etaPhi2.size() == 2){
        selection.push_back(ROOT::VecOps::DeltaR(etaPhi1[0], etaPhi2[0], etaPhi1[1], etaPhi2[1]));
	}

    return selection;
}


Vec_f getDR(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idMother1, int idGrandMother1, int idParticle2, int idMother2, int idGrandMother2){
	/*Get DR with idParticle1, idMother1, idGrandMother1, idParticle2, idMother2 and idGrandMother2*/
	Vec_f selection = {};
	Vec_f etaPhi1 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle1, idMother1, idGrandMother1);
	Vec_f etaPhi2 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle2, idMother2, idGrandMother2);

	if(etaPhi1.size() == 2 && etaPhi2.size() == 2){
        selection.push_back(ROOT::VecOps::DeltaR(etaPhi1[0], etaPhi2[0], etaPhi1[1], etaPhi2[1]));
	}

    return selection;
}


Vec_f getDR(Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idMother1, int idGrandMother1, int idGreatGrandMother1, int idParticle2, int idMother2, int idGrandMother2, int idGreatGrandMother2){
	/*Get DR with idParticle1, idMother1, idGrandMother1, idGreatGrandMother1, idParticle2, idMother2, idGrandMother2 and idGreatGrandMother2*/
	Vec_f selection = {};
	Vec_f etaPhi1 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle1, idMother1, idGrandMother1, idGreatGrandMother1);
	Vec_f etaPhi2 = getEtaPhi(genPart_eta, genPart_phi, genPart_pdgId, genPart_genPartIdxMother, idParticle2, idMother2, idGrandMother2, idGreatGrandMother2);

	if(etaPhi1.size() == 2 && etaPhi2.size() == 2){
        selection.push_back(ROOT::VecOps::DeltaR(etaPhi1[0], etaPhi2[0], etaPhi1[1], etaPhi2[1]));
	}

    return selection;
}


Vec_f get2BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idMother, int idGrandMother, int idGreatGrandMother){
	/*Get PtEtaPhiM with idParticle, idMother and idGrandMother, idGreatGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	Vec_i indexGreatGrandMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float phi1 = 0;
    float phi2 = 0;
    float mass1 = 0;
	float mass2 = 0;
    bool particle1 = false;
    bool particle2 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		if(genPart_pdgId[i] == idGreatGrandMother){
            indexGreatGrandMother.push_back(i);
        }
		else if(std::find(indexGreatGrandMother.begin(), indexGreatGrandMother.end(), genPart_genPartIdxMother[i]) != indexGreatGrandMother.end()){
        	if(genPart_pdgId[i] == idGrandMother){
            	indexGrandMother.push_back(i);
        	}
		}
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
			if(genPart_pdgId[i] == idGrandMother){//this is for when the grandmother changes state, grandmother has 2 indexes
            	indexGrandMother.push_back(i);
        	}
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
    }
	if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_2Body = (p_part1 + p_part2);
		selection = {p_2Body.pt(), p_2Body.Eta(), p_2Body.Phi(), p_2Body.M()};
    }
    return selection;
}


Vec_f get2BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idMother, int idGrandMother){
	/*Get 2Body PtEtaPhiM with idParticle1,2, idMother and idGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float phi1 = 0;
    float phi2 = 0;
    float mass1 = 0;
	float mass2 = 0;
    bool particle1 = false;
    bool particle2 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idGrandMother){
            indexGrandMother.push_back(i);
        }
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
    }
	if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_2Body = (p_part1 + p_part2);
		if (abs(p_2Body.M()) < 0.01){
			selection = {p_2Body.pt(), p_2Body.Eta(), p_2Body.Phi(), std::sqrt(-(p_2Body.X()*p_2Body.X() + p_2Body.Y()*p_2Body.Y() + p_2Body.Z()*p_2Body.Z()) + p_2Body.E()*p_2Body.E())};
		}else{
			selection = {p_2Body.pt(), p_2Body.Eta(), p_2Body.Phi(), p_2Body.M()};
		}
    }
    return selection;
}


Vec_f get2BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idMother){
	/*Get 2Body PtEtaPhiM with idParticle1,2, idMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float phi1 = 0;
    float phi2 = 0;
    float mass1 = 0;
	float mass2 = 0;
    bool particle1 = false;
    bool particle2 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother){
            indexMother.push_back(i);
        }
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
    }
	if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_2Body = (p_part1 + p_part2);
		selection = {p_2Body.pt(), p_2Body.Eta(), p_2Body.Phi(), p_2Body.M()};
    }
    return selection;
}


Vec_f get3BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idParticle3, int idMother, int idGrandMother, int idGreatGrandMother){
	/*Get 3Body PtEtaPhiM with idParticle1,2,3, idMother and idGrandMother, idGreatGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	Vec_i indexGreatGrandMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		if(genPart_pdgId[i] == idGreatGrandMother){
            indexGreatGrandMother.push_back(i);
        }
        else if(std::find(indexGreatGrandMother.begin(), indexGreatGrandMother.end(), genPart_genPartIdxMother[i]) != indexGreatGrandMother.end()){
        	if(genPart_pdgId[i] == idGrandMother){
            	indexGrandMother.push_back(i);
        	}
		}
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
			if(genPart_pdgId[i] == idGrandMother){//this is for when the grandmother changes state, grandmother has 2 indexes
            	indexGrandMother.push_back(i);
        	}
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}else if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(idParticle3, genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
	if(particle1 && particle2 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_3Body = (p_part1 + p_part2 + p_part3);
		selection = {p_3Body.pt(), p_3Body.Eta(), p_3Body.Phi(), p_3Body.M()};
    }
    return selection;
}


Vec_f get3BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idParticle3, int idMother, int idGrandMother){
	/*Get 3Body PtEtaPhiM with idParticle1,2,3, idMother and idGrandMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idGrandMother){
            indexGrandMother.push_back(i);
        }
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idMother){//this is for when the mother changes state, mother has 2 indexes
            	indexMother.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}else if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(idParticle3, genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
	if(particle1 && particle2 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_3Body = (p_part1 + p_part2 + p_part3);
		selection = {p_3Body.pt(), p_3Body.Eta(), p_3Body.Phi(), p_3Body.M()};
    }
    return selection;
}


Vec_f get3BodyPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idParticle2, int idParticle3, int idMother){
	/*Get 2Body PtEtaPhiM with idParticle1,2,3, idMother*/
    Vec_f selection = {};
	Vec_i indexMother = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother){
            indexMother.push_back(i);
        }
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}else if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(idParticle3, genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
	if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_3Body = (p_part1 + p_part2 + p_part3);
		selection = {p_3Body.pt(), p_3Body.Eta(), p_3Body.Phi(), p_3Body.M()};
    }
    return selection;
}


Vec_f getD0StarPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother){
	/*This is for D*0: idParticle1 = 421, idMother1=423, idGrandMother1=25, idParticle3=111/22, idMother3=423, idGrandMother3=25*/
	int idParticle1 = 421;
	int idMother1 = 423;
	int idGrandMother1 = 25;
	int idParticle3a = 111;
	int idParticle3b = 22;
	int idMother3 = 423;
	int idGrandMother3 = 25;
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother3 = {};
	Vec_i indexGrandMother1 = {};
	Vec_i indexGrandMother3 = {};
	float pt1 = 0;
	float pt3 = 0;
	float eta1 = 0;
	float eta3 = 0;
	float phi1 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass3 = 0;
    bool particle1 = false;
	bool particle3 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1 (D0)
		if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
        	if(genPart_pdgId[i] == idMother1){//this is for when the mother changes state, mother has 2 indexes
            	indexMother1.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		//Particle 3 (pi0/photon)
		if(genPart_pdgId[i] == idGrandMother3){
            indexGrandMother3.push_back(i);
        }
		else if(std::find(indexGrandMother3.begin(), indexGrandMother3.end(), genPart_genPartIdxMother[i]) != indexGrandMother3.end()){
        	if(genPart_pdgId[i] == idMother3){
            	indexMother3.push_back(i);
        	}
		}
		else if(std::find(indexMother3.begin(), indexMother3.end(), genPart_genPartIdxMother[i]) != indexMother3.end()){
        	if(genPart_pdgId[i] == idMother3){//this is for when the mother changes state, mother has 2 indexes
            	indexMother3.push_back(i);
        	}
			if((genPart_pdgId[i] == idParticle3a || genPart_pdgId[i] == idParticle3b) && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(genPart_pdgId[i], genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
    if(particle1 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_D0Star = (p_part1 + p_part3);
		selection = {p_D0Star.pt(), p_D0Star.Eta(), p_D0Star.Phi(), p_D0Star.M()};
    }
    return selection;
}


Vec_f getHiggsPtEtaPhiM(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, int idParticle1, int idMother1, int idParticle2, int idMother2){
	/*Get Higgs variables with idParticle1, idMother1, idParticle2 and idMother2
	This is for phi: idParticle1 = 333, idMother1=25, idParticle2=22, idMother2=25*/
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother2 = {};
    float pt1 = 0;
	float pt2 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float phi1 = 0;
    float phi2 = 0;
    float mass1 = 0;
	float mass2 = 0;
    bool particle1 = false;
    bool particle2 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1
		if(genPart_pdgId[i] == idMother1){
            indexMother1.push_back(i);
        }
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		//Particle 2
		if(genPart_pdgId[i] == idMother2){
            indexMother2.push_back(i);
        }
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
			if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
    }
    if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_Higgs = (p_part1 + p_part2);
		selection = {p_Higgs.pt(), p_Higgs.Eta(), p_Higgs.Phi(), p_Higgs.M()};
    }
    return selection;
}


Vec_f getHiggsPtEtaPhiMD0Star(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother){
	/* Correct Higgs mass with all particles for D0*.
	This is for D*0: idParticle1 = 421, idMother1=423, idGrandMother1=25, idParticle2=22, idMother2=25, idParticle3=111/22, idMother3=423, idGrandMother3=25*/
	int idParticle1 = 421;
	int idMother1 = 423;
	int idGrandMother1 = 25;
	int idParticle2 = 22;
	int idMother2 = 25;
	int idParticle3a = 111;
	int idParticle3b = 22;
	int idMother3 = 423;
	int idGrandMother3 = 25;
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother2 = {};
	Vec_i indexMother3 = {};
	Vec_i indexGrandMother1 = {};
	Vec_i indexGrandMother3 = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1 (D0)
		if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
        	if(genPart_pdgId[i] == idMother1){//this is for when the mother changes state, mother has 2 indexes
            	indexMother1.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		//Particle 2 (photon)
		if(genPart_pdgId[i] == idMother2){
            indexMother2.push_back(i);
        }
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
			if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
		//Particle 3 (pi0/photon)
		if(genPart_pdgId[i] == idGrandMother3){
            indexGrandMother3.push_back(i);
        }
		else if(std::find(indexGrandMother3.begin(), indexGrandMother3.end(), genPart_genPartIdxMother[i]) != indexGrandMother3.end()){
        	if(genPart_pdgId[i] == idMother3){
            	indexMother3.push_back(i);
        	}
		}
		else if(std::find(indexMother3.begin(), indexMother3.end(), genPart_genPartIdxMother[i]) != indexMother3.end()){
        	if(genPart_pdgId[i] == idMother3){//this is for when the mother changes state, mother has 2 indexes
            	indexMother3.push_back(i);
        	}
			if((genPart_pdgId[i] == idParticle3a || genPart_pdgId[i] == idParticle3b) && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(genPart_pdgId[i], genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
    if(particle1 && particle2 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_Higgs = (p_part1 + p_part2 + p_part3);
		selection = {p_Higgs.pt(), p_Higgs.Eta(), p_Higgs.Phi(), p_Higgs.M()};
    }
    return selection;
}


Vec_f getHiggsPtEtaPhiMD0StarDitrack(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother){
	/* Missing pi0/photon Higgs mass for D0*.
	This is for D*0: idParticle1 = 421, idMother1=423, idGrandMother1=25, idParticle2=22, idMother2=25*/
	int idParticle1 = 421;
	int idMother1 = 423;
	int idGrandMother1 = 25;
	int idParticle2 = 22;
	int idMother2 = 25;
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother2 = {};
	Vec_i indexGrandMother1 = {};
    float pt1 = 0;
	float pt2 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float phi1 = 0;
    float phi2 = 0;
    float mass1 = 0;
	float mass2 = 0;
    bool particle1 = true;
    bool particle2 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1 with grandmother
		/*
		if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
        	if(genPart_pdgId[i] == idMother1){//this is for when the mother changes state, mother has 2 indexes
            	indexMother1.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		*/
		//Particle 2
		if(genPart_pdgId[i] == idMother2){
            indexMother2.push_back(i);
        }
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
			if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
    }
    if(particle1 && particle2){
		//Get D0 from 2body:
		Vec_f d0PtEtaPhiM = get2BodyPtEtaPhiM(genPart_pt, genPart_eta, genPart_phi, genPart_mass, genPart_pdgId, genPart_genPartIdxMother, -321, 211, 421, 423, 25);
		pt1 = d0PtEtaPhiM[0];
		eta1 = d0PtEtaPhiM[1];
		phi1 = d0PtEtaPhiM[2];
		mass1 = d0PtEtaPhiM[3];
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_Higgs = (p_part1 + p_part2);
		selection = {p_Higgs.pt(), p_Higgs.Eta(), p_Higgs.Phi(), p_Higgs.M()};
    }
    return selection;
}


Vec_f getHiggsPtEtaPhiMPhi3Ditrack(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother){
	/* Missing pi0 Higgs mass for Phi3.
	This is for Phi3: idParticle1 = 211, idMother1=333, idGrandMother1=25, idParticle2 = -211, idMother2=333, idGrandMother2=25, idParticle3=22, idMother3=25*/
	int idParticle1 = 211;
	int idMother1 = 333;
	int idGrandMother1 = 25;
	int idParticle2 = -211;
	int idMother2 = 333;
	int idGrandMother2 = 25;
	int idParticle3 = 22;
	int idMother3 = 25;
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother2 = {};
	Vec_i indexMother3 = {};
	Vec_i indexGrandMother1 = {};
	Vec_i indexGrandMother2 = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1 with grandmother
		if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
        	if(genPart_pdgId[i] == idMother1){//this is for when the mother changes state, mother has 2 indexes
            	indexMother1.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		//Particle 2 with grandmother
		if(genPart_pdgId[i] == idGrandMother2){
            indexGrandMother2.push_back(i);
        }
		else if(std::find(indexGrandMother2.begin(), indexGrandMother2.end(), genPart_genPartIdxMother[i]) != indexGrandMother2.end()){
        	if(genPart_pdgId[i] == idMother2){
            	indexMother2.push_back(i);
        	}
		}
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
        	if(genPart_pdgId[i] == idMother2){//this is for when the mother changes state, mother has 2 indexes
            	indexMother2.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
		//Particle 3
		if(genPart_pdgId[i] == idMother3){
            indexMother3.push_back(i);
        }
		else if(std::find(indexMother3.begin(), indexMother3.end(), genPart_genPartIdxMother[i]) != indexMother3.end()){
			if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(idParticle3, genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
    if(particle1 && particle2 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_Higgs = (p_part1 + p_part2 + p_part3);
		selection = {p_Higgs.pt(), p_Higgs.Eta(), p_Higgs.Phi(), p_Higgs.M()};
    }
    return selection;
}


Vec_f getHiggsPtEtaPhiMOmegaDitrack(Vec_f& genPart_pt, Vec_f& genPart_eta, Vec_f& genPart_phi, Vec_f& genPart_mass, Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother){
	/* Missing pi0 Higgs mass for Omega.
	This is for Omega: idParticle1 = 211, idMother1=223, idGrandMother1=25, idParticle2 = -211, idMother2=223, idGrandMother2=25, idParticle3=22, idMother3=25*/
	int idParticle1 = 211;
	int idMother1 = 223;
	int idGrandMother1 = 25;
	int idParticle2 = -211;
	int idMother2 = 223;
	int idGrandMother2 = 25;
	int idParticle3 = 22;
	int idMother3 = 25;
    Vec_f selection = {};
	Vec_i indexMother1 = {};
	Vec_i indexMother2 = {};
	Vec_i indexMother3 = {};
	Vec_i indexGrandMother1 = {};
	Vec_i indexGrandMother2 = {};
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
	float eta1 = 0;
    float eta2 = 0;
	float eta3 = 0;
	float phi1 = 0;
    float phi2 = 0;
	float phi3 = 0;
    float mass1 = 0;
	float mass2 = 0;
	float mass3 = 0;
    bool particle1 = false;
    bool particle2 = false;
	bool particle3 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
		//Particle 1 with grandmother
		if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
        	if(genPart_pdgId[i] == idMother1){//this is for when the mother changes state, mother has 2 indexes
            	indexMother1.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
				pt1 = genPart_pt[i];
				eta1 = genPart_eta[i];
            	phi1 = genPart_phi[i];
				mass1 = getMass(idParticle1, genPart_mass[i]);
            	particle1 = true;
        	}
		}
		//Particle 2 with grandmother
		if(genPart_pdgId[i] == idGrandMother2){
            indexGrandMother2.push_back(i);
        }
		else if(std::find(indexGrandMother2.begin(), indexGrandMother2.end(), genPart_genPartIdxMother[i]) != indexGrandMother2.end()){
        	if(genPart_pdgId[i] == idMother2){
            	indexMother2.push_back(i);
        	}
		}
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
        	if(genPart_pdgId[i] == idMother2){//this is for when the mother changes state, mother has 2 indexes
            	indexMother2.push_back(i);
        	}
			if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
				pt2 = genPart_pt[i];
				eta2 = genPart_eta[i];
            	phi2 = genPart_phi[i];
				mass2 = getMass(idParticle2, genPart_mass[i]);
            	particle2 = true;
        	}
		}
		//Particle 3
		if(genPart_pdgId[i] == idMother3){
            indexMother3.push_back(i);
        }
		else if(std::find(indexMother3.begin(), indexMother3.end(), genPart_genPartIdxMother[i]) != indexMother3.end()){
			if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
				pt3 = genPart_pt[i];
				eta3 = genPart_eta[i];
            	phi3 = genPart_phi[i];
				mass3 = getMass(idParticle3, genPart_mass[i]);
            	particle3 = true;
        	}
		}
    }
    if(particle1 && particle2 && particle3){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, mass2);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, mass3);
		PtEtaPhiMVector p_Higgs = (p_part1 + p_part2 + p_part3);
		selection = {p_Higgs.pt(), p_Higgs.Eta(), p_Higgs.Phi(), p_Higgs.M()};
    }
    return selection;
}


Vec_f getMinimum(Vec_f v1, Vec_f v2){
	Vec_f output = {};
	if (!v1.empty() && !v2.empty() && v1.size() == v2.size()){
		for (unsigned int i = 0; i < v1.size(); i++){
			output.push_back(min(v1[i], v2[i]));
		}
	}
	return output;
}


Vec_f getMaximum(Vec_f v1, Vec_f v2){
	Vec_f output = {};
	if (!v1.empty() && !v2.empty() && v1.size() == v2.size()){
		for (unsigned int i = 0; i < v1.size(); i++){
			output.push_back(max(v1[i], v2[i]));
		}
	}
	return output;
}


bool ifAllLessThan(Vec_f v1, float bound){
	if (v1.size() == 0)
		return false;
	for (unsigned int i = 0; i < v1.size(); i++){
		if(v1[i] >= bound){
			return false;
		}
	}
	return true;
}


bool ifAllGreaterThan(Vec_f v1, float bound){
	if (v1.size() == 0)
		return false;
	for (unsigned int i = 0; i < v1.size(); i++){
		if(v1[i] <= bound){
			return false;
		}
	}
	return true;
}


Vec_f getValuesIdParticle(Vec_f values, Vec_i& genPart_pdgId, int idParticle, int equal){
    //Returns the vector values if the particle idParticle exists in genPart_pdgId and equal=1
    //Returns the vector {} if the particle idParticle exists in genPart_pdgId and equal=1
	Vec_f output = {};
    if(equal == 0){
        for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
            if(genPart_pdgId[i] == idParticle){
                return output;
            }
        }
        return values;
    }
    else{
        for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
            if(genPart_pdgId[i] == idParticle){
                return values;
            }
        }
        return output;
    }
}


Vec_f sqrt(Vec_f v1){
	Vec_f output = {};
    for (unsigned int i = 0; i < v1.size(); i++){
			output.push_back(std::sqrt(v1[i]));
	}
    return output;
}


Vec_i getFilteredGoodMeson(Vec_i goodMeson, Vec_f goodMeson_pt, Vec_f goodMeson_vtx_prob){
	/**
	 * Filters a vector of good mesons indexes removing duplicates.
	 *
	 * @param goodMeson - A vector of integers representing good mesons indexes.
	 * @param goodMeson_pt - A vector of floats representing the transverse momenta of good mesons.
	 * @param goodMeson_vtx_prob - A vector of floats representing the vertex probabilities of good mesons.
	 *
	 * @return A vector of integers representing the filtered indexes of good mesons.
	 *
	 * This function filters the good mesons based on vertex probability and transverse momentum.
	 * The function checks if each good meson is similar to previously encountered good mesons, and if not, it adds the meson
	 * to the filtered list. The filtered indexes vector indicates which good mesons passed the filtering criteria (1 for
	 * filtered, 0 for not filtered).
	 */
	Vec_i filteredIndexes = {};
	Vec_f probs = {};
	Vec_f momentums = {};
	for(unsigned int i = 0; i < goodMeson.size(); i++){
		bool same = false;
		if (goodMeson[i] == 1){
			for(unsigned int j = 0; j < probs.size(); j++){
				if ((abs(probs[j] - goodMeson_vtx_prob[i]) < 0.0001) && (abs(momentums[j] - goodMeson_pt[i]) < 0.001)){//same meson
					same = true;
					break;
				}
			}
			if (same){
				filteredIndexes.push_back(0);
			}else{
				probs.push_back(goodMeson_vtx_prob[i]);
				momentums.push_back(goodMeson_pt[i]);
				filteredIndexes.push_back(1);
			}
		}else{
			filteredIndexes.push_back(0);
		}
	}
    return filteredIndexes;
}


Vec_i getFilteredGoodParticleMaxPt(Vec_i goodParticle, Vec_f goodParticle_pt){
	Vec_i filteredIndexes = {};
	float maxPt = 0;
	int maxPt_idx = 0;
	for(unsigned int i = 0; i < goodParticle.size(); i++){		
		if (goodParticle[i] == 1){
			if (goodParticle_pt[i] > maxPt){
				maxPt = goodParticle_pt[i];
				filteredIndexes[maxPt_idx] = 0;
				maxPt_idx = i;
				filteredIndexes.push_back(1);
			}else{
				filteredIndexes.push_back(0);
			}
		}else{
			filteredIndexes.push_back(0);
		}
	}
    return filteredIndexes;
}


Vec_i getFilteredGoodParticleMaxPtMass(Vec_i goodParticle, Vec_f goodParticle_pt, Vec_i goodParticle_Nphotons, Vec_f goodParticle_Nbody_mass, int caseNum){
	//case0: omega, case1: phi, case2: D0Star
	if (Sum(goodParticle_Nphotons) == 0) return getFilteredGoodParticleMaxPt(goodParticle, goodParticle_pt);
	
	float theoretical_mass = 0.0;
	if (caseNum == 0){
		theoretical_mass = omega_mass;
	} else if (caseNum == 1){
		theoretical_mass = phi_mass;
	} else if(caseNum == 2){
		theoretical_mass = D0Star_mass;
	}

	Vec_i filteredIndexes = {};
	float bestNBodyMassDiff = 1000.0;
	int bestNBodyMass_idx = 0;
	for(unsigned int i = 0; i < goodParticle.size(); i++){		
		if (goodParticle[i] == 1 && goodParticle_Nphotons[i] > 0){
			if (abs(goodParticle_Nbody_mass[i] - theoretical_mass) < bestNBodyMassDiff){
				bestNBodyMassDiff = abs(goodParticle_Nbody_mass[i] - theoretical_mass);
				filteredIndexes[bestNBodyMass_idx] = 0;
				bestNBodyMass_idx = i;
				filteredIndexes.push_back(1);
			}else{
				filteredIndexes.push_back(0);
			}
		}else{
			filteredIndexes.push_back(0);
		}
	}
    return filteredIndexes;
}


PtEtaPhiMVector sum2Body(const float particle1_pt, const float particle1_eta, const float particle1_phi, const float particle1_mass, 
	const float particle2_pt, const float particle2_eta, const float particle2_phi, const float particle2_mass){
	
	PtEtaPhiMVector particle1P4(particle1_pt, particle1_eta, particle1_phi, particle1_mass);
	PtEtaPhiMVector particle2P4(particle2_pt, particle2_eta, particle2_phi, particle2_mass);

	if (particle1_pt < 0.001){
		return particle2P4;
	}
	if (particle2_pt < 0.001){
		return particle1P4;
	}

	PtEtaPhiMVector twoBody = (particle1P4 + particle2P4);

    return twoBody;
}


PtEtaPhiMVector sum3Body(const float particle1_pt, const float particle1_eta, const float particle1_phi, const float particle1_mass, 
	const float particle2_pt, const float particle2_eta, const float particle2_phi, const float particle2_mass,
	const float particle3_pt, const float particle3_eta, const float particle3_phi, const float particle3_mass){

	PtEtaPhiMVector particle1P4(particle1_pt, particle1_eta, particle1_phi, particle1_mass);
	PtEtaPhiMVector particle2P4(particle2_pt, particle2_eta, particle2_phi, particle2_mass);
	PtEtaPhiMVector particle3P4(particle3_pt, particle3_eta, particle3_phi, particle3_mass);
	PtEtaPhiMVector threeBody = (particle1P4 + particle2P4 + particle3P4);

    return threeBody;
}


PtEtaPhiMVector diff2Body(const float particle1_pt, const float particle1_eta, const float particle1_phi, const float particle1_mass, 
	const float particle2_pt, const float particle2_eta, const float particle2_phi, const float particle2_mass){

	PtEtaPhiMVector particle1P4(particle1_pt, particle1_eta, particle1_phi, particle1_mass);
	PtEtaPhiMVector particle2P4(particle2_pt, particle2_eta, particle2_phi, particle2_mass);
	PtEtaPhiMVector twoBody = (particle1P4 - particle2P4);

    return twoBody;
}


Vec_f fmod(Vec_f v1, float mod){
	Vec_f output = {};
    for (unsigned int i = 0; i < v1.size(); i++){
			output.push_back(std::fmod(v1[i], mod));
	}
    return output;
}


#endif
