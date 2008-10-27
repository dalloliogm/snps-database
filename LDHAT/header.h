#include <stdlib.h>
#include <math.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

float *vector();
float **matrix();
double *dvector();
double **dmatrix();
int *ivector();
int **imatrix();
char **cmatrix();
void free_vector();
void free_dvector();
void free_ivector();
void free_matrix();
void free_dmatrix();
void free_imatrix();
void free_cmatrix();
void nrerror();
int mini();
int maxi();
int minc();
void pswap();

int read_fasta();
void allele_count();
float watterson();
int check22();

long setseed();
float ran2();

void rec_test();
void ld_calc();
void fit_pwlk();

struct site_type ** pair_spectrum();
int add_type();
void print_pairs();
int * order_pt();
void lk_est();
void print_lks();
void lk_surf();
int lk_calc();
void type_print();
void print_par();
void read_pt();
struct site_type ** init_pset();
struct site_type ** add_pset();
float * read_pars();
void read_lk();
void print_lkres();
void ld_test();
void ld_calc2();

#define NSHUFF 1000
#define NRUN 1000000
#define ADD 100
#define SEQ_MAX 250
#define RHO_MAX 100.0
#define MAXNAME 30
#define MAXLINE 2000

struct site_type {

	int pt[4];
	int nt;
	float ld_stat[3];
};

struct data_sum {

	int nseq;
	int lseq;
	int tlseq;
	char lc;
	float avc;
	float rho;
	float lkmax;
	double ld[4];
	float rme;
	int rce;
};


