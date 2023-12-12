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

void TMVA_GF_TO ( const char* outFileName,
                  const char* channel,
                  int testSet=0 )
{
    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 25;
    
    // options to control used methods
    bool useRandomSplitting = false; // option for cross validation
    bool useLikelihood = true;    // likelihood based discriminant
    bool useLikelihoodKDE = false;    // likelihood based discriminant
    bool useFischer = false;       // Fischer discriminant
    bool useMLP = false;          // Multi Layer Perceptron (old TMVA NN implementation)
    bool useBDT = false;           // Boosted Decision Tree (AdaBoost)
    bool useBDTG = false;         // BDT with GradBoost
    bool useDL = false;           // TMVA Deep Learning ( CPU or GPU)
    // bool useKeras = false;        // Keras Deep learning
    
    // Open files
    TString fileformat;
    TFile* sgnfile;
    TFile* bkgfile;
    if ( std::strcmp(channel, "phi") == 0 ) {
        //
    } else if ( std::strcmp(channel, "rho") == 0 ) {
        sgnfile = TFile::Open("/work/submit/kyoon/RareHiggs/Torino/mva/OCT2/GF_Rho/histos_SR_preselection_SignalggH.root", "READ");
        bkgfile = TFile::Open("/work/submit/kyoon/RareHiggs/Torino/mva/OCT2/GF_Rho/histos_CR_preselection_Sidebands.root", "READ");
    } else if ( std::strcmp(channel, "k0star") == 0 ) {
        //
    }
    
    // Initialize the dataset
    TFile* outfile = TFile::Open(outFileName, "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");
    
    // Add variables to dataset
    dataloader->AddVariable("_firstTrkIsoCh", "_firstTrkIsoCh", "", 'F');
    dataloader->AddVariable("_coupleIso0", "_coupleIso0", "", 'F');
    dataloader->AddVariable("_bestCouplePt/mesonGammaMass", "_bestCouplePt__div_mesonGammaMass", "", 'F');
    dataloader->AddVariable("_photonEt/mesonGammaMass", "_photonEt__div_mesonGammaMass", "", 'F');
    // dataloader->AddVariable("mesonGammaMass", "mesonGammaMass", "", 'F');
    
    // Set weights
    dataloader->SetWeightExpression("_BDTweight");

    // Spectator used for split
    // dataloader->AddSpectator("Entry$", "eventID");

    // Apply split
    ////////////////////// TODO: use cross validation /////////////////////////
    const char* trainTreeEventSplitStr = Form("(Entry$ %% 2) == %d", testSet);
    const char* testTreeEventSplitStr = Form("(Entry$ %% 2) != %d", testSet); // "(Entry$) >= 0"; 
    
    // Apply cuts
    const char* higgsMass_full = "mesonGammaMass > 115 && mesonGammaMass < 135";
    
    TCut cutSignalTrain = Form("%s && %s", trainTreeEventSplitStr, higgsMass_full);
    TCut cutBkgTrain = Form("%s && %s", trainTreeEventSplitStr, higgsMass_full);
    TCut cutSignalTest = Form("%s && %s", testTreeEventSplitStr, higgsMass_full);
    TCut cutBkgTest = Form("%s && %s", testTreeEventSplitStr, higgsMass_full);

    // Register trees
    ///////////////////// TODO: add weight per event basis /////////////////////
    double signalWeight = 1.0;
    double backgroundWeight = 1.0;
    
    dataloader->AddTree((TTree*)sgnfile->Get("tree_output"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)bkgfile->Get("tree_output"), "Background", backgroundWeight, cutBkgTrain, "train");
    
    dataloader->AddTree((TTree*)sgnfile->Get("tree_output"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)bkgfile->Get("tree_output"), "Background", backgroundWeight, cutBkgTest, "test");
    
    TMVA::Factory factory("TMVAClassification", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification:Transformations=P,D");

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
    // Prepare training and test trees
    TString prepareOptions = "NormMode=None";
    prepareOptions+=":SplitMode=random:!V";
    prepareOptions+=":MixMode=Random";
    dataloader->PrepareTrainingAndTestTree("", prepareOptions);

    /*
        ## Booking Methods
 
        Here we book the TMVA methods. We book first a Likelihood based on KDE (Kernel Density Estimation), a Fischer discriminant, a BDT
        and a shallow neural network
 
    */
 
    // Likelihood ("naive Bayes estimator")
    if (useLikelihood)
    {
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "Likelihood",
                           "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );
    }
    // Use a kernel density estimator to approximate the PDFs
    if (useLikelihoodKDE)
    {
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "LikelihoodKDE",
                      "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" );
 
    }
 
    // Fisher discriminant (same as LD)
    if (useFischer)
    {
        factory.BookMethod(dataloader,TMVA::Types::kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" );
    }
 
    // Boosted Decision Trees
    if (useBDT)
    {
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA_TO",
                           "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA1",
        //                    "!V:VarTransform=P,D:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA2",
        //                    "!V:VarTransform=D:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    }

    if (useBDTG)
    {
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG1",
                           "!V:VarTransform=P,D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG2",
        //                    "!V:VarTransform=D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG3",
        //                    "!V:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG4",
        //                    "!V:VarTransform=P,D:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG5",
        //                    "!V:VarTransform=D:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG6",
        //                    "!V:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_depth4_with_pruning",
        //                    "!V:VarTransform=P,D:NTrees=100:BoostType=Grad:Shrinkage=0.06:MaxDepth=4:SeparationType=GiniIndex:nCuts=15:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=CostComplexity:PruneStrength=80" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
        //                    "!V:VarTransform=P,D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=NoPruning" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_d3",
        //                   "!V:NTrees=600:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.6:PruneMethod=CostComplexity:PruneStrength=60" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG__rho",
        //                  "!V:NTrees=100:BoostType=Grad:Shrinkage=0.1:MaxDepth=2:SeparationType=GiniIndex:nCuts=30:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.15" );
    }
 
    // Multi-Layer Perceptron (Neural Network)
    if (useMLP)
    {
        factory.BookMethod(dataloader,TMVA::Types::kMLP, "MLP",
                      "!H:!V:NeuronType=tanh:VarTransform=N:NCycles=100:HiddenLayers=N+5:TestRate=5:UseRegulator" );
    }

    // Deep Neural Network
    if (useDL)
    {
 
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
 
    /*
      ## Train Methods
      Here we train all the previously booked methods.
    */
 
    factory.TrainAllMethods();
 
    /*
      ## Test  all methods
      Now we test and evaluate all methods using the test data set
    */
    
    factory.TestAllMethods();
    factory.EvaluateAllMethods();
    // cv.Evaluate();
 
    // after we get the ROC curve and we display
    // auto c1 = factory.GetROCCurve(dataloader);
    // c1->Draw();
}
