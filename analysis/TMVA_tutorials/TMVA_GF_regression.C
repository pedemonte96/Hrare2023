#include <string.h>

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

void TMVA_GF_regression(const char* outFileName, const char* channel, int testSet=0){

    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 25;
    
    // options to control used methods
    bool useRandomSplitting = false; // option for cross validation
    bool useLikelihood = false;    // likelihood based discriminant
    bool useLikelihoodKDE = false;    // likelihood based discriminant
    bool useFischer = false;       // Fischer discriminant
    bool useMLP = false;          // Multi Layer Perceptron (old TMVA NN implementation)
    bool useBDT = false;           // Boosted Decision Tree (AdaBoost)
    bool useBDTG = true;         // BDT with GradBoost
    bool useDL = false;           // TMVA Deep Learning ( CPU or GPU)
    // bool useKeras = false;        // Keras Deep learning
    
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

    dataloader->AddVariable("goodMeson_DR[0]", "meson_DR", "", 'F');

    dataloader->AddVariable("goodMeson_Nphotons[0]", "meson_N_photons", "", 'I');
    dataloader->AddVariable("goodMeson_photons_pt[0]", "meson_photons_pt", "GeV", 'F');

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
    dataloader->AddTarget("goodMeson_pt_GEN");

    // Set weights.
    dataloader->SetWeightExpression("w*lumiIntegrated", "Regression");

    // global event weights per tree (see below for setting event-wise weights)
    Double_t regWeight  = 1.0;
    
    // Register trees
    cout << "\033[1;36m-------------------------------------- ADD TREES --------------------------------------\033[0m" << endl;
    dataloader->AddRegressionTree((TTree*)sgnfile->Get("events"), regWeight);

    // Apply cuts and split
    cout << "\033[1;36m-------------------------------------- CUT and SPLIT --------------------------------------\033[0m" << endl;
    TCut positivePT = "goodMeson_pt_GEN > 0";
    //Select 2/3 to train and 1/3 to test.
    int nEntries = ((TTree*)sgnfile->Get("events"))->GetEntries();
    double trainingPart = 0.66; // Train with 66% of the dataset
    int nTrain = (int)(nEntries * trainingPart);

    cout << "Cut: " << positivePT << endl;
    cout << "Number of entries: " << nEntries << endl;
    cout << "Trainig set: " << nTrain << " (" << trainingPart*100 << "\%)\t" << "Testing set: " << nEntries - nTrain << " (" << (1-trainingPart)*100 << "\%)" << endl;

    TString prepareOptions = "!V:nTrain_Regression=%d:nTest_Regression=0:SplitMode=Random:NormMode=None:MixMode=Random";

    dataloader->PrepareTrainingAndTestTree(positivePT, Form(prepareOptions, nTrain));
    
    cout << "\033[1;36m-------------------------------------- FACTORY --------------------------------------\033[0m" << endl;
    
    TMVA::Factory factory("TMVARegression", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Regression:Transformations=P,D");

    /*
    // Use cross validation
    int numFolds = 3;
    const char* analysisType = "Classification";
    const char* splitType = (useRandomSplitting) ? "Random" : "Deterministic";
    const char* splitExpr = (!useRandomSplitting) ? "int(fabs([eventID]))%int([NumFolds])" : "";
    TString cvOptions = Form("!V"
                            ":!Silent"
                            ":ModelPersistence"
                            ":AnalysisType=%s"
                            ":SplitType=%s"
                            ":NumFolds=%i"
                            ":SplitExpr=%s",
                            analysisType, splitType, numFolds, splitExpr);
    TMVA::CrossValidation cv("TMVACrossValidation", dataloader, outfile, cvOptions);
    */
    /*
        ## Booking Methods:
        Here we book the TMVA methods. We book first a Likelihood based on KDE (Kernel Density Estimation), a Fischer discriminant, a BDT
        and a shallow neural network
    */
 
    // Likelihood ("naive Bayes estimator")
    if (useLikelihood){
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "Likelihood",
                           "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );
    }
    // Use a kernel density estimator to approximate the PDFs
    if (useLikelihoodKDE){
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "LikelihoodKDE",
                      "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" );
    }
 
    // Fisher discriminant (same as LD)
    if (useFischer){
        factory.BookMethod(dataloader,TMVA::Types::kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" );
    }
 
    // Boosted Decision Trees
    if (useBDT){
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA_d2_t200",
        //               "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.1:UseBaggedBoost:BaggedSampleFraction=0.01:SeparationType=GiniIndex:nCuts=30" );
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA",
                           "!V:VarTransform=D:NTrees=115:MinNodeSize=5:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.7:SeparationType=GiniIndex:nCuts=12" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA_d4_t60",
        //              "!V:NTrees=80:MinNodeSize=2.5%:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    }

    if (useBDTG){
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_depth4_with_pruning",
                           "!V:VarTransform=P,D:NTrees=100:BoostType=Grad:Shrinkage=0.06:MaxDepth=4:SeparationType=GiniIndex:nCuts=15:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=CostComplexity:PruneStrength=80" );
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG115",
                           "!V:VarTransform=P,D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=NoPruning" );
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG200",
                           "!V:VarTransform=P,D:NTrees=200:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=NoPruning");
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_d3",
                          "!V:NTrees=600:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.6:PruneMethod=CostComplexity:PruneStrength=60" );
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG__rho",
                         "!V:NTrees=100:BoostType=Grad:Shrinkage=0.1:MaxDepth=2:SeparationType=GiniIndex:nCuts=30:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.15" );
    }
 
    // Multi-Layer Perceptron (Neural Network)
    if (useMLP){
        factory.BookMethod(dataloader,TMVA::Types::kMLP, "MLP",
                      "!H:!V:NeuronType=tanh:VarTransform=N:NCycles=100:HiddenLayers=N+5:TestRate=5:UseRegulator" );
    }

    // Deep Neural Network
    if (useDL){
 
        bool useDLGPU = false;
#ifdef R__HAS_TMVAGPU
        useDLGPU = true;
#endif
 
        // Define DNN layout
        TString inputLayoutString = "InputLayout=1|1|14";
        TString batchLayoutString= "BatchLayout=1|128|14";
        TString layoutString ("Layout=DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|1|LINEAR");
        // Define Training strategies
        // one can catenate several training strategies
        TString training1("LearningRate=1e-3,Momentum=0.9,"
                          "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
                          "MaxEpochs=30,WeightDecay=1e-4,Regularization=None,"
                          "Optimizer=ADAM,ADAM_beta1=0.9,ADAM_beta2=0.999,ADAM_eps=1.E-7," // ADAM default parameters
                          "DropConfig=0.0+0.0+0.0+0.");
        //     TString training2("LearningRate=1e-3,Momentum=0.9"
        //                       "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
        //                       "MaxEpochs=20,WeightDecay=1e-4,Regularization=None,"
        //                       "Optimizer=SGD,DropConfig=0.0+0.0+0.0+0.");
 
        TString trainingStrategyString ("TrainingStrategy=");
        trainingStrategyString += training1; // + "|" + training2;
 
        // General Options.
 
        TString dnnOptions ("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=G:"
                            "WeightInitialization=XAVIER");
        dnnOptions.Append (":"); dnnOptions.Append (inputLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (batchLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (layoutString);
        dnnOptions.Append (":"); dnnOptions.Append (trainingStrategyString);
 
        TString dnnMethodName = "DNN_CPU";
        if (useDLGPU) {
            dnnOptions += ":Architecture=GPU";
            dnnMethodName = "DNN_GPU";
        } else  {
            dnnOptions += ":Architecture=CPU";
        }
 
        factory.BookMethod(dataloader,TMVA::Types::kDL, dnnMethodName, dnnOptions);
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
 
    // Train Methods: Here we train all the previously booked methods.
    cout << "\033[1;36m-------------------------------------- TRAINING... --------------------------------------\033[0m" << endl;
    factory.TrainAllMethods();
 
    // Test  all methods: Now we test and evaluate all methods using the test data set.
    cout << "\033[1;36m-------------------------------------- TESTING --------------------------------------\033[0m" << endl;
    factory.TestAllMethods();
    cout << "\033[1;36m-------------------------------------- EVALUATING --------------------------------------\033[0m" << endl;
    factory.EvaluateAllMethods();

    outfile->Close();
    std::cout << "==> Wrote root file: " << outfile->GetName() << std::endl;
    std::cout << "==> TMVARegression is done!" << std::endl;


    cout << "\033[1;36m-------------------------------------- DONE --------------------------------------\033[0m" << endl;
}
