#include "./header.h"
#include "./random.cc"
#include "./rtest.cc"

long *idum;

main (int argc, char *argv[]) {

	int i, j, **seqs, **nall, ord=1, *locs, ns, **pij, lkf=0, npt=0, new=0, anc=0;
	int tcat=1, rcat=0, verb=1;
	char fname[MAXNAME], **seqnames;
	long seed=-setseed();
	extern int sizeofpset;
	float **lkmat, *theta, rmax, tmp;
	FILE *ifp;
	struct site_type **pset, *new_pt;
	struct data_sum *data;

	idum = &seed;

	if (argc > 1) ifp = fopen(argv[1], "r"); 
	else {
		printf("\n\nInput filename for seqs\n\n");
		scanf("%s", &fname);
		ifp = fopen(fname, "r");
	}
	if (ifp == NULL) nrerror("Error in opening sequence file");

	data = malloc((size_t) sizeof(struct data_sum));
	fscanf(ifp,"%i%i", &data->nseq, &data->lseq);
	if ((data->nseq < 2) || (data->lseq < 2)) {printf("\n\nInsufficient data for analysis (n > 1, L > 1) \n\n"); exit(1);}
	if (data->nseq > SEQ_MAX) {printf("\n\nMore than max no. sequences: Using first %i for analysis\n\n", SEQ_MAX); data->nseq=SEQ_MAX;}
	printf("\nAnalysing %i sequences of length %i seg sites\n", data->nseq, data->lseq);
	seqs = imatrix(1, data->nseq, 1, data->lseq);
	seqnames = cmatrix(1, data->nseq, 1, MAXNAME);
	if (read_fasta(seqs, ifp, data->nseq, data->lseq, seqnames)) printf("\nSequences read succesfully\n");
	fclose(ifp);

	nall = imatrix(1, data->lseq, 1, 6);
	allele_count(seqs, data->nseq, data->lseq, nall);

	if (argc > 2) ifp = fopen(argv[2], "r");
	else {
		printf("\nInput name of file containing location of seg sites\n\n");
		scanf("%s", &fname);
		ifp = fopen(fname, "r");
	}
	if (ifp == NULL) nrerror("Cannot open loc file");
	fscanf(ifp, "%i %i %c", &ns, &data->tlseq, &data->lc);
	if (ns != data->lseq) nrerror("Lseq and Locs disagree");
	if ((data->lc != 'C')&&(data->lc != 'L')) nrerror("Must input linear/circular");
	if (data->lc == 'C') {
	  data->avc=0;
	  while (data->avc <= 0) {
	    printf("\n\nInput average tract length for conversion model: ");scanf("%f", &(data->avc));
	  }}
	locs = ivector(1, data->lseq);
	for (i=1; i<=data->lseq; i++) {
		fscanf(ifp, "%i", &locs[i]); 
		if ((locs[i]==0)||(locs[i]>data->tlseq)) {printf("\n\nError in Loc file\n\n"); exit(1);}}
	printf("\nLocation of seg sites\n\n");
	for (i=1; i<=data->lseq; i++) printf("%3i   %4i\n", i, locs[i]);
	fclose(ifp);

	if (argc < 4) {
		printf("\n\nDo you wish to input an existing likelihood file? (1/0): ");
		scanf("%i", &lkf);
		if (lkf) {
			printf("\n\nInput name of likelihood file: ");
			scanf("%s", &fname);
			ifp = fopen(fname, "r");
		}
	}
	else {lkf = 1; ifp = fopen(argv[3], "r");}
	if ((lkf) && (ifp==NULL)) nrerror("Cannot open likelihood file");
	
	if (argc > 4) {printf("\n\nSet to concise output\n\n"); verb=0;}

	pij = imatrix(1,data->lseq,1,data->lseq);
	for (i=1;i<=data->lseq;i++) for (j=1;j<=data->lseq;j++) pij[i][j]=0;
	pset = init_pset(pset, lkf, ifp, &npt, data->nseq);
	pset = pair_spectrum(seqs, data, nall, pset, &npt, &new, anc, pij);
        printf("\n\nCompleted classification of pair types \n\n");
	if (lkf) printf("\n\nOld = %i: New = %i\n\n", npt,new);
	if (verb) type_print(pij, data->lseq);

	print_pairs(stdout, pset, npt+new);

	if (lkf) theta=read_pars(ifp, &tcat, theta, &rcat, &rmax);
	else {
		theta = vector(1,tcat);
		for (i=1;i<=tcat;i++) theta[i]=0;
		if (tcat == 1) {
			tmp = (float) watterson(data->nseq);
/*			theta[1] = (float) data->lseq/(tmp*data->tlseq);*/
			theta[1] = (float) 1/tmp*log((float) (data->tlseq)/((data->tlseq)-(data->lseq)));
			printf("\n\nDo you wish to use the Watterson estimate for theta (%.5f) (1/0)?: ",theta[1]);
			scanf("%i", &i);
			if (!i) {printf("\n\nInput theta: "); theta[1]=0.0; while(theta[1]==0.0) scanf("%f", &theta[1]);}
		}
		else exit(1);
		printf("\n\nMax value of 4Ner to estimate: ");
		scanf("%f", &rmax);
		if (rmax>RHO_MAX) {printf("\n\n4Ner greater than max allowed: resetting to %.0f\n\n",RHO_MAX); rmax=(float) RHO_MAX;}
		printf("\n\nNumber of points to estimate for 4Ner (min=2): ");
		while (rcat < 2) scanf("%i", &rcat);
	}
	lkmat = matrix(1,npt+new,1,rcat);
	if (lkf) read_lk(ifp, lkmat, npt, tcat, rcat);
	if (new) lk_est(pset, npt, new, lkmat, tcat, theta, rcat, rmax);
	print_lks(pset, data->nseq, npt+new, lkmat, tcat, theta, rcat, rmax);

	lk_surf(pset, pij, data, lkmat, tcat, theta, rcat, rmax, locs);

	if (verb) {
		printf("\n\nWriting pairwise fits to file: fit\n\n");
		fit_pwlk(data,pij,locs,lkmat,tcat,rcat,rmax);
	}

	lkf=0;
	printf("\n\nDo you wish to test for recombination? (1/0): ");
	scanf("%i", &lkf);
	if (lkf) rec_test(data, pij, locs, lkmat, pset, npt+new, tcat, rcat, rmax);

	free_ivector(pij,1,data->lseq*(data->lseq-1)/2);
	free_imatrix(seqs,1,data->nseq,1,data->lseq);
	free_imatrix(nall,1,data->lseq,1,5);
	for (i=1;i<sizeofpset;i++) free(pset[i]);
	free(pset);
	free(data);

	printf("\n\nInput Q to end\n\n");
	while(getchar()!='Q');
}



