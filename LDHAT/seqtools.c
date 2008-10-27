#include "./header.h"

int sizeofpset=100;

int read_fasta(seqs,ifp,nseq,lseq,seqnames) 
int **seqs, nseq, lseq;
char **seqnames;
FILE *ifp;
{

	int i, site, seq=0, cts[5];
	char line[MAXLINE], *c, bases[5]="TCAG-";
	
	printf("\n\nReading sequences in fasta format\n\n");
	for (i=0;i<5;i++) cts[i]=0;


	while (!feof(ifp) && (seq<nseq)) {
		fgets(line, MAXLINE, ifp);
		if ((c = (char *) strchr(line, '>')) != NULL) {
			seq++;
			printf("Sequence :%3i ", seq);
			strncpy(seqnames[seq], (c+1), MAXNAME);
			for (i=1;i<=MAXNAME;i++) if(seqnames[seq][i]=='\n') seqnames[seq][i]='\0';
			printf("%s: ", seqnames[seq]);
			site=1;
			while (site<=lseq) {
				fgets(line, MAXLINE, ifp);
				for (c=line; (*c)!='\0'; c++) {
				   switch(*c) {
					case 'T': case 't': case '0': {
						seqs[seq][site] = 2;
						site++;
						cts[0]++;
						break;
					}
					case 'C': case 'c': case '1': {
						seqs[seq][site] = 3;
						site++;
						cts[1]++;
						break;
					}
					case 'A': case 'a': case '2': {
						seqs[seq][site] = 4;
						site++;
						cts[2]++;
						break;
					}
					case 'G': case 'g': case '3' :{
						seqs[seq][site] = 5;
						site++;
						cts[3]++;
						break;
					}
					case'-': case'N': case'n': case'?': case'R': case'Y': case'M': case'K': case'S': case'W': case'H': case'B': case'V': case'D' :{
						seqs[seq][site]=1;
						site++;
						cts[4]++;
						break;
					}
					case '>': {printf("\nError in sequence file(%i of %i bases read)\n",site,lseq); exit(1);}
					default: {
						break;
					}
				   }
				}
			}
			if (site-1 != lseq) {printf("\nSequences incorrect length (%i)\n\n",site-1); exit(1);}
			for (i=0;i<5;i++) printf("%c:%5i ",bases[i], cts[i]);
			printf("\n");
		}
	}
	if (seq!=nseq) {printf("\n\nDid not read %i sequences \n\n",nseq); exit(1);}
	return 1;
}


void allele_count(seqs,nseq,lseq,nall) 
int **seqs,nseq,lseq,**nall;
{
        
        int seq, site, i;
        
        for (site=1; site<=lseq; site++) for(i=1; i<=6; i++) nall[site][i]=0;
        for (seq=1; seq<=nseq; seq++) for (site=1; site<=lseq; site++) nall[site][seqs[seq][site]]++;
        printf("\nAllele frequencies\n\n Site   -   T/0  C/1  A/2  G/3\n\n");
        for (site=1; site<=lseq; site++) {
                printf("%4i ", site);
                for (i=1; i<=5; i++) printf("%4i ", nall[site][i]);
                printf("\n");
        } 
}

float watterson(n) 
int n;
{

	int i;
	float cump=1;

	for (i=2;i<n;i++) cump+=(float) 1/i;
	return cump;
}

int check22(s1,s2,nall) 
int s1,s2,**nall;
{
                        
        int i, na;

/*Commenting out this line allows the use of missing data*/
/*	if (nall[s1][1] || nall[s2][1]) return 0;*/

        for (na=0, i=2; i<=5; i++) if (nall[s1][i]>0) na++;
        if (na != 2) return 0;
        for (na=0, i=2; i<=5; i++) if (nall[s2][i]>0) na++;
        if (na != 2) return 0;
                           
        return 1; 
}



/* Routine to classify each pairwise comparison*/


struct site_type ** pair_spectrum(seqs,data,nall,pset,npt,new,anc,pij) 
int **seqs,**nall,*npt,*new,anc,**pij;
struct data_sum *data;
struct site_type **pset;
{

	int i, j, seq, sites[2], states[2][2], *pt;
	char bases[6]="n-TCAG";

	printf("\n\nCalculating distribution of pair types\n\n");

	pt  = (int *) malloc((size_t) 4*sizeof(int));

