#if !defined SNPSIM_H
#define SNPSIM_H

struct node {
	int node_num;
	float time;
	struct node *d[2];
	struct node *a[2];
	int *asite;
	float rlen;
	int nuc;
};

struct results {
	int nrun;
	float nm;
	float pwd;
	float sn;
	float nr;
	double cf;
	double cf2;
};

struct control{
	int nsamp;
	int len;
	long int seed;
	float *theta;
	float *rmap;
	float R;
	int hyp;
	float phm;
	float rhm;
	float a;
	int mut;
	int inf;
	int nrun;
	int print;
	int fmin;
	int cond;
    int **slocs;
    int growth;
    float lambda;
	int bneck;
	float tb;
	float strb;
    double w0;
	int rm;
	float cl_fac;

};

#define BACC 1e-6


void snp_sim();
struct node ** make_tree();
void print_lin();
void  count_rlen();
void print_nodes();
void tree_summary();
struct node ** add_tree();
float tree_time();
int add_mut();
int add_mut_f();
void seq_mut();
void print_seqs();
char num_to_nuc();
int count_desc();
void choose_time();
float bisect();
float tgrowth();

void recombine();
void coalesce();

#endif


