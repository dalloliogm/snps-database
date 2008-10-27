#include "./header.h"
#include "./random.cc"

long *idum;

main (int argc, char *argv[]) {

	int i, j, **seqs, **nall, ord=1, *locs, ns, **pij, lkf=0, npt=0, new=0, anc=0;
	int tcat=1, rcat=0;
	char fname[MAXNAME], c, **seqnames;
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
		ifp=fopen(fname, "r");
	}
	if (ifp == NULL) nrerror("Cannot open loc file");
	fscanf(ifp, "%i %i %c", &ns, &data->tlseq, &data->lc);
	if (ns != data->lseq) nrerror("Lseq and Locs disagree");
	if ((data->lc != 'C')&&(data->lc != 'L')) nrerror("Must input linear/circular");
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

	pij = imatrix(1,data->lseq,1,data->lseq);
	for (i=1;i<=data->lseq;i++) for (j=1;j<=data->lseq;j++) pij[i][j]=0;
	pset = init_pset(pset, lkf, ifp, &npt, data->nseq);
	pset = pair_spectrum(seqs, data, nall, pset, &npt, &new, anc, pij);
        printf("\n\nCompleted classification of pair types \n\n");
	if (lkf&&new)  {printf("\n\nLikelihoods missing for pairs: use pairwise to generate\n\n"); exit(1);}
	if (lkf) {
		theta=read_pars(ifp, &tcat, theta, &rcat, &rmax);
		lkmat = matrix(1,npt+new,1,rcat);
		read_lk(ifp, lkmat, npt, tcat, rcat);
	}

	ld_test(data, pij, locs, lkmat, pset, npt+new, rcat, rmax, lkf);

	free_ivector(pij,1,data->lseq*(data->lseq-1)/2);
	free_imatrix(seqs,1,data->nseq,1,data->lseq);
	free_imatrix(nall,1,data->lseq,1,5);

	if (lkf) free_matrix(lkmat,1,npt+new,1,rcat);
	for (i=1;i<sizeofpset;i++) free(pset[i]);
	free(pset);
	free(data);

/*	printf("\n\nInput Q to end\n\n");
	while(getchar()!='Q');
*/
}



void ld_test(data,pij,locs,lkmat,pset,npt,rcat,rmax,lkf) 
int **pij, *locs, npt, rcat, lkf;
float **lkmat, rmax;
struct data_sum *data;
struct site_type **pset;
{

	int i, j, k, l, **pijs, *ord, ngs[3], shuff, tmp, u, aij[2], dij, t, opt=0, fl=0, *anal;
	int na, **inf, **infs, nsf;
	float f[2], npairs, d, rmp, fcut, fmax;
	double dav[6], lds[3];
	FILE *ofp;
	
	printf("\n\nAnalysing the relationship between linkage disequilibrium and physical distance");
	printf("\n\nCurrent implementation only analyses biallelic markers");
	if (lkf) printf("\n\nUsing LkR[0.0]/LkR[%.1f] as a condition for whether pairs are informative about recombination\n\n",rmax);

	for (i=1; i<=npt; i++){
		f[0]=(float) ((pset[i]->pt[1])+(pset[i]->pt[3]))/(data->nseq);
		f[1]=(float) ((pset[i]->pt[2])+(pset[i]->pt[3]))/(data->nseq);
		if ((!f[0])||(!f[1])) {printf("\n\nError: zero frequency for pt %i (%f %f)\n\n",i,f[0],f[1]); exit(1);}
		pset[i]->ld_stat[0]=(float) (pset[i]->pt[3])/(data->nseq)-f[0]*f[1];
		if (pset[i]->ld_stat[0]!=0.0) pset[i]->ld_stat[1]=(float) pow((pset[i]->ld_stat[0]),2)/(f[0]*f[1]*(1-f[0])*(1-f[1]));
		else {pset[i]->ld_stat[1]=0.0;}
		if (pset[i]->ld_stat[0] < 0) pset[i]->ld_stat[2]=(pset[i]->ld_stat[0])/(-1*f[0]*f[1]);
		else if (pset[i]->ld_stat[0]>0) pset[i]->ld_stat[2]=(pset[i]->ld_stat[0])/((float) f[0]<f[1] ? f[0]*(1-f[1]) : f[1]*(1-f[0]));
		else {pset[i]->ld_stat[2]=0.0;}
		if (lkf) pset[i]->ld_stat[3] = lkmat[i][1]-lkmat[i][rcat];
	}