/*Likelihood estimation for each pairwise comparison using the method of Fearnhead and Donnelly (2001) */

void lk_est(pset,npt,new,lkmat,tcat,stheta,rcat,rmax) 
int npt, new, tcat,rcat;
float **lkmat, *stheta, rmax;
struct site_type **pset;
{

	int i, j, k, p, nd, *data, K;
	double **P, *mu, theta[2],  *log_lk;

	printf("\n\nEstimating likelihood surface for data (%i pair types)\n", new);

	K = 2;
	mu = (double *) calloc(K,sizeof(double));
	for (i=0; i<K; i++) mu[i] = (double) 1/K;
	P = (double **) calloc(K, sizeof(double *));
	for (i=0; i<K; i++) P[i] = (double *) calloc(K, sizeof(double));
	for (i=0; i<K; i++) for (j=0; j<K; j++) {
		if (j!=i) P[i][j] = (double) 1/(K-1);
		else P[i][j] = 0.0;
	}
	log_lk = (double *) calloc(rcat, sizeof(double));

	for (i=npt+1; i<=npt+new; i++) {
		for (j=0, nd=0; j<4; j++) if (pset[i]->pt[j]) nd++;
		data = (int *) malloc((size_t) 3*nd*sizeof(int)); 
		for (j=0,k=0; j<4; j++) 
		   if (pset[i]->pt[j]) {
			data[3*k] = (int) j/2 + 1;
			data[3*k+1] = (int) j%2 + 1;
			data[3*k+2] = (int) pset[i]->pt[j];
			k++;
		   }
		printf("\nHaplotype data: (%i of %i)\n",i,npt+new); for (j=0; j<nd; j++) printf("%i%i:%i\n",data[3*j], data[3*j+1],data[3*j+2]);
		theta[0]=stheta[1];
		theta[1]=stheta[1];
		printf("theta : %.3f %.3f\n", theta[0], theta[1]);
		pairs(nd, data, K, P, mu, theta, (double) rmax, rcat, NRUN, log_lk);
		for (p=1; p<=rcat; p++) lkmat[i][p] = (float) log_lk[p-1];
		free(data);
	}

