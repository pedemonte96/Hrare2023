#!/bin/bash

nohup bash autotrain.sh "phi" 0 "BDTG_AB_13" "!V:NTrees=1820:BoostType=Grad:Shrinkage=0.67532:MaxDepth=6:SeparationType=MisClassificationError:nCuts=99:UseRandomisedTrees=F:UseNvars=85:UseBaggedBoost:BaggedSampleFraction=1.35521:PruneMethod=ExpectedError:PruneStrength=60:PruningValFraction=0.92973"
nohup bash autotrain.sh "phi" 1 "BDTG_AB_13" "!V:NTrees=1820:BoostType=Grad:Shrinkage=0.67532:MaxDepth=6:SeparationType=MisClassificationError:nCuts=99:UseRandomisedTrees=F:UseNvars=85:UseBaggedBoost:BaggedSampleFraction=1.35521:PruneMethod=ExpectedError:PruneStrength=60:PruningValFraction=0.92973"
nohup bash autotrain.sh "phi" 2 "BDTG_AB_13" "!V:NTrees=1820:BoostType=Grad:Shrinkage=0.67532:MaxDepth=6:SeparationType=MisClassificationError:nCuts=99:UseRandomisedTrees=F:UseNvars=85:UseBaggedBoost:BaggedSampleFraction=1.35521:PruneMethod=ExpectedError:PruneStrength=60:PruningValFraction=0.92973"

nohup bash autotrain.sh "phi" 0 "BDTG_AB_23" "!V:VarTransform=P:NTrees=2407:BoostType=Grad:Shrinkage=0.5284:MaxDepth=5:SeparationType=GiniIndex:nCuts=50:UseRandomisedTrees=F:UseNvars=30:UseBaggedBoost:BaggedSampleFraction=2.30715:PruneMethod=ExpectedError:PruneStrength=13:PruningValFraction=0.89482"
nohup bash autotrain.sh "phi" 1 "BDTG_AB_23" "!V:VarTransform=P:NTrees=2407:BoostType=Grad:Shrinkage=0.5284:MaxDepth=5:SeparationType=GiniIndex:nCuts=50:UseRandomisedTrees=F:UseNvars=30:UseBaggedBoost:BaggedSampleFraction=2.30715:PruneMethod=ExpectedError:PruneStrength=13:PruningValFraction=0.89482"
nohup bash autotrain.sh "phi" 2 "BDTG_AB_23" "!V:VarTransform=P:NTrees=2407:BoostType=Grad:Shrinkage=0.5284:MaxDepth=5:SeparationType=GiniIndex:nCuts=50:UseRandomisedTrees=F:UseNvars=30:UseBaggedBoost:BaggedSampleFraction=2.30715:PruneMethod=ExpectedError:PruneStrength=13:PruningValFraction=0.89482"

nohup bash autotrain.sh "phi" 0 "BDTG_AB_35" "!V:VarTransform=D:NTrees=1220:BoostType=Grad:Shrinkage=0.08311:MaxDepth=6:SeparationType=RegressionVariance:nCuts=95:UseRandomisedTrees=F:UseNvars=73:UseBaggedBoost:BaggedSampleFraction=3.02759:PruneMethod=ExpectedError:PruneStrength=72:PruningValFraction=1.56143"
nohup bash autotrain.sh "phi" 1 "BDTG_AB_35" "!V:VarTransform=D:NTrees=1220:BoostType=Grad:Shrinkage=0.08311:MaxDepth=6:SeparationType=RegressionVariance:nCuts=95:UseRandomisedTrees=F:UseNvars=73:UseBaggedBoost:BaggedSampleFraction=3.02759:PruneMethod=ExpectedError:PruneStrength=72:PruningValFraction=1.56143"
nohup bash autotrain.sh "phi" 2 "BDTG_AB_35" "!V:VarTransform=D:NTrees=1220:BoostType=Grad:Shrinkage=0.08311:MaxDepth=6:SeparationType=RegressionVariance:nCuts=95:UseRandomisedTrees=F:UseNvars=73:UseBaggedBoost:BaggedSampleFraction=3.02759:PruneMethod=ExpectedError:PruneStrength=72:PruningValFraction=1.56143"