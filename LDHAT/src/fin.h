#if !defined FIN_H
#define FIN_H

#define EVENT_PRINT 1

void print_help(int argc, char* argv[]);

struct node_tree {
	int node_num;
	int site;
	float time;
	float time_above;
	float time_below;
	int ndesc;
	struct node_tree *d[2];
	struct node_tree *a;
	int nuc;
};

struct node_list {
	int node_num;
	struct node_tree **asite;
	int nanc;
	double rlen;
	double time;
	int pop;
};


struct results {
	int nrun;
	float nm;
	float pwd;
	float sn;
	float nr;
	float mhm;
	double cf;
	double cf2;
	float *fdist;

	double covG[10];   /*For genealogical covariances*/
	double r2[3];
    double Dp;
	double G4;
	double cfld;
    double cfld2;
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
	int conv;
	float clen;
	float cratio;
	int asc;
  int gt;
  float rescale;	// Rescale output loci file
};

#define BACC 1e-6

struct node_tree *** make_tree();
void set_res();
void print_lin();
void  count_rlen();
void print_nodes();
void tree_summary();
float tree_time();
int add_mut();
struct node_tree * add_mut_f();
void seq_mut();
void print_seqs();
void print_res();
void read_input();
void read_flags();
void select_base();
void evolve();
char num_to_nuc();
int count_desc();

void choose_time();
double bisect();
double tgrowth();

struct node_list ** recombine();
struct node_list ** coalesce();

void check_lin();

#endif