	printf("\n\nAnalysis options:  \n\n");
	printf("	All sites 				(1)\n");
	printf("	Informative about recombination 	(2)\n");
	printf("	Frequency cut-off			(3)\n\n");

	scanf("%i", &opt);
	switch(opt) {
		case 1:
			break;
		case 2:
			fcut=1.0;
			if (!lkf) {printf("\n\nNo likelihood file specified\n\n"); exit(1);}
			printf("\n\nChange Lk ratio criterion from default of 1.0? (1/0):");
			scanf("%i",&fl);
			if (fl) {printf("\n\nInput ratio cut-off :");scanf("%f", &fcut);}
			break;
		case 3:
			printf("\n\nInput frequency cut-off :");
			scanf("%f", &fcut);
			break;
		default:
			printf("\n\nInvalid option\n\n");
			exit(1);
	}
	
	anal = ivector(1,data->lseq);
	inf = imatrix(1,data->lseq, 1, data->lseq);
	for (i=1;i<data->lseq;i++) {
		for (j=i+1;j<=data->lseq;j++) {
			inf[i][j]=1;
			if (pij[i][j]==0) inf[i][j]=0;
			else if ((opt==2)&&(fabs(pset[pij[i][j]]->ld_stat[3])<fcut)) inf[i][j]=0;
			else if (opt==3) {
				if (((pset[pij[i][j]]->pt[1])+(pset[pij[i][j]]->pt[3]))<(fcut*(data->nseq))) inf[i][j]=0;
				else if (((pset[pij[i][j]]->pt[2])+(pset[pij[i][j]]->pt[3]))<(fcut*(data->nseq))) inf[i][j]=0;
			}
		}
		for (j=i+1,na=0; j<=data->lseq;j++) if (inf[i][j]) na++;
		if (na) anal[i]=1;
		else anal[i]=0;
	}
	if (inf[data->lseq-1][data->lseq]) anal[data->lseq]=1; 
	else anal[data->lseq]=0;

	for (i=0;i<6;i++) dav[i]=0.0;
	for (i=1,npairs = 0; i<data->lseq;i++) if (anal[i]) for (j=i+1; j<=data->lseq;j++) 
                if (inf[i][j]) {
                        npairs++;
                        t=pij[i][j];
			if (data->lc=='L') {
                        	dav[0] += (double) locs[j]-locs[i];
                        	dav[3] += (double) (locs[j]-locs[i])*(locs[j]-locs[i]);
			}
			else {
				dav[0] += (double) minc(locs[i], locs[j], data->tlseq);
				dav[3] += (double) pow((float) minc(locs[i], locs[j], data->tlseq),2);
			}
                        dav[1] += (double) (pset[t]->ld_stat[1]);
                        dav[2] += (double) (pset[t]->ld_stat[2]);
                        dav[4] += (double) pow((pset[t]->ld_stat[1]),2);
                        dav[5] += (double) pow((pset[t]->ld_stat[2]),2);
                }
	if (npairs < 1) {printf("\n\nNo data\n\n"); exit(1);}
        for(i=0; i<6; i++) dav[i] /= npairs;
        for(i=3;i<6;i++) {dav[i]-=pow(dav[i-3],2); dav[i]=sqrt(dav[i]); }
        ld_calc2(pset, pij, data->lseq, locs, data->ld, inf, data);

        printf("\nObserved LD statistics\n\n\
                        Npairs 		= %8.0f\n\
                        G4 		= %8.0f\n\
                        corr(r2,D)  	= %8.5f\n\
                        corr(D',d)  	= %8.5f\n", \
                npairs, data->ld[0], ((data->ld[1])/npairs-dav[0]*dav[1])/(dav[3]*dav[4]), \
                dav[5]>0.00001 ? ((data->ld[2])/npairs-dav[0]*dav[2])/(dav[3]*dav[5]) : 0.00);

