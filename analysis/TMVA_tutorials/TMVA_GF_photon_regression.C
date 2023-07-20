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

void TMVA_GF_photon_regression(const char* outFileName, const char* channel, int testSet=0){

    time_t start_t;
    struct tm * timeinfo;
    time (&start_t);
    timeinfo = localtime(&start_t);
    printf("Staring: %s", asctime(timeinfo));

    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 25;
    (TMVA::gConfig().GetIONames()).fWeightFileDir = "../../../../../../../../../work/submit/pdmonte/weights";
    
    // Open files
    TFile* sgnfile;
    if(std::strcmp(channel, "omega") == 0 || std::strcmp(channel, "o") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUN29/2018/outname_mc1038_GFcat_OmegaCat_2018.root", "READ");
    else if(std::strcmp(channel, "phi") == 0 || std::strcmp(channel, "phi3") == 0 || std::strcmp(channel, "p") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUN29/2018/outname_mc1039_GFcat_Phi3Cat_2018.root", "READ");
    else if(std::strcmp(channel, "d0starrho") == 0 || std::strcmp(channel, "dr") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUN29/2018/outname_mc1040_GFcat_D0StarRhoCat_2018.root", "READ");
    else if(std::strcmp(channel, "d0star") == 0 || std::strcmp(channel, "d") == 0)
        sgnfile = TFile::Open("/data/submit/pdmonte/outputs/JUN29/2018/outname_mc1041_GFcat_D0StarCat_2018.root", "READ");     
    else
        return -1;

    // Initialize the dataset
    TFile* outfile = TFile::Open(Form("/work/submit/pdmonte/%s", outFileName), "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

    // Add variables to dataset
    dataloader->AddVariable("goodMeson_pt[0]", "meson_pt", "GeV", 'F');
    dataloader->AddVariable("goodMeson_eta[0]", "meson_eta", "", 'F');
    dataloader->AddVariable("goodMeson_phi[0]", "meson_phi", "", 'F');
    dataloader->AddVariable("goodMeson_mass[0]", "meson_mass", "GeV", 'F');

    dataloader->AddVariable("goodMeson_ditrk_pt[0]", "meson_ditrk_pt", "GeV", 'F');
    dataloader->AddVariable("goodMeson_ditrk_eta[0]", "meson_ditrk_eta", "", 'F');
    dataloader->AddVariable("goodMeson_ditrk_phi[0]", "meson_ditrk_phi", "", 'F');
    dataloader->AddVariable("goodMeson_ditrk_mass[0]", "meson_ditrk_mass", "GeV", 'F');

    dataloader->AddVariable("goodMeson_Nphotons[0]", "meson_N_photons", "", 'I');
    dataloader->AddVariable("goodMeson_photons_pt[0]", "meson_photons_pt", "GeV", 'F');
    dataloader->AddVariable("goodMeson_photons_DR[0]", "meson_photons_DR", "", 'F');

    dataloader->AddVariable("goodPhotons_pt[0]", "photon_pt", "GeV", 'F');
    dataloader->AddVariable("goodPhotons_eta[0]", "photon_eta", "", 'F');
    dataloader->AddVariable("goodPhotons_phi[0]", "photon_phi", "", 'F');

    // Add spectators not used in training
    dataloader->AddSpectator("HCandMass", "HCandMass");
    dataloader->AddSpectator("goodMeson_pt", "goodMeson_pt");
    dataloader->AddSpectator("goodMeson_eta", "goodMeson_eta");
    dataloader->AddSpectator("goodMeson_phi", "goodMeson_phi");
    dataloader->AddSpectator("goodMeson_mass", "goodMeson_mass");
    dataloader->AddSpectator("goodPhotons_pt", "goodPhotons_pt");
    dataloader->AddSpectator("goodPhotons_eta", "goodPhotons_eta");
    dataloader->AddSpectator("goodPhotons_phi", "goodPhotons_phi");
    dataloader->AddSpectator("goodMeson_pt_GEN", "goodMeson_pt_GEN");
    dataloader->AddSpectator("goodMeson_eta_GEN", "goodMeson_eta_GEN");
    dataloader->AddSpectator("goodMeson_phi_GEN", "goodMeson_phi_GEN");
    dataloader->AddSpectator("goodMeson_mass_GEN", "goodMeson_mass_GEN");
    dataloader->AddSpectator("goodPhotons_pt_GEN", "goodPhotons_pt_GEN");
    dataloader->AddSpectator("goodPhotons_eta_GEN", "goodPhotons_eta_GEN");
    dataloader->AddSpectator("goodPhotons_phi_GEN", "goodPhotons_phi_GEN");

    // Add target value
    dataloader->AddTarget("goodPhotons_pt_GEN");

    // Set weights.
    Double_t regWeight  = 1.0;
    
    // Add training and testing trees
    cout << "\033[1;36m-------------------------------------- ADD TREES, CUT and SPLIT -------------------------------------\033[0m" << endl;
    TCut cutTrain = Form("(Entry$ %% 3) != %d", testSet);
    TCut cutTest = Form("(Entry$ %% 3) == %d", testSet);
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
    
    TMVA::Factory factory("TMVARegression", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Regression:Transformations=P,D");

    // Booking Methods 
    factory.BookMethod(dataloader, TMVA::Types::kBDT, "BDTG_photon",
	    "!V:VarTransform=P,N:NTrees=1000:BoostType=Grad:Shrinkage=0.3:MaxDepth=5:SeparationType=MisClassificationError:nCuts=30:UseRandomisedTrees:UseNvars=39:UseBaggedBoost:BaggedSampleFraction=1.45822:PruneMethod=NoPruning");
    
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
    std::cout << "==> TMVARegression is done!" << std::endl;

    time_t end_t;
    time (&end_t);
    double diff_t = difftime(end_t, start_t);
    printf("Execution time: %d seconds\n", (int)diff_t);

    cout << "\033[1;36m----------------------------------------------- DONE! -----------------------------------------------\033[0m" << endl;
}