	free(mu);
	free(log_lk);
	for (i=0;i<K;i++) free(P[i]);
	free(P);
}	


void print_lks(pset,nseq,npt,lkmat,tcat,theta,rcat,rmax) 
int nseq,npt,tcat,rcat;
float **lkmat, *theta, rmax;
struct site_type **pset;
{

	int p, c1, c2, c3;
	FILE *ofp;

	ofp = fopen("new_lk", "w");

	fprintf(ofp, "\n%i %i\n%i ",nseq,npt,tcat);
	for (c1=1; c1<=tcat; c1++) fprintf(ofp, " %f ", theta[c1]);
	fprintf(ofp,"\n%i %f\n",rcat, rmax);
	fprintf(ofp, "\n\nType    00  01  10  11 Rho");
	for (c3=0; c3<rcat; c3++) fprintf(ofp, "%7.1f ",(float) c3*rmax/(rcat-1));
	fprintf(ofp,"\n\n");
	for (p=1; p<=npt; p++) {
		fprintf(ofp,"%4i # ", p);
		for (c1=0; c1<4; c1++) fprintf(ofp,"%3i ", pset[p]->pt[c1]);
		fprintf(ofp," :  ");
		for (c1=0; c1<tcat; c1++)
			for (c2=0; c2<tcat; c2++) 
			   for (c3=1; c3<=rcat; c3++) 
				fprintf(ofp,"%7.2f ", lkmat[p][rcat*tcat*c1+rcat*c2+c3]);
		fprintf(ofp,"\n");
	}
	fclose(ofp);
}



/*Estimation of the likelihood surface for rho*/

void lk_surf(pset,pij,data,lkmat,tcat,theta,rcat,rmax,locs) 
int **pij, tcat, rcat, *locs;
float **lkmat, *theta, rmax;
struct site_type **pset;
struct data_sum *data;
{

	int i, p, *pars, fl=0, t, j;
	float **clist;
	float lkmax;
	FILE *ofp;

	printf("\n\nDo you wish to change grid over which to estimate likelihoods for (default = %i points, 4Ner 0 - %.1f) (1/0) :",rcat,rmax);
	scanf("%i", &fl);
	if (fl) {
		data->rme=-10; data->rce=0;
		printf("\n\nMax 4Ner for estimation           : ");
		while (data->rme < 0.0) scanf("%f", &data->rme);  
        	printf("\n\nNumber of classes to estimate for: ");
        	while (data->rce < 1) scanf("%i", &data->rce);
	}
	else {
		data->rme=rmax; data->rce=rcat;
	}

	clist = matrix(1,data->rce, 1, 5);
	pars = ivector(1,data->lseq); for (i=1;i<=data->lseq;i++) pars[i]=1;