	for (sites[0]=1; sites[0]<data->lseq; sites[0]++) {
		for (sites[1]=sites[0]+1; sites[1]<=data->lseq; sites[1]++) {
			if (!check22(sites[0], sites[1], nall)) pij[sites[0]][sites[1]]=0; 
			else {
			   for (i=0; i<4; i++) pt[i]=0;
			   for (j=0; j<2; j++) {
				for (i=2; i<=5; i++) if (nall[sites[j]][i]) {states[j][0]=i;break;}
				for (i++; i<=5; i++) if (nall[sites[j]][i]) {states[j][1]=i;break;}
			   }
			   for (seq=1; seq<=data->nseq; seq++) {
				if (seqs[seq][sites[0]]==states[0][0]) {
					if (seqs[seq][sites[1]]==states[1][0]) pt[3]++;
					else if (seqs[seq][sites[1]]==states[1][1]) pt[2]++;
				}
				else if (seqs[seq][sites[0]]==states[0][1]) {
					if (seqs[seq][sites[1]]==states[1][0]) pt[1]++;
					else if (seqs[seq][sites[1]]==states[1][1]) pt[0]++;
				}
			   }
			   if (anc == 0) pt = order_pt(pt, &(data->nseq));
			   if ((pt[1]+pt[3]==0)||(pt[2]+pt[3]==0)) pij[sites[0]][sites[1]]=0;
			   else {
			   	if ((*npt)+(*new)+10>sizeofpset) pset = add_pset(pset);
			   	i=add_type(pset, pt, npt, new);
			   	pij[sites[0]][sites[1]]=i;
			   }
			}
		}
	}
	free(pt);
	return pset;
}


/*Routine to add new pair type to existing set*/

int add_type(pset,cpt,ntc,new) 
int *cpt,*ntc,*new;
struct site_type **pset;
{

	int t, fl, i, j;
	extern int sizeofpset;

	for (t=1; t<=(*ntc)+(*new); t++) {
		for (i=0, fl=1; i<4; i++) if (pset[t]->pt[i] != cpt[i]) {fl=0; break;}
		if (fl==1) {
			pset[t]->nt++;
			return t;
		}
	}
	for (i=0; i<4; i++) pset[t]->pt[i]=cpt[i];
	pset[t]->nt=1;
	(*new)++;
	return t;
}


void print_pairs(ofp,pset,nt) 
int nt;
FILE *ofp;
struct site_type **pset;
{

	int t, i;

	fprintf(ofp,"\nPrinting pair types\n\nType   00   01   10   11 \n\n");
	for (t=1; t<=nt; t++) {
	   if (pset[t]->nt) {
		fprintf(ofp,"%4i ",t);
		for (i=0; i<4; i++) fprintf(ofp,"%4i ", pset[t]->pt[i]);
		fprintf(ofp,": %5i ",pset[t]->nt);
		fprintf(ofp, "\n");
	   }
	}
}



int * order_pt(pt,nsamp) 
int *pt, *nsamp;
{
	int fl=0;
	if (2*(pt[2]+pt[3]) > (*nsamp)) fl += 2;
	if (2*(pt[1]+pt[3]) > (*nsamp)) fl += 1;
	switch(fl) {
		case 0 : {
			break;
		}
		case 1 : {
			pswap(pt,0,1);
			pswap(pt,2,3);
			break;
		}
		case 2 : {
			pswap(pt, 0, 2);
			pswap(pt, 1, 3);
			break;
		}
		case 3 : {
			pswap(pt,0,3);
			pswap(pt,1,2);
			break;
		}
		default : {
			printf("\n\nError in sorting\n\n");
			exit(1);
		}
	}

/*Next Line must commented out if use multiple mutation rates*/

	if (pt[2]>pt[1]) pswap(pt,1,2);
	return pt;
}


void type_print(pij,lseq) 
int **pij, lseq;
{

	int i, j;
	FILE *ofp;

	ofp = fopen("type_table", "w");
	if (!ofp) nrerror("Cannot open type-table");

	fprintf(ofp,"Pair types\n\n        ");
        for (i=1; i<lseq; i++) fprintf(ofp, " %3i", i+1);
        for (i=1; i<lseq; i++) {
                fprintf(ofp,"\n%3i:", i);
                for (j=1; j<=i; j++) fprintf(ofp,"    ");
                for (j=i+1; j<=lseq; j++) fprintf(ofp," %3i", pij[i][j]);
        }
	fclose(ofp);
}



