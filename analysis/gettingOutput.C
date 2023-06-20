#include <iostream>

void gettingOutput(const char *path)
{
	printf("%s", path);
	TFile *f=new TFile(path);
	f->Get("Events")->Print();
}
