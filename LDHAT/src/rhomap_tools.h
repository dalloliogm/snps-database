#if !defined TOOLS_H
#define TOOLS_H
#pragma warning(disable:4786) 
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <float.h>

#define SWAP(a,b) temp=(a);(a)=(b);(b)=temp;

const double PI=3.1415926535897932384626;

/*#define IM1 2147483563
#define IM2 2147483399
#define AM (1.0/IM1)
#define IMM1 (IM1-1)
#define IA1 40014
#define IA2 40692
#define IQ1 53668
#define IQ2 52774
#define IR1 12211
#define IR2 3791
#define NTAB 32
#define NDIV (1+IMM1/NTAB)
//#define EPS 1.2e-7
#define RNMX (1.0-EPS)
#define MAXIT 100
#define FPMIN 1.0e-30*/

const int IM1=2147483563;
const int  IM2=2147483399;
const double AM=(1.0/IM1);
const int  IMM1=(IM1-1);
const int IA1=40014;
const int IA2=40692;
const int IQ1=53668;
const int IQ2=52774;
const int IR1=12211;
const int IR2=3791;
const int NTAB=32;
const int NDIV=(1+IMM1/NTAB);
const int MAXIT=100;
const double FPMIN=1.0e-30;

__inline int mini(int i, int j) 
{
        if (i<j) return i;
        else return j; 
};

__inline int maxi(int i, int j) 
{
	if (i>j) return i;
	else return j;
};

__inline double mind(double d1, double d2)
{
  if (d1<d2) return d1;
  else return d2;
}

__inline double maxd(double d1, double d2)
{
  if (d1>d2) return d1;
  else return d2;
}

void nrerror(char error_text[]);
//int mini(int i, int j); 
//int maxi(int i, int j); 
float minc(float l1, float l2, float ls); 
float minf(float f1, float f2);
float maxf(float f1, float f2);
//double mind(double d1, double d2);
//double maxd(double d1, double d2);
double lnfac(int i);
void pswap(int *pt, int s1, int s2);
double lognC2();
double lognC4();
void sort();
long setseed();
double ran2();

extern __inline double Add_Log(double Summand1, double Summand2);
extern __inline double Subtract_Log(double Summand, double subtrahend);

double normrnd();
int poissrnd(double xm);
double gamrnd(double ia, double ib);
double gammln(double xx);
double log_gamma_pdf(double alpha, double beta, double x);
double exprnd(double mean);
double factorial(int n);
double gamma_function(int xx);
double betai(double a, double b, double x);
double betacf(double a, double b, double x);
double cumulative_binomial_prob(int success, int trials, double p);

double *dvector(int nh);
float *fvector(int nh);
double **dmatrix(int nrh, int nch);
float **fmatrix(int nrh, int nch);
int *ivector(int nh);
int **imatrix(int nrh, int nch);
void free_dvector(double *v);
void free_fvector(float *v);
void free_ivector(int *v);
void free_dmatrix(double **m, int nrh);
void free_fmatrix(float **m, int nrh);
void free_imatrix(int **m, int nrh);

int my_finite(double x);
void my_exit(char *message, int code);
float select(unsigned long k, unsigned long n, float *arr);
int compare (const void * a, const void * b);
float bi_weighted_mean(float *x, int xlen, int iterations);
float wmean(float *x, float *w, int xlen);

#endif