	for (j=1, data->lkmax=-100000000; j<=data->rce; j++) {
		lkmax = -100000000;
	   	if (data->rce > 1) clist[j][1] = (float) (data->rme)*(j-1)/((data->rce)-1);
		printf("\nLikelihood estimation with C = %6.2f: ", clist[j][1]);
	   	if ((fl=lk_calc(pars, pij, data, tcat, rcat, rmax, &lkmax, locs, clist[j][1], lkmat)) == 0) lkmax=0;
		clist[j][2]=lkmax;
		clist[j][3]=(float) fl;
		printf(" %.3f", lkmax);
		if ((lkmax < 0) && (lkmax > data->lkmax)) {
			data->lkmax = lkmax;
			data->rho=clist[j][1]; 
		}
	}
	printf("\n\nResults of Estimation\n\n C       Lkmax     Type\n\n");
	for (j=1; j<=data->rce; j++) {
		printf("%8.2f   ",clist[j][1]);
		if (clist[j][2] < 0.0) printf("%8.3f  %3.0f", clist[j][2], clist[j][3]);
		if (clist[j][1] > rmax) printf(" Beyond range of estimated likelihoods");
		printf("\n");
	}
	printf("\n\nMaximum at rho = %.3f : Lk = %.3f \n\n",data->rho, data->lkmax);

	ofp = fopen("outfile", "w");
	if (ofp == NULL) {printf("\n\nCannot open outfile\n\n"); exit(1);}
	fprintf(ofp,"Lk surface\n\nTheta = %.5f\n\n", theta[1]);
	fprintf(ofp,"\n\nRho   Pairwise Lk\n\n");
	for (j=1;j<=data->rce;j++) {
		fprintf(ofp,"%8.2f  ", clist[j][1]);
		if (clist[j][2] < 0.0) fprintf(ofp,"%8.3f", clist[j][2]);
		if (clist[j][1] > rmax) fprintf(ofp," Beyond range of likelihoods: Using Rho_max as estimate");
		fprintf(ofp,"\n");
	}
	fclose(ofp);

	free_ivector(pars,1,data->lseq);
        free_matrix(clist,1,data->rce,1,5);
}
		

/*Routine to calculate the pairwise likelihood for any given rho*/

int lk_calc(pars,pij,data,tcat,rcat,rmax,lkrun,locs,ct,lkmat) 
int *pars, **pij, tcat, rcat, *locs;
float rmax, *lkrun, ct, **lkmat;
struct data_sum *data;
{

	int i, j, k, t, aij[2], fl=1, dij;
	float cij, d, lke=-100;

	for (i=1, (*lkrun)=0.0; i<data->lseq; i++)
                for (j=i+1; j<=data->lseq; j++) {
                   t = pij[i][j];
		   if (t > 0) {
			if (data->lc == 'C') {
			  dij = locs[j]-locs[i];
			  /*If wish to use circular model, have to comment out previous line, and use next*/
			  /*dij = mini(locs[j]-locs[i], locs[i]+(data->tlseq)-locs[j]);*/
			  cij = (float) 2*ct*(1-exp((float) -dij/(data->avc)));
			}
			else cij = (float) ct*(locs[j]-locs[i])/(data->tlseq);
/*			aij[0]=(pars[i]-1)*(rcat)*tcat; aij[1]=(pars[j]-1)*(rcat);*/
			aij[0]=aij[1]=0;
			if (cij < 0) {printf(" C < 0!! "); return 0;}
			if (cij > rmax) {
				lke = (float) lkmat[t][aij[0]+aij[1]+rcat];
				fl=2;
			}
			else {
			   d = (float) cij*(rcat-1)/rmax;
			   k = (int) d+1;
			   if (k<rcat) lke = (float) lkmat[t][aij[0]+aij[1]+k]+(d-k+1)*(lkmat[t][aij[0]+aij[1]+k+1]-lkmat[t][aij[0]+aij[1]+k]);
			   else lke = lkmat[t][aij[0]+aij[1]+rcat];
			}
			if (lke < 0.0) { (*lkrun) += (float) lke;}
                        else {printf(" Lk >= 0!! "); return 0;}
		   }
                }
	return fl;
}

