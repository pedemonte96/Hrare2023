1. First train all models with different variables to create weight files:
    - Fill name:command in `commmands_tmva.txt`. This is going to call the `TMVA_GF_regression_vars.C` file.
    - run `python slurm.py -i commands_tmva.txt`

2. Evaluate all models:
    - Fill name:command in `commands_evaluate.txt` (e.g. `eval_BDTG_NONE:python computeErrors.py -m BDTG_NONE`)
    - run `python slurm.py -i commands_evaluate.txt`
3. Join results:
    - Run `bash evaluationAllVars.sh`
4. With python analyse the recently created file `evaluationAllVars.out`.