#include <string.h>
#include <time.h>
#include <vector>

#include "TROOT.h"
#include "TMVA/CrossValidation.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Factory.h"
#include "TMVA/Types.h"
#include "TFile.h"
#include "TCollection.h"
#include "TCut.h"
#include "TObjArray.h"
#include "TString.h"
#include "TTree.h"

using namespace TMVA;

void TMVA_GF_regression(const char* nameModel, const char* channel, const char* prodCat="ggH", int testSet=0, const std::vector<int>& variables={}, int codeDF=127, int codeDL=4095, const char* options = ""){

    time_t start_t;
    struct tm * timeinfo;
    time (&start_t);
    timeinfo = localtime(&start_t);
    printf("Staring: %s", asctime(timeinfo));

    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 80;
    (TMVA::gConfig().GetIONames()).fWeightFileDir = "../../../../../../../../../data/submit/pdmonte/TMVA_models/weightsOptsFinalBis";
    
    // Open files
    int trainA, trainB;
    if(testSet == 0){
        trainA = 1;
        trainB = 2;
    }else if(testSet == 1){
        trainA = 2;
        trainB = 0;
    }else if(testSet == 2){
        trainA = 0;
        trainB = 1;
    }

    int delta = 0;
    if(std::strcmp(prodCat, "ggH") == 0 || std::strcmp(prodCat, "ggh") == 0 || std::strcmp(prodCat, "GGH") == 0){
        delta = 0;
    }else if(std::strcmp(prodCat, "vbf") == 0 || std::strcmp(prodCat, "VBF") == 0){
        delta = 30;
    }

    cout << prodCat << endl;

    cout << "Train on sets " << trainA << " and " << trainB << endl;

    TFile* sgnfileA;
    TFile* sgnfileB;
    if(std::strcmp(channel, "omega") == 0 || std::strcmp(channel, "o") == 0){
        sgnfileA = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_OmegaCat_2018_sample%d.root", 1038 + delta, trainA), "READ");
        sgnfileB = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_OmegaCat_2018_sample%d.root", 1038 + delta, trainB), "READ");
    }else if(std::strcmp(channel, "phi") == 0 || std::strcmp(channel, "phi3") == 0 || std::strcmp(channel, "p") == 0){
        sgnfileA = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_Phi3Cat_2018_sample%d.root", 1039 + delta, trainA), "READ");
        sgnfileB = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_Phi3Cat_2018_sample%d.root", 1039 + delta, trainB), "READ");
    }else if(std::strcmp(channel, "d0starrho") == 0 || std::strcmp(channel, "dr") == 0){
        sgnfileA = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarRhoCat_2018_sample%d.root", 1040 + delta, trainA), "READ");
        sgnfileB = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarRhoCat_2018_sample%d.root", 1040 + delta, trainB), "READ");
    }else if(std::strcmp(channel, "d0star") == 0 || std::strcmp(channel, "d") == 0){
        sgnfileA = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarCat_2018_sample%d.root", 1041 + delta, trainA), "READ");
        sgnfileB = TFile::Open(Form("/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarCat_2018_sample%d.root", 1041 + delta, trainB), "READ");   
    }else
        return -1;

    // Initialize the dataset
    TFile* outfile = TFile::Open(Form("/data/submit/pdmonte/TMVA_models/rootVars/%s", Form("%s_%s_%s_%d.root", nameModel, channel, prodCat, testSet)), "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

    // Add variables to dataset
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_photon1_pt_input_pred", "goodMeson_photon1_pt_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000001 = 1     1
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_photon2_pt_input_pred", "goodMeson_photon2_pt_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000010 = 2     2
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_ditrk_mass_input_pred", "goodMeson_ditrk_mass_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000100 = 4     3
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_mass_input_pred", "goodMeson_mass_input_pred", "GeV", 'F');}               codeDF /= 2;  // 0001000 = 8     4
    if (codeDF % 2) {dataloader->AddVariable("goodPhotons_pt_input_pred", "goodPhotons_pt_input_pred", "GeV", 'F');}               codeDF /= 2;  // 0010000 = 16    5
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_ditrk_pt_input_pred", "goodMeson_ditrk_pt_input_pred", "GeV", 'F');}       codeDF /= 2;  // 0100000 = 32    6
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_pt_input_pred", "goodMeson_pt_input_pred", "GeV", 'F');}                   codeDF /= 2;  // 1000000 = 64    7
    if (codeDF > 0) {cout << "codeDF greater than 127!" << endl; return -1;}

    if (codeDL % 2) {dataloader->AddVariable("goodMeson_eta_input_pred", "goodMeson_eta_input_pred", "", 'F');}   codeDL /= 2;                  // 000000000001 = 1    1
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_phi_input_pred", "goodMeson_phi_input_pred", "", 'F');}   codeDL /= 2;                  // 000000000010 = 2    2
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_ditrk_eta_input_pred", "goodMeson_ditrk_eta_input_pred", "", 'F');}   codeDL /= 2;      // 000000000100 = 4    3
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_ditrk_phi_input_pred", "goodMeson_ditrk_phi_input_pred", "", 'F');}   codeDL /= 2;      // 000000001000 = 8    4
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_Nphotons_input_pred", "goodMeson_Nphotons_input_pred", "", 'F');}   codeDL /= 2;        // 000000010000 = 16   5
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_photon1_DR_input_pred", "goodMeson_photon1_DR_input_pred", "", 'F');}   codeDL /= 2;    // 000000100000 = 32   6
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_photon2_DR_input_pred", "goodMeson_photon2_DR_input_pred", "", 'F');}   codeDL /= 2;    // 000001000000 = 64   7
    if (codeDL % 2) {dataloader->AddVariable("goodPhotons_eta_input_pred", "goodPhotons_eta_input_pred", "", 'F');}   codeDL /= 2;              // 000010000000 = 128  8
    if (codeDL % 2) {dataloader->AddVariable("goodPhotons_phi_input_pred", "goodPhotons_phi_input_pred", "", 'F');}   codeDL /= 2;              // 000100000000 = 256  9
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_DR_input_pred", "goodMeson_DR_input_pred", "", 'F');}   codeDL /= 2;                    // 001000000000 = 512  10
    if (codeDL % 2) {dataloader->AddVariable("delta_eta_goodMeson_ditrk_goodPhoton_input_pred", "delta_eta_goodMeson_ditrk_goodPhoton_input_pred", "", 'F');}   codeDL /= 2;              // 010000000000 = 1024  11
    if (codeDL % 2) {dataloader->AddVariable("delta_phi_goodMeson_ditrk_goodPhoton_input_pred", "delta_phi_goodMeson_ditrk_goodPhoton_input_pred", "", 'F');}   codeDL /= 2;              // 100000000000 = 2048  12
    if (codeDL > 0) {cout << "codeDL greater than 4095!" << endl; return -1;}

    for(int i = 0; i < variables.size(); i++){
        //cout << Form("var%d_input_pred", variables[i]) << endl;
        dataloader->AddVariable(Form("var%d_input_pred", variables[i]), Form("var%d_input_pred", variables[i]), "", 'F');
    }

    // Add target value
    dataloader->AddTarget("goodMeson_pt_GEN/goodMeson_pt_input_pred");
    // Add variable to correlation matrices
    //dataloader->AddVariable("HCandMass", "HCandMass", "", 'F');
    
    // Add training and testing trees
    cout << "\033[1;36m-------------------------------------- ADD TREES, CUT and SPLIT -------------------------------------\033[0m" << endl;
    // Set weights.
    //dataloader->SetWeightExpression("w*lumiIntegrated", "Regression");
    Double_t regWeight  = 1.0;
    TCut cutTrain = Form("(Entry$ %% 50) != %d", testSet);
    TCut cutTest = Form("(Entry$ %% 50) == %d", testSet);
    dataloader->AddTree((TTree*)sgnfileA->Get("events"), "Regression", regWeight, cutTrain, "train");
    dataloader->AddTree((TTree*)sgnfileA->Get("events"), "Regression", regWeight, cutTest, "test");
    dataloader->AddTree((TTree*)sgnfileB->Get("events"), "Regression", regWeight, cutTrain, "train");
    dataloader->AddTree((TTree*)sgnfileB->Get("events"), "Regression", regWeight, cutTest, "test");

    int nEntries = ((TTree*)sgnfileA->Get("events"))->GetEntries() + ((TTree*)sgnfileB->Get("events"))->GetEntries();
    int nTrain = (((TTree*)sgnfileA->Get("events"))->CopyTree(cutTrain))->GetEntries() + (((TTree*)sgnfileB->Get("events"))->CopyTree(cutTrain))->GetEntries();
    int nTest = (((TTree*)sgnfileA->Get("events"))->CopyTree(cutTest))->GetEntries() + (((TTree*)sgnfileB->Get("events"))->CopyTree(cutTest))->GetEntries();

    cout << "Number of entries: " << nEntries << endl;
    cout << "Cut train: " << cutTrain << "\tTraining events: " << nTrain << " (" << ((double)((int)((double)nTrain/nEntries*10000)))/100.0 << "\%)" << endl;
    cout << "Cut test:  " << cutTest  << "\tTesting events:  " << nTest  << " (" << ((double)((int)((double)nTest/nEntries*10000)))/100.0 << "\%)"  << endl;

    // Preparing trees
    cout << "\033[1;36m------------------------------------------ PREPARING TREES ------------------------------------------\033[0m" << endl;
    
    TString prepareOptions = "!V:SplitMode=Random:NormMode=None:MixMode=Random";
    dataloader->PrepareTrainingAndTestTree("", prepareOptions);
    
    cout << "\033[1;36m---------------------------------------------- FACTORY ----------------------------------------------\033[0m" << endl;
    
    TMVA::Factory factory("TMVARegression", outfile, "!V:!Silent:Color:DrawProgressBar=F:AnalysisType=Regression:Transformations=P,D");

    // Booking Methods ------------------------------------------------------------------------------------
    TString modelOptions = "!V:NTrees=1000:BoostType=Grad:Shrinkage=0.2:MaxDepth=5:SeparationType=SDivSqrtSPlusB:nCuts=90:UseRandomisedTrees=T:UseNvars=67:UseBaggedBoost:BaggedSampleFraction=2.4:PruneMethod=NoPruning";
    if(std::strcmp(options, "") != 0){
        modelOptions = options;
    }
    factory.BookMethod(dataloader, TMVA::Types::kBDT, Form("%s_%s_%s_%d", nameModel, channel, prodCat, testSet), modelOptions);
    
	// Train Methods: Here we train all the previously booked methods.
    cout << "\033[1;36m-------------------------------------------- TRAINING... --------------------------------------------\033[0m" << endl;
    factory.TrainAllMethods();
 
    // Test  all methods: Now we test and evaluate all methods using the test data set.
    cout << "\033[1;36m---------------------------------------------- TESTING ----------------------------------------------\033[0m" << endl;
    factory.TestAllMethods();
    cout << "\033[1;36m--------------------------------------------- EVALUATING --------------------------------------------\033[0m" << endl;
    factory.EvaluateAllMethods();

    outfile->Close();
    std::cout << "==> Wrote root file: " << outfile->GetName() << std::endl;

    time_t end_t;
    time (&end_t);
    double diff_t = difftime(end_t, start_t);
    printf("Execution time: %d seconds\n", (int)diff_t);

    cout << "\033[1;36m----------------------------------------------- DONE! -----------------------------------------------\033[0m" << endl;
}