	printf("\n\nDo you wish to print data to file: ldplot ?  (1/0):");
	scanf("%i", &fl);
	if (fl) {
		ofp = fopen("ldplot", "w"); 
		fprintf(ofp,"\nSites used in the analysis: ");
		for (i=1;i<=data->lseq;i++) if(anal[i]) fprintf(ofp," %i", locs[i]);
		fprintf(ofp,"\n\nDistance  r-squared |D|' ");
		if (lkf) fprintf(ofp,"  L[0.0]-L[%.1f]",rmax);
		fprintf(ofp,"\n\n");
		for (i=1;i<data->lseq;i++)
		   for(j=i+1;j<=data->lseq;j++) {
			if (inf[i][j]) {
				t=pij[i][j];
				if (data->lc == 'L') fprintf(ofp,"%6i ",locs[j]-locs[i]);
				else fprintf(ofp,"%6i ", minc(locs[i], locs[j], data->tlseq));
				fprintf(ofp," %.5f %.5f ", pset[t]->ld_stat[1], pset[t]->ld_stat[2]);
				if (lkf) fprintf(ofp," %8.2f ", pset[t]->ld_stat[3]);
				fprintf(ofp,"\n");
			}
		   }
		fclose(ofp);
	}

	printf("\n\nDo you want to permute sites to test for correlation between LD and distance? (1/0):");
	scanf("%i", &fl);
	if (fl) {
		printf("\n\nNumber of permutations? :");
		scanf("%i", &nsf);
		pijs = imatrix(1, data->lseq, 1, data->lseq);
		infs = imatrix(1, data->lseq, 1, data->lseq);
		ord = ivector(1, data->lseq);

		for (i=1; i<=data->lseq; i++) ord[i]=i;
		ofp = fopen("rdist", "w");
		if (!ofp) {printf("\nCannot open file for output\n\n"); exit(1);}
		fprintf(ofp,"Distribution of permuted values\n\nShuffle   G4   corr(r2,d)   corr(D',d)\n\n");

		for (i=0;i<3;i++) ngs[i]=0;
		for (shuff=1; shuff<=nsf;shuff++) {
			if ((shuff%100)==0) printf("\nShuffle %i", shuff);
			for (i=1; i<=data->lseq;i++) if (anal[i]) {
				k=0; 
				while(k==0) {
					j=(int) ((float) ran2()*(data->lseq))+1; 
					if (anal[j]) k=1;
				}
				tmp=ord[i]; ord[i]=ord[j]; ord[j]=tmp;
			}
			for (i=1; i<data->lseq; i++) 
				for (j=i+1;j<=data->lseq;j++) {
					l = mini(ord[i], ord[j]);
					u = maxi(ord[i], ord[j]);
					pijs[i][j] = pij[l][u];
					infs[i][j] = inf[l][u];
				}
			ld_calc2(pset, pijs, data->lseq, locs, lds, infs, data);
			fprintf(ofp,"%5i  %10.0f  %8.5f  %8.5f\n",shuff,\
				lds[0], (lds[1]/npairs-dav[0]*dav[1])/(dav[3]*dav[4]), \
				dav[5] > 0.00001 ? (lds[2]/npairs-dav[0]*dav[2])/(dav[3]*dav[5]) : 0.00);
			if (lds[0] >= (data->ld[0])) ngs[0]++;
			for (i=1; i<3; i++) if (lds[i]<=(data->ld[i])) ngs[i]++;
		}

		fclose(ofp);
		printf("\n\nResults of shuffling\n\n");
		printf("Proportion G4 >= observed         = %.4f\n", (float) ngs[0]/nsf);
		printf("Proportion corr(r2,d) <= observed = %.4f\n", (float) ngs[1]/nsf);
		printf("Proportion corr(D',d) <= observed = %.4f\n", (float) ngs[2]/nsf);

		free_imatrix(pijs,1,data->lseq, 1, data->lseq);
		free_imatrix(infs,1,data->lseq, 1, data->lseq);
		free_ivector(ord, 1, data->lseq);
	}

	free_imatrix(inf,1,data->lseq,1,data->lseq); 
	free_ivector(anal,1,data->lseq);
}



void ld_calc2(pset,pijs,lseq,locs,ldv,inf,data) 
int **pijs,lseq,*locs,**inf;
double ldv[3];
struct site_type **pset;
struct data_sum *data;
{

	int i, j, pt, ct=0;
	double d;

	for (i=0; i<3; i++) ldv[i]=0.0;
	for (i=1; i<lseq; i++)
		for (j=i+1; j<=lseq;j++) {
			pt = pijs[i][j];
			if (inf[i][j]) {
				ct++;
				if (data->lc == 'L') d = (double) locs[j]-locs[i];
				else d = (double) minc(locs[i], locs[j], data->tlseq);
			 	if (pset[pt]->ld_stat[2] < 0.9999) ldv[0] += (double) d;
				ldv[1] += (double) (pset[pt]->ld_stat[1])*d;
				ldv[2] += (double) (pset[pt]->ld_stat[2])*d;
			}
		}
}

