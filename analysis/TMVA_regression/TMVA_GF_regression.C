#include <string.h>
#include <time.h>

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

void TMVA_GF_regression(const char* outFileName, const char* channel, int testSet=0, const char* nameModel = "model", const char* variables[] = {}, int numVariables=0, int codeDF=127, int codeDL=511){

    time_t start_t;
    struct tm * timeinfo;
    time (&start_t);
    timeinfo = localtime(&start_t);
    printf("Staring: %s", asctime(timeinfo));

    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 25;
    (TMVA::gConfig().GetIONames()).fWeightFileDir = "../../../../../../../../../data/submit/pdmonte/TMVA_models/weightsVars";
    
    // Open files
    TFile* sgnfile;
    if(std::strcmp(channel, "omega") == 0 || std::strcmp(channel, "o") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUL31/2018/outname_mc1038_GFcat_OmegaCat_2018.root", "READ");
    else if(std::strcmp(channel, "phi") == 0 || std::strcmp(channel, "phi3") == 0 || std::strcmp(channel, "p") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUL31/2018/outname_mc1039_GFcat_Phi3Cat_2018.root", "READ");
    else if(std::strcmp(channel, "d0starrho") == 0 || std::strcmp(channel, "dr") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUL31/2018/outname_mc1040_GFcat_D0StarRhoCat_2018.root", "READ");
    else if(std::strcmp(channel, "d0star") == 0 || std::strcmp(channel, "d") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUL31/2018/outname_mc1041_GFcat_D0StarCat_2018.root", "READ");     
    else
        return -1;

    // Initialize the dataset
    TFile* outfile = TFile::Open(Form("/data/submit/pdmonte/TMVA_models/rootVars/%s", outFileName), "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

    // Add variables to dataset
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_eta_input_pred", "goodMeson_eta_input_pred", "", 'F');}   codeDL /= 2;                  // 000000001 = 1    1
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_phi_input_pred", "goodMeson_phi_input_pred", "", 'F');}   codeDL /= 2;                  // 000000010 = 2    2
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_ditrk_eta_input_pred", "goodMeson_ditrk_eta_input_pred", "", 'F');}   codeDL /= 2;      // 000000100 = 4    3
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_ditrk_phi_input_pred", "goodMeson_ditrk_phi_input_pred", "", 'F');}   codeDL /= 2;      // 000001000 = 8    4
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_Nphotons_input_pred", "goodMeson_Nphotons_input_pred", "", 'F');}   codeDL /= 2;        // 000010000 = 16   5
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_photon1_DR_input_pred", "goodMeson_photon1_DR_input_pred", "", 'F');}   codeDL /= 2;    // 000100000 = 32   6
    if (codeDL % 2) {dataloader->AddVariable("goodMeson_photon2_DR_input_pred", "goodMeson_photon2_DR_input_pred", "", 'F');}   codeDL /= 2;    // 001000000 = 64   7
    if (codeDL % 2) {dataloader->AddVariable("goodPhotons_eta_input_pred", "goodPhotons_eta_input_pred", "", 'F');}   codeDL /= 2;              // 010000000 = 128  8
    if (codeDL % 2) {dataloader->AddVariable("goodPhotons_phi_input_pred", "goodPhotons_phi_input_pred", "", 'F');}   codeDL /= 2;              // 100000000 = 256  9
    if (codeDL > 0) {cout << "codeDL greater than 511!" << endl; return -1;}

    
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_photon1_pt_input_pred", "goodMeson_photon1_pt_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000001 = 1     1
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_photon2_pt_input_pred", "goodMeson_photon2_pt_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000010 = 2     2
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_ditrk_mass_input_pred", "goodMeson_ditrk_mass_input_pred", "GeV", 'F');}   codeDF /= 2;  // 0000100 = 4     3
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_mass_input_pred", "goodMeson_mass_input_pred", "GeV", 'F');}               codeDF /= 2;  // 0001000 = 8     4
    if (codeDF % 2) {dataloader->AddVariable("goodPhotons_pt_input_pred", "goodPhotons_pt_input_pred", "GeV", 'F');}               codeDF /= 2;  // 0010000 = 16    5
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_ditrk_pt_input_pred", "goodMeson_ditrk_pt_input_pred", "GeV", 'F');}       codeDF /= 2;  // 0100000 = 32    6
    if (codeDF % 2) {dataloader->AddVariable("goodMeson_pt_input_pred", "goodMeson_pt_input_pred", "GeV", 'F');}                   codeDF /= 2;  // 1000000 = 64    7
    if (codeDF > 0) {cout << "codeDF greater than 127!" << endl; return -1;}

    for(int i = 0; i < numVariables; i++){
        cout << variables[i] << endl;
        dataloader->AddVariable(variables[i], variables[i], "", 'F');
    }

    // Add target value
    dataloader->AddTarget("goodMeson_pt_GEN/goodMeson_pt_input_pred");
    
    // Add training and testing trees
    cout << "\033[1;36m-------------------------------------- ADD TREES, CUT and SPLIT -------------------------------------\033[0m" << endl;
    // Set weights.
    //dataloader->SetWeightExpression("w*lumiIntegrated", "Regression");
    Double_t regWeight  = 1.0;
    TCut cutTrain = Form("(Entry$ %% 20) != %d", testSet);
    TCut cutTest = Form("(Entry$ %% 20) == %d", testSet);
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Regression", regWeight, cutTrain, "train");
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Regression", regWeight, cutTest, "test");

    int nEntries = ((TTree*)sgnfile->Get("events"))->GetEntries();
    int nTrain = (((TTree*)sgnfile->Get("events"))->CopyTree(cutTrain))->GetEntries();
    int nTest = (((TTree*)sgnfile->Get("events"))->CopyTree(cutTest))->GetEntries();

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
 
    factory.BookMethod(dataloader, TMVA::Types::kBDT, nameModel,
        "!V:NTrees=1000:BoostType=Grad:Shrinkage=0.2:MaxDepth=5:SeparationType=SDivSqrtSPlusB:nCuts=90:UseRandomisedTrees=T:UseNvars=67:UseBaggedBoost:BaggedSampleFraction=2.4:PruneMethod=NoPruning");
    
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
