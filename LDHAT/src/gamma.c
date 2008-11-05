#include <math.h>
#include "gamma.h"
#include "nrutil.h"

float gammln(xx)
float xx;
{
	double x,tmp,ser;
	static double cof[6]={76.18009173,-86.50532033,24.01409822,
		-1.231739516,0.120858003e-2,-0.536382e-5};
	int j;

	x=xx-1.0;
	tmp=x+5.5;
	tmp -= (x+0.5)*log(tmp);
	ser=1.0;
	for (j=0;j<=5;j++) {
		x += 1.0;
		ser += cof[j]/x;
	}
	return -tmp+log(2.50662827465*ser);
}


void gcf(gammcf,a,x,gln)
float a,x,*gammcf,*gln;
{
	int n;
	float gold=0.0,g,fac=1.0,b1=1.0;
	float b0=0.0,anf,ana,an,a1,a0=1.0;
	float gammln();
	void nrerror();

	*gln=gammln(a);
	a1=x;
	for (n=1;n<=ITMAX;n++) {
		an=(float) n;
		ana=an-a;
		a0=(a1+a0*ana)*fac;
		b0=(b1+b0*ana)*fac;
		anf=an*fac;
		a1=x*a0+anf*a1;
		b1=x*b0+anf*b1;
		if (a1) {
			fac=1.0/a1;
			g=b1*fac;
			if (fabs((g-gold)/g) < EPSg) {
				*gammcf=exp(-x+a*log(x)-(*gln))*g;
				return;
			}
			gold=g;
		}
	}
	nrerror("a too large, ITMAX too small in routine GCF");
}


void gser(gamser,a,x,gln)
float a,x,*gamser,*gln;
{
	int n;
	float sum,del,ap;
	float gammln();
	void nrerror();

	*gln=gammln(a);
	if (x <= 0.0) {
		if (x < 0.0) nrerror("x less than 0 in routine GSER");
		*gamser=0.0;
		return;
	} else {
		ap=a;
		del=sum=1.0/a;
		for (n=1;n<=ITMAX;n++) {
			ap += 1.0;
			del *= x/ap;
			sum += del;
			if (fabs(del) < fabs(sum)*EPSg) {
				*gamser=sum*exp(-x+a*log(x)-(*gln));
				return;
			}
		}
		nrerror("a too large, ITMAX too small in routine GSER");
		return;
	}
}


float gammp(a,x)
float a,x;
{
	float gamser,gammcf,gln;
	void gser(),gcf(),nrerror();

	if (x < 0.0 || a <= 0.0) nrerror("Invalid arguments in routine GAMMP");
	if (x < (a+1.0)) {
		gser(&gamser,a,x,&gln);
		return gamser;
	} else {
		gcf(&gammcf,a,x,&gln);
		return 1.0-gammcf;
	}
}

float gammq(a,x)
float a,x;
{
	float gamser,gammcf,gln;
	void gcf(),gser(),nrerror();

	if (x < 0.0 || a <= 0.0) nrerror("Invalid arguments in routine GAMMQ");
	if (x < (a+1.0)) {
		gser(&gamser,a,x,&gln);
		return 1.0-gamser;
	} else {
		gcf(&gammcf,a,x,&gln);
		return gammcf;
	}
}

float rgamm(a) 
float a;
{

	int i;
	extern long int *idum;
	float r, c[3], x[3];

	r = ran2();
	for (i=0;i<3;i++) {x[i]=(float) i*a; c[i]=gammp(a,x[i]);}
	while ((c[2]-c[0])>ACC) {
	    if (c[1]>r) {x[2]=x[1];c[2]=c[1];}
	    else  {x[0]=x[1]; c[0]=c[1];}
	    x[1]=(x[2]+x[0])/2;
	    c[1]=gammp(a,x[1]);
	}
	return (float) x[1]/a;
}

	
