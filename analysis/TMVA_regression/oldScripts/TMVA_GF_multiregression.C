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

void TMVA_GF_multiregression(const char* outFileName, const char* channel, int testSet=0){
    
    bool useDLGPU = false;
#ifdef R__HAS_TMVAGPU
        useDLGPU = true;
#endif

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
    //TFile* outfile = TFile::Open(Form("/work/submit/pdmonte/%s", outFileName), "RECREATE");
    TFile* outfile = TFile::Open(outFileName, "RECREATE");
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

    // Add target values
    dataloader->AddTarget("goodMeson_pt_GEN");
    dataloader->AddTarget("goodPhotons_pt_GEN");

    // Add training and testing trees
    cout << "\033[1;36m-------------------------------------- ADD TREES, CUT and SPLIT -------------------------------------\033[0m" << endl;
    // Set weights.
    //dataloader->SetWeightExpression("w*lumiIntegrated", "Regression");
    Double_t regWeight  = 1.0;
    const char* positivePT = "goodMeson_pt_GEN > 0";
    const char* trainTreeEventSplitStr = Form("(Entry$ %% 3) != %d", testSet);
    const char* testTreeEventSplitStr = Form("(Entry$ %% 3) == %d", testSet);
    TCut cutTrain = Form("%s && %s", trainTreeEventSplitStr, positivePT);
    TCut cutTest = Form("%s && %s", testTreeEventSplitStr, positivePT);

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

    cout << "\033[1;36m------------------------------------------ BOOKING METHODS ------------------------------------------\033[0m" << endl;

    // Booking Methods. Methods that support multitarget regression: kPDERS, kPDEFoam, kMLP, kDL, kPyKeras

    // Probability density estimator range search method (multi-dimensional)
    //factory.BookMethod(dataloader, TMVA::Types::kPDERS, "PDERS",    "!V:NormTree=T:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=100:NEventsMax=500:MaxVIterations=1000");
    // Multi-dimensional PDE using self-adapting phase-space binning
    //factory.BookMethod(dataloader, TMVA::Types::kPDEFoam, "PDEFoam", "H:V:MultiTargetRegression=T:SigBgSeparate=F:TailCut=0.001:VolFrac=0.0333:nActiveCells=500:nSampl=2000:nBin=5:Nmin=100:Kernel=None:Compress=T");
    // Artificial Neural Network (Multilayer perceptron) - TMVA version
    //factory.BookMethod(dataloader, TMVA::Types::kMLP, "MLP",        "!V:NeuronType=tanh:VarTransform=N:NCycles=500:HiddenLayers=N+5:TestRate=5");
    // NN with BFGS quadratic minimisation
    factory.BookMethod(dataloader, TMVA::Types::kMLP, "MLP_BFGS",   "!V:NeuronType=sigmoid:VarTransform=N:NCycles=1000:HiddenLayers=N,N-1:TestRate=10:TrainingMethod=BFGS");


    // Deep Neural Network
    if (false){
        // Define DNN layout
        TString inputLayoutString = "InputLayout=1|1|14";
        TString batchLayoutString = "BatchLayout=1|128|14";
        TString layoutString = "Layout=DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|1|LINEAR";
        // Define Training strategies: one can catenate several training strategies
        TString training1("LearningRate=1e-3,Momentum=0.9,"
                          "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
                          "MaxEpochs=30,WeightDecay=1e-4,Regularization=None,"
                          "Optimizer=ADAM,ADAM_beta1=0.9,ADAM_beta2=0.999,ADAM_eps=1.E-7," // ADAM default parameters
                          "DropConfig=0.0+0.0+0.0+0.");
        //     TString training2("LearningRate=1e-3,Momentum=0.9"
        //                       "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
        //                       "MaxEpochs=20,WeightDecay=1e-4,Regularization=None,"
        //                       "Optimizer=SGD,DropConfig=0.0+0.0+0.0+0.");
 
        TString trainingStrategyString = "TrainingStrategy=";
        trainingStrategyString += training1; // + "|" + training2;
 
        // General Options.
        TString dnnOptions ("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=G:WeightInitialization=XAVIER");
        dnnOptions.Append (":"); dnnOptions.Append (inputLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (batchLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (layoutString);
        dnnOptions.Append (":"); dnnOptions.Append (trainingStrategyString);
 
        TString dnnMethodName = "DNN_CPU";
        if (useDLGPU) {
            dnnOptions += ":Architecture=GPU";
            dnnMethodName = "DNN_GPU";
        } else {
            dnnOptions += ":Architecture=CPU";
        }
        factory.BookMethod(dataloader, TMVA::Types::kDL, dnnMethodName, dnnOptions);
    }
 
    /*
    // Keras deep learning
    if (useKeras) {

        Info("TMVA_Higgs_Classification", "Building deep neural network with keras ");
        // create python script which can be executed
        // create 2 conv2d layer + maxpool + dense
        TMacro m;
        m.AddLine("import tensorflow");
        m.AddLine("from tensorflow.keras.models import Sequential");
        m.AddLine("from tensorflow.keras.optimizers import Adam");
        m.AddLine("from tensorflow.keras.layers import Input, Dense");
        m.AddLine("");
        m.AddLine("model = Sequential() ");
        m.AddLine("model.add(Dense(64, activation='relu',input_dim=7))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(2, activation='sigmoid'))");
        m.AddLine("model.compile(loss = 'binary_crossentropy', optimizer = Adam(learning_rate = 0.001), metrics = ['accuracy'])");
        m.AddLine("model.save('Higgs_model.h5')");
        m.AddLine("model.summary()");
 
        m.SaveSource("make_higgs_model.py");
        // execute
        auto ret = (TString *)gROOT->ProcessLine("TMVA::Python_Executable()");
        TString python_exe = (ret) ? *(ret) : "python";
        gSystem->Exec(python_exe + " make_higgs_model.py");
 
        if (gSystem->AccessPathName("Higgs_model.h5")) {
            Warning("TMVA_Higgs_Classification", "Error creating Keras model file - skip using Keras");
        } else {
            // book PyKeras method only if Keras model could be created
            Info("TMVA_Higgs_Classification", "Booking tf.Keras Dense model");
            factory.BookMethod(
                               dataloader, TMVA::Types::kPyKeras, "PyKeras",
                               "H:!V:VarTransform=None:FilenameModel=Higgs_model.h5:tf.keras:"
                               "FilenameTrainedModel=Higgs_trained_model.h5:NumEpochs=20:BatchSize=100:"
                               "GpuOptions=allow_growth=True"); // needed for RTX NVidia card and to avoid TF allocates all GPU memory
        }
    }
    */

    // Train all the previously booked methods.
    cout << "\033[1;36m-------------------------------------------- TRAINING... --------------------------------------------\033[0m" << endl;
    factory.TrainAllMethods();
 
    // Test and evaluate all methods using the test data set.
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
