#include <iostream>

void gettingOutput()
{
	TFile *f=new TFile("/work/submit/mariadlf/Hrare/D02/2018/ggh-hD0Stargamma-powheg/NANOAOD_02/step7_ggH_HD0StarGamma_9.root");
	//TFile *f=new TFile("/work/submit/mariadlf/Hrare/D02/2018/ggh-hphipipipi0gamma-powheg_03_test2/NANOAOD_03_test2/step7_ggH_Phi3Gamma_9.root");
	f->Get("Events")->Print();

}
