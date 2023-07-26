#!/bin/bash

#root -l -q -b "TMVA_GF_regression.C(\"testing.root\", \"phi\", 0)"
root -l -q -b "TMVA_GF_regression_vars.C(\"testing.root\", \"phi\", 0, \"BDTG_var0\", (const char*[]){\"var0_input_pred\"}, 1)"
