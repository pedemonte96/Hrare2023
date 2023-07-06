
## Create histograms
Requisits:
* Python 3.11
* ROOT 6.28

`python3 createHistogramFiles.py`

Will create all the histograms in `/data/submit/pdmonte/outHistsFits/`.


## Fit histograms and create workspaces
In cmsenv (python 2.7.14, ROOT 6.14):

`python SIGfits.py` (for the signal)

`python BKGfits.py` (for background)


## Create datacards and compute asymptotic limits
In cmsenv:

`bash combineCommand.sh`