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


using Vec_i = ROOT::VecOps::RVec<int>;
using Vec_f = ROOT::VecOps::RVec<float>;
typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > PtEtaPhiMVector;

Vec_f getPTParticleMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_pt, int idParticle, int idMother){
    Vec_f selection = {};
	Vec_i indexMother = {};
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idMother){//this is the D0*, mother of D0
            indexMother.push_back(i);
        }
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idParticle){//get D0 son of D0Star
            	selection.push_back(genPart_pt[i]);
				return selection;
        	}
		}
    }
    return selection;
}

Vec_f getPTParticleMotherGrandMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_pt, int idParticle, int idMother, int idGrandMother){
    Vec_f selection = {};
	Vec_i indexMother = {};
	Vec_i indexGrandMother = {};
	for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
        if(genPart_pdgId[i] == idGrandMother){
            indexGrandMother.push_back(i);
        }
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
        	if(genPart_pdgId[i] == idMother){//get D0 son of D0Star
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idParticle){//get D0 son of D0Star
            	selection.push_back(genPart_pt[i]);
				return selection;
        	}
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

Vec_f getDRParticleMotherGrandMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, int idParticle1, int idMother1, int idGrandMother1, int idParticle2, int idMother2, int idGrandMother2){
    Vec_f selection = {};
    Vec_i indexMother1 = {};
	Vec_i indexGrandMother1 = {};
	Vec_i indexMother2 = {};
	Vec_i indexGrandMother2 = {};
	float phi1 = 0;
	float phi2 = 0;
	float eta1 = 0;
	float eta2 = 0;
	bool particle1 = false;
	bool particle2 = false;
    for(unsigned int i = 0; i < genPart_pdgId.size(); i++){
    	
    	if(genPart_pdgId[i] == idGrandMother1){
            indexGrandMother1.push_back(i);
        }
		else if(std::find(indexGrandMother1.begin(), indexGrandMother1.end(), genPart_genPartIdxMother[i]) != indexGrandMother1.end()){
        	if(genPart_pdgId[i] == idMother1){
            	indexMother1.push_back(i);
        	}
		}
		else if(std::find(indexMother1.begin(), indexMother1.end(), genPart_genPartIdxMother[i]) != indexMother1.end()){
			if(genPart_pdgId[i] == idParticle1 && !particle1){
            	phi1 = genPart_phi[i];
            	eta1 = genPart_eta[i];
				particle1 = true;
        	}
		}

    	if(genPart_pdgId[i] == idGrandMother2){
            indexGrandMother2.push_back(i);
        }
		else if(std::find(indexGrandMother2.begin(), indexGrandMother2.end(), genPart_genPartIdxMother[i]) != indexGrandMother2.end()){
        	if(genPart_pdgId[i] == idMother2){
            	indexMother2.push_back(i);
        	}
		}
		else if(std::find(indexMother2.begin(), indexMother2.end(), genPart_genPartIdxMother[i]) != indexMother2.end()){
			if(genPart_pdgId[i] == idParticle2 && !particle2){
            	phi2 = genPart_phi[i];
            	eta2 = genPart_eta[i];
				particle2 = true;
        	}
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

Vec_f getThreeBody4Momentum(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, Vec_f& genPart_pt, Vec_f& genPart_mass, int idParticle1, int idParticle2, int idParticle3, int idMother, int massPT){
    Vec_f selection = {};
	Vec_i indexMother = {};	
    float phi1 = 0;
    float phi2 = 0;
    float phi3 = 0;
    float eta1 = 0;
    float eta2 = 0;
    float eta3 = 0;
	float pt1 = 0;
	float pt2 = 0;
	float pt3 = 0;
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
            	phi1 = genPart_phi[i];
            	eta1 = genPart_eta[i];
				pt1 = genPart_pt[i];
				mass1 = genPart_mass[i];
            	particle1 = true;
        	}
        	else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
            	phi2 = genPart_phi[i];
            	eta2 = genPart_eta[i];
				pt2 = genPart_pt[i];
				mass2 = genPart_mass[i];
            	particle2 = true;
        	}
        	else if(genPart_pdgId[i] == idParticle3 && !particle3){//get particle 3
            	phi3 = genPart_phi[i];
            	eta3 = genPart_eta[i];
				pt3 = genPart_pt[i];
				mass3 = genPart_mass[i];
            	particle3 = true;
        	}
		}
    }
    if(particle1 && particle2 && particle3){
	//	cout << mass1 << " " << mass2 << " " << mass3 << endl;
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, 0.13498);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, 0.13957);
		PtEtaPhiMVector p_part3(pt3, eta3, phi3, 0.13957);
		if (massPT == 0)
	        selection.push_back((p_part1 + p_part2 + p_part3).M());
        else if (massPT == 1)
			selection.push_back((p_part1 + p_part2 + p_part3).pt());
		return selection;
    }
    return selection;
}

Vec_f getTwoBody4Momentum(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, Vec_f& genPart_pt, Vec_f& genPart_mass, int idParticle1, int idParticle2, int idMother, int massPT){
    Vec_f selection = {};
	Vec_i indexMother = {};	
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
        if(genPart_pdgId[i] == idMother){
            indexMother.push_back(i);
        }
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
            	phi1 = genPart_phi[i];
            	eta1 = genPart_eta[i];
				pt1 = genPart_pt[i];
				mass1 = genPart_mass[i];
            	particle1 = true;
        	}
        	else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
            	phi2 = genPart_phi[i];
            	eta2 = genPart_eta[i];
				pt2 = genPart_pt[i];
				mass2 = genPart_mass[i];
            	particle2 = true;
        	}
		}
    }
    if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, 0.13957);
		if (massPT == 0)
	        selection.push_back((p_part1 + p_part2).M());
        else if (massPT == 1)
			selection.push_back((p_part1 + p_part2).pt());
		return selection;
    }
    return selection;
}

Vec_f getTwoBody4MomentumGrandMother(Vec_i& genPart_pdgId, Vec_i& genPart_genPartIdxMother, Vec_f& genPart_phi, Vec_f& genPart_eta, Vec_f& genPart_pt, Vec_f& genPart_mass, int idParticle1, int idParticle2, int idMother, int idGrandMother, int massPT){
    Vec_f selection = {};
	Vec_i indexMother = {};	
	Vec_i indexGrandMother = {};	
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
		if(genPart_pdgId[i] == idGrandMother){
            indexGrandMother.push_back(i);
        }
		else if(std::find(indexGrandMother.begin(), indexGrandMother.end(), genPart_genPartIdxMother[i]) != indexGrandMother.end()){
        	if(genPart_pdgId[i] == idMother){
            	indexMother.push_back(i);
        	}
		}
		else if(std::find(indexMother.begin(), indexMother.end(), genPart_genPartIdxMother[i]) != indexMother.end()){
        	if(genPart_pdgId[i] == idParticle1 && !particle1){//get particle 1
            	phi1 = genPart_phi[i];
            	eta1 = genPart_eta[i];
				pt1 = genPart_pt[i];
				mass1 = genPart_mass[i];
            	particle1 = true;
        	}
        	else if(genPart_pdgId[i] == idParticle2 && !particle2){//get particle 2
            	phi2 = genPart_phi[i];
            	eta2 = genPart_eta[i];
				pt2 = genPart_pt[i];
				mass2 = genPart_mass[i];
            	particle2 = true;
        	}
		}
    }
    if(particle1 && particle2){
		PtEtaPhiMVector p_part1(pt1, eta1, phi1, mass1);
		PtEtaPhiMVector p_part2(pt2, eta2, phi2, 0.13957);
		if (massPT == 0)
	        selection.push_back((p_part1 + p_part2).M());
        else if (massPT == 1)
			selection.push_back((p_part1 + p_part2).pt());
		return selection;
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

#endif

