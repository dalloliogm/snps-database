#include "./header.h"

void nrerror(error_text)
char error_text[];
{
	void exit();

	fprintf(stderr,"Numerical Recipes run-time error...\n");
	fprintf(stderr,"%s\n",error_text);
	fprintf(stderr,"...now exiting to system...\n");
	exit(1);
}



float *vector(nl,nh)
int nl,nh;
{
	float *v;

	v=(float *)malloc((unsigned) (nh-nl+1)*sizeof(float));
	if (!v) nrerror("allocation failure in vector()");
	return v-nl;
}

int *ivector(nl,nh)
int nl,nh;
{
	int *v;

	v=(int *)malloc((unsigned) (nh-nl+1)*sizeof(int));
	if (!v) nrerror("allocation failure in ivector()");
	return v-nl;
}

double *dvector(nl,nh)
int nl,nh;
{
	double *v;

	v=(double *)malloc((unsigned) (nh-nl+1)*sizeof(double));
	if (!v) nrerror("allocation failure in dvector()");
	return v-nl;
}



float **matrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
	int i;
	float **m;

	m=(float **) malloc((unsigned) (nrh-nrl+1)*sizeof(float*));
	if (!m) nrerror("allocation failure 1 in matrix()");
	m -= nrl;

	for(i=nrl;i<=nrh;i++) {
		m[i]=(float *) malloc((unsigned) (nch-ncl+1)*sizeof(float));
		if (!m[i]) nrerror("allocation failure 2 in matrix()");
		m[i] -= ncl;
	}
	return m;
}

double **dmatrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
	int i;
	double **m;

	m=(double **) malloc((unsigned) (nrh-nrl+1)*sizeof(double*));
	if (!m) nrerror("allocation failure 1 in dmatrix()");
	m -= nrl;

	for(i=nrl;i<=nrh;i++) {
		m[i]=(double *) malloc((unsigned) (nch-ncl+1)*sizeof(double));
		if (!m[i]) nrerror("allocation failure 2 in dmatrix()");
		m[i] -= ncl;
	}
	return m;
}

int **imatrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
	int i,**m;

	m=(int **)malloc((unsigned) (nrh-nrl+1)*sizeof(int*));
	if (!m) nrerror("allocation failure 1 in imatrix()");
	m -= nrl;

	for(i=nrl;i<=nrh;i++) {
		m[i]=(int *)malloc((unsigned) (nch-ncl+1)*sizeof(int));
		if (!m[i]) nrerror("allocation failure 2 in imatrix()");
		m[i] -= ncl;
	}
	return m;
}

char **cmatrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
        int i;
	char **m;

        m=(char **)malloc((unsigned) (nrh-nrl+1)*sizeof(char*));
        if (!m) nrerror("allocation failure 1 in cmatrix()");
        m -= nrl;

        for(i=nrl;i<=nrh;i++) {
                m[i]=(char *)malloc((unsigned) (nch-ncl+1)*sizeof(char));
                if (!m[i]) nrerror("allocation failure 2 in cmatrix()");
                m[i] -= ncl;
        }
        return m; 
}


void free_vector(v,nl,nh)
float *v;
int nl,nh;
{
	free((char*) (v+nl));
}

void free_ivector(v,nl,nh)
int *v,nl,nh;
{
	free((char*) (v+nl));
}

void free_dvector(v,nl,nh)
double *v;
int nl,nh;
{
	free((char*) (v+nl));
}



void free_matrix(m,nrl,nrh,ncl,nch)
float **m;
int nrl,nrh,ncl,nch;
{
	int i;

	for(i=nrh;i>=nrl;i--) free((char*) (m[i]+ncl));
	free((char*) (m+nrl));
}

void free_dmatrix(m,nrl,nrh,ncl,nch)
double **m;
int nrl,nrh,ncl,nch;
{
	int i;

	for(i=nrh;i>=nrl;i--) free((char*) (m[i]+ncl));
	free((char*) (m+nrl));
}

void free_imatrix(m,nrl,nrh,ncl,nch)
int **m;
int nrl,nrh,ncl,nch;
{
	int i;

	for(i=nrh;i>=nrl;i--) if ((m[i]+ncl) != NULL) free((char*) (m[i]+ncl));
	if ((m+nrl) != NULL) free((char*) (m+nrl));
}

        
void free_cmatrix(m,nrl,nrh,ncl,nch)
char **m;
int nrl,nrh,ncl,nch;
{
        int i;
 
        for(i=nrh;i>=nrl;i--) if ((m[i]+ncl) != NULL) free((char*) (m[i]+ncl));
        if ((m+nrl) != NULL) free((char*) (m+nrl));
}



int mini(i,j) 
int i,j;
{
        if (i<j) return i;
        else return j; 
}

int maxi(i,j) 
int i,j;
{
	if (i>j) return i;
	else return j;
}


int minc(l1,l2,ls) 
int l1,l2,ls;
{
        
        int d;
        if ((d=(l2-l1)) > (int) ((float) ls/2)) d = (int) ls-l2+l1;
        return d; 
}


void pswap(pt,s1,s2) 
int *pt,s1,s2;
{
                 
        int tmp;
                 
        tmp = pt[s2];
        pt[s2]=pt[s1];
        pt[s1]=tmp; 
}