void read_pt(ifp,pset,npt) 
int *npt;
FILE *ifp;
struct site_type **pset;
{

	int p=1, i;
	char c;

	printf("\n\nReading data for pair types\n\n");
	while((c=fgetc(ifp)) != EOF)
	if (c == '#') {
		if ((p%50) == 0) printf("\n");
		printf(".");
		for (i=0; i<4; i++) fscanf(ifp, "%i", &pset[p]->pt[i]);	
		p++;
	}
	if ((*npt) != p-1) {
		printf("\nWarning: No. entries in Likelihood file does not match total (%i)\n\n",p-1); 
		exit(1);
	}
}



struct site_type ** init_pset(pset,lkf,ifp,npt,nseq) 
int lkf, *npt, nseq;
FILE *ifp;
struct site_type **pset;
{

	int i, j, nsfile;
	struct site_type *new_pt;
	extern int sizeofpset;

	if (lkf) {
		fscanf(ifp,"%i %i", &nsfile, &(*npt));
		if (nsfile != nseq) {printf("\nLikelihood file for different no. seqs than data\n\n"); exit(1);}
		sizeofpset = (*npt) + ADD;
	}

	pset = (struct site_type **) malloc((size_t) sizeofpset*sizeof(struct site_type *));
        for (i=1;i<sizeofpset;i++) {
                new_pt = (struct site_type *) malloc((size_t) sizeof(struct site_type));
                pset[i] = new_pt;
        }

        if (lkf) {
                read_pt(ifp, pset, npt);
		rewind(ifp);
        }

	for (i=1;i<sizeofpset;i++) {
		pset[i]->nt=0;
		for (j=0;j<3;j++) pset[i]->ld_stat[j]=0.0;
		if ((!lkf) || (i>(*npt))) for (j=0;j<4;j++) pset[i]->pt[j]=0;
	}
	return pset;
}



struct site_type ** add_pset(pset) 
struct site_type **pset;
{

	int i, j;
	extern int sizeofpset;
	struct site_type **npset, *new_pt;

/*	printf(" :New memory for pset: %i plus %i", sizeofpset, ADD); */
        npset = (struct site_type **) malloc((size_t) ((int) sizeofpset+ADD)*sizeof(struct site_type *));
        if (npset == NULL) {printf("\nError in reallocation\n"); exit(1);}
        for (i=1;i<sizeofpset;i++) npset[i]=pset[i];
        for (i=sizeofpset; i<(sizeofpset+ADD); i++) {
                        new_pt = (struct site_type *) malloc((size_t) sizeof(struct site_type));
			if (new_pt==NULL) {printf("\noom\n\n"); exit(1);}
                        for (j=0; j<4; j++) new_pt->pt[j]=0;
			for (j=0; j<3; j++) new_pt->ld_stat[j]=0.0;
                        new_pt->nt=0;
			npset[i] = new_pt;
        }
        sizeofpset += ADD; 
        free(pset);
	pset = npset;	

	return pset;
}



float * read_pars(ifp,tcat,theta,rcat,rmax) 
int *tcat, *rcat;
float *theta, *rmax;
FILE *ifp;
{

	int i, ns, npt;

	fscanf(ifp, "%i %i", &ns, &npt);
	fscanf(ifp, "%i", &(*tcat));
	theta = vector(1, (int) (*tcat));
	for (i=1;i<=(*tcat);i++) fscanf(ifp,"%f", &theta[i]);
	fscanf(ifp, "%i", &(*rcat));
	fscanf(ifp,"%f", &(*rmax));

	return theta;
}


void read_lk(ifp,lkmat,npt,tcat,rcat) 
int npt, tcat, rcat;
float **lkmat;
FILE *ifp;
{

	int p=1, i, j, k, pc[4];
	char c;

	printf("\n\nReading likelihoods for pair types\n");
	while((c=fgetc(ifp)) != EOF)
		if (c == ':') {
			if ((p%50) == 0) printf("\n");
			printf(".");
			for (i=0; i<tcat; i++)
				for (j=0; j<tcat; j++)
					for (k=1; k<=rcat; k++) fscanf(ifp,"%f", &lkmat[p][i*tcat*rcat+j*rcat+k]);
			p++;
		}
	if (p-1 != npt) {printf("\n\nLikelihood file does not agree with header\n\n"); exit(1);}
	fclose(ifp);
}



