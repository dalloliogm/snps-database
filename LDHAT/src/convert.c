#include "./header.h"

#define DEBUG 1

main (int argc, char *argv[]) {

	int i, j, **seqs, **nall, *sloc;
	int nseq, nmax, lseq, fl, na, psite, fgap=0, ilseq;
	float fcut=0.0, pwd, sn, ns, ctaj[12], n;
	char fname[MAXNAME], bases[6]="0-TCAG", c, **seqnames;
	FILE *ifp, *ofp, *loc, *inloc;

	if (argc > 1) ifp = fopen(argv[1], "r"); 	// get -seq argument
	else {
		printf("\n\nInput filename for seqs\n\n");
		scanf("%s", &fname);
		ifp = fopen(fname, "r");
	}
	if (ifp == NULL) nrerror("Error in opening sequence file");

	if (argc > 2) {								// get -loc argument
		printf("\nUsing input location file: %s\n\n", argv[2]);
		inloc = fopen(argv[2], "r");
		if (!inloc) {printf("\n\nCannot open input locs\n\n"); exit(1);}
	}

     	fscanf(ifp,"%i %i", &nseq, &lseq);

	if (argc > 2) {
		fscanf(inloc,"%i %i %c", &i, &ilseq, &c);
		if (i != lseq) {printf("\n\nError: loc file does not match sequence file\n\n"); exit(1);}
		sloc = (int *) malloc ((size_t) (lseq+1)*sizeof(int));
		for (i=1;i<=lseq;i++) {
			fscanf(inloc,"%i", &sloc[i]);
			printf("\nSite %4i : position %10i", i, sloc[i]);
		}
		fclose(inloc);
	}

	if (nseq > SEQ_MAX) {printf("\n\nMore than max no. sequences: Using first %i for analysis\n\n", SEQ_MAX); nseq=SEQ_MAX;}
	printf("\n\nReading %i sequences of length %i bases .........\n", nseq, lseq);

	seqs = (int **) imatrix(1, nseq, 1, lseq);
	seqnames = (char **) cmatrix(1, nseq, 1, MAXNAME);

	if (read_fasta(seqs, ifp, nseq, lseq, seqnames)) printf("\nSequences read succesfully\n\n");
	fclose(ifp);

	nall = imatrix(1, lseq, 1, 6);
	allele_count(seqs, nseq, lseq, nall);

	printf("\n\nSegregating sites written to file	: sites\n");
	printf("Locations of segregating sites to file	: locs\n\n");
	ofp = fopen("sites", "w");
	loc = fopen("locs", "w");
	printf("\n\nAll segregating sites or those with 2 alleles? (1/2):"); scanf("%i", &fl);
	if (fl==2) {
	  printf("\n\nFrequency cutoff? (0 for none):");
	  scanf("%f", &fcut);
	}
	printf("\n\nInclude sites with gaps or unknown bases? (1/0) :");
	scanf("%i", &fgap);

	for (i=1, psite=0;i<=lseq;i++) {
		if ((!fgap) && (nall[i][1])) nall[i][6]=0;
		else {
			for (j=2,na=0,nmax=0;j<=5;j++) {if (nall[i][j]) na++; if (nall[i][j]>nmax) nmax=nall[i][j];}
			if ((fl==1)&&(na>1)) nall[i][6]=1;
			else if ((fl==2)&&(na==2)) if (nseq-nmax > (int) nseq*fcut) nall[i][6]=1;
			else nall[i][6]=0;
		}
		if (nall[i][6]) psite++;
	}

	if (psite==0) {printf("\n\nNo data to output\n\n"); exit(1);}
	fprintf(ofp,"%i %i",nseq,psite);
	fprintf(loc,"%i %i %c", psite, (argc > 2 ? ilseq : lseq), (argc > 2 ? c : 'L'));
	for (i=1;i<=nseq;i++) {
		fprintf(ofp,"\n>%s\n",seqnames[i]);
		for (j=1,na=0;j<=lseq;j++) if (nall[j][6]) {
			fprintf(ofp,"%c",bases[seqs[i][j]]);
			na++;
			if ((na%50)==0) fprintf(ofp,"\n");
		}
	}
	fclose(ofp);
	for (i=1;i<=lseq;i++) if (nall[i][6]) fprintf(loc,"\n%i", (argc > 2 ? sloc[i] : i));
	fclose(loc);

	for (i=1, sn=0, pwd=0, ns=0; i<=lseq; i++) if (nall[i][6]) {
	  sn++;
	  for (j=2; j<=5; j++) if (nall[i][j]==1) ns++;
	  for (j=2;j<=5;j++) pwd += (float) nall[i][j]*nall[i][j];
	}
	pwd = (float) sn-pwd/((float) nseq*nseq);
	pwd *= (float) nseq/(nseq-1);

	for (i=1, ctaj[0]=ctaj[1]=0.0; i<nseq; i++) {ctaj[0]+=(float) 1/i; ctaj[1]+= (float) 1/(i*i);}	// calculating Tajima's D?
	n = (float) nseq;
	ctaj[2]=(float) (nseq+1)/(3*nseq-3);
	ctaj[3]=(float) 2*(nseq*nseq+nseq+3)/(9*nseq*(nseq-1));
	ctaj[4]=ctaj[2]-1/ctaj[0];
	ctaj[5]=(float) ctaj[3]-(nseq+2)/(nseq*ctaj[0])+ctaj[1]/(ctaj[0]*ctaj[0]);
	ctaj[6]=ctaj[4]/ctaj[0];
	ctaj[7]=ctaj[5]/(ctaj[0]*ctaj[0]+ctaj[1]);
	ctaj[8]=2*(nseq*ctaj[0]-2*(nseq-1))/((nseq-1)*(nseq-2));
        ctaj[9]=ctaj[8]+(n-2)/((n-1)*(n-1))+((2/(n-1))*(1.5-(2*(ctaj[0]+1/n)-3.0)/(n-2)-1/n));
	ctaj[10]=(nseq*nseq*ctaj[1]/((nseq-1)*(nseq-1))+ctaj[0]*ctaj[0]*ctaj[9]-2*nseq*ctaj[0]*(ctaj[0]+1)/((nseq-1)*(nseq-1)))/(ctaj[0]*ctaj[0]+ctaj[1]);
	ctaj[11]=nseq/(n-1)*(ctaj[0]-n/(n-1))-ctaj[10];

	if (DEBUG) {
	  printf("\n\nCoefficients for tests\n\n");
	  for (i=0;i<12;i++) printf("%8.4f\n", ctaj[i]);
	}

	printf("\n\nSummary of output data\n");
	printf("\nSegregating sites      = %8.0f", sn);
	printf("\nAverage PWD            = %8.3f", pwd);
	printf("\nWatterson theta        = %8.3f", (float) sn/ctaj[0]);
	printf("\nTajima D statistic     = %8.3f", (float) (pwd-sn/ctaj[0])/sqrt(ctaj[6]*sn+ctaj[7]*sn*(sn-1)));
	printf("\nFu and Li D* statistic = %8.3f", (float) (nseq/(nseq-1)*sn-ctaj[0]*ns)/sqrt(ctaj[11]*sn+ctaj[10]*sn*sn));
	printf("\n\n");

	/*
	if (argc < 3) free_imatrix(seqs, 1, nseq, 1, lseq);
	free_imatrix(nall,1,lseq,1,6);
	free(sloc);
	*/

	printf("\n\nInput Q to end\n\n");
	while (getchar()!='Q');
}

