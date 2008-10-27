void rec_test(data,pij,locs,lkmat,pset,npt,tcat,rcat,rmax) 
int **pij, *locs, npt, tcat, rcat;
float **lkmat, rmax;
struct data_sum *data;
struct site_type **pset;
{

	int i, j, **pijs, *ord, ngs[4], shuff, tmp, *pars, imax, l, u, aij[2], dij, t, k, *anal;
	float f[2], npairs, lmax, lkrun, cij, lke, d, rmp;
	double lds[3], dav[6];
	FILE *ofp;
	
	printf("\n\nTesting for recombination and analysing patterns of linkage disequilibrium\n\n");

	for (i=1; i<=npt; i++){
		f[0]=(float) ((pset[i]->pt[1])+(pset[i]->pt[3]))/(data->nseq);
		f[1]=(float) ((pset[i]->pt[2])+(pset[i]->pt[3]))/(data->nseq);
		pset[i]->ld_stat[0]=(float) (pset[i]->pt[3])/(data->nseq)-f[0]*f[1];
		pset[i]->ld_stat[1]=(float) pow((pset[i]->ld_stat[0]),2)/(f[0]*f[1]*(1-f[0])*(1-f[1]));
		if (pset[i]->ld_stat[0] < 0) pset[i]->ld_stat[2]=(pset[i]->ld_stat[0])/(-1*f[0]*f[1]);
		else pset[i]->ld_stat[2]=(pset[i]->ld_stat[0])/((float) f[0]<f[1] ? f[0]*(1-f[1]) : f[1]*(1-f[0]));
	}

	pijs = imatrix(1, data->lseq, 1, data->lseq);
	ord = ivector(1, data->lseq);
	pars = ivector(1, data->lseq);
	anal = ivector(1,data->lseq);

	for (i=1; i<=data->lseq; i++) ord[i]=i;
	for (i=1;i<data->lseq;i++) {
		for (j=i+1,t=0;j<=data->lseq;j++) if (pij[i][j]) t++;
		if (t) anal[i]=1; else anal[i]=0;
	}
	if (pij[(data->lseq)-1][data->lseq]) anal[data->lseq]=1; else anal[data->lseq]=0;

	for (i=0;i<6;i++) dav[i]=0.0;	
	for (i=1, npairs = 0;i<data->lseq;i++) for (j=i+1; j<=data->lseq;j++) 
		if (pij[i][j] != 0) {
			npairs++;
			if (data->lc=='L') {
				dav[0] += (double) locs[j]-locs[i];
				dav[3] += (double) (locs[j]-locs[i])*(locs[j]-locs[i]);
			}
			else {
				dav[0] += (double) minc(locs[i], locs[j], data->tlseq);
				dav[3] += (double) pow((float) minc(locs[i], locs[j], data->tlseq), 2);
			}
			dav[1] += (double) pset[pij[i][j]]->ld_stat[1];
			dav[2] += (double) pset[pij[i][j]]->ld_stat[2];
			dav[4] += (double) pow((pset[pij[i][j]]->ld_stat[1]), 2);
			dav[5] += (double) pow((pset[pij[i][j]]->ld_stat[2]), 2);
		}
	for(i=0; i<6; i++) dav[i] /= (float) npairs;
	for(i=3;i<6;i++) {dav[i]-=pow(dav[i-3],2); dav[i]=sqrt(dav[i]);}
	ld_calc(pset, pij, locs, data->ld, data);

	printf("\n\nObserved LD statistics\n\n");
	printf("	Npairs       = %8.0f\n", npairs);
	printf("        Lkmax        = %8.2f\n", data->lkmax);
	printf("	G4           = %8.0f\n", data->ld[0]);
	printf("	corr(r2,D)   = %8.5f\n", ((data->ld[1])/npairs-dav[0]*dav[1])/(dav[3]*dav[4]));
	if (dav[5]>0.0001) 
	printf("	corr(D',d)   = %8.5f\n", ((data->ld[2])/npairs-dav[0]*dav[2])/(dav[3]*dav[5]));
	else
	printf("	corr(D',d)   = na\n");	

	ofp = fopen("rdist", "w");
	if (!ofp) {printf("\nCannot open file for output\n\n"); exit(1);}
	fprintf(ofp,"Distribution of estimated Rho values\n\nShuffle   Rho    Lkmax      G4     corr(r2,d)   corr(D',d)\n\n");

	for (i=0;i<4;i++) ngs[i]=0;
	for (shuff=1; shuff<=NSHUFF;shuff++) {
			if ((shuff%100)==0) printf("\nShuffle %i", shuff);
			for (i=1; i<=data->lseq;i++) if (anal[i]) {
				k=0;
				while (k==0) {j=(int) ((float) ran2()*(data->lseq))+1; if (anal[j]) k=1;}
				tmp=ord[i]; ord[i]=ord[j]; ord[j]=tmp;
			}
			for (i=1; i<data->lseq; i++) 
				for (j=i+1;j<=data->lseq;j++) {
					l = mini(ord[i], ord[j]);
					u = maxi(ord[i], ord[j]);
					pijs[i][j] = pij[l][u];
				}

			for (i=1; i<=data->lseq;i++) pars[i]=1;
			for (i=1, lmax=-100000000;i<=data->rce;i++) {
				if(lk_calc(pars, pijs, data, tcat, rcat, rmax, &lkrun, locs, (float) (i-1)*(data->rme)/((data->rce)-1), lkmat))
					if (lkrun > lmax) {imax = i; lmax=lkrun;}
			}
			ld_calc(pset, pijs, locs, lds, data);
			fprintf(ofp,"%4i  %8.3f  %8.3f  %.0f  %8.5f  %8.5f\n",shuff, (float) (imax-1)*(data->rme)/((data->rce)-1), lmax, \
				lds[0], (lds[1]/npairs-dav[0]*dav[1])/(dav[3]*dav[4]), \
				dav[5]>0.0001 ? (lds[2]/npairs-dav[0]*dav[2])/(dav[3]*dav[5]) : 0.00);
			if (lmax >= data->lkmax) ngs[0]++;
			for (i=1; i<3; i++) if (lds[i]<=(data->ld[i])) ngs[i+1]++;
			if (lds[0]>=(data->ld[0])) ngs[1]++;
		}

	fclose(ofp);
	printf("\n\nResults of shuffling\n\n");
	printf("Proportion Lkmax >= estimated      = %.4f\n", (float) ngs[0]/NSHUFF);
	printf("Proportion G4 >= G4 estimated      = %.4f\n",(float) ngs[1]/NSHUFF);
	printf("Proportion corr(r2,d) <= estimated = %.4f\n", (float) ngs[2]/NSHUFF);
	printf("Proportion corr(D',d) <= estimated = %.4f\n", (float) ngs[3]/NSHUFF);

	free_imatrix(pijs,1,data->lseq, 1, data->lseq);
	free_ivector(ord, 1, data->lseq);
	free_ivector(pars, 1, data->lseq);
	free_ivector(anal,1,data->lseq);
}



void ld_calc(pset,pijs,locs,ldv, data) 
int **pijs,*locs;
double ldv[3];
struct site_type **pset;
struct data_sum *data;
{

	int i, j, pt, dij;
	for (i=0; i<3; i++) ldv[i]=0.0;
	for (i=1; i<data->lseq; i++)
		for (j=i+1; j<=data->lseq;j++) {
			pt = pijs[i][j];
			if (pt) {
				if (data->lc=='L') dij = locs[j]-locs[i];
				else dij = minc(locs[i], locs[j], data->tlseq);
			 	if (pset[pt]->ld_stat[2] < 0.9999) ldv[0]+=(double) dij;
				ldv[1] += (double) pset[pt]->ld_stat[1]*dij;
				ldv[2] += (double) pset[pt]->ld_stat[2]*dij;
			}
		}
}


void fit_pwlk(data,pij,locs,lkmat,tcat,rcat,rmax) 
int **pij,*locs,tcat,rcat;
float **lkmat, rmax;
struct data_sum *data;
{

	int i, j, dij, t, k;
	float lkmax, cij, lke, d, rmp, clk=0.0;
	FILE *ofp;
	
	ofp = fopen("fit","w");
	fprintf(ofp,"\nFit between data and ML model for each pair (+ve: Rho_max_pair > Rho_est, -ve Rho_max_pair < Rho_est)\n\n      ");
	for (i=1; i<data->lseq; i++) fprintf(ofp, " %6i", i+1);
	for (i=1; i<data->lseq; i++) {
		fprintf(ofp,"\n%5i:", i);
		for (j=1; j<i; j++) fprintf(ofp,"       ");
                for (j=i+1; j<=data->lseq; j++) {
                   t = pij[i][j];
                   if (t > 0) {
                        if (data->lc == 'C') {
				dij = locs[j]-locs[i];
/*	Comment out previous line and use following for circular model*/
/*                                dij = mini(locs[j]-locs[i], locs[i]+(data->tlseq)-locs[j]);*/
                                cij = (float) 2*(data->rho)*(1-exp((float) -dij/(data->avc)));
                        }
                        else cij = (float) (data->rho)*(locs[j]-locs[i])/(data->tlseq);
/*			printf("\nSites %3i and %3i are of type %5i : dist = %8.3f ", i, j, t, cij);*/
                        if (cij > rmax) lke = (float) lkmat[t][rcat];
                        else {
                           d = (float) cij*(rcat-1)/rmax;
                           k = (int) d+1;
                           if (k<rcat) lke = (float) lkmat[t][k]+(d-k+1)*(lkmat[t][k+1]-lkmat[t][k]);
                           else lke = lkmat[t][rcat];
                        } /*printf(": extrapolated lk = %.3f", lke);*/
			for (k=1, lkmax=-100000000; k<=rcat;k++)
				if (lkmat[t][k]>lkmax) {lkmax = lkmat[t][k]; rmp=(float) (k-1)*rmax/(rcat-1);}
/*			printf(" Maxlk = %.3f", lkmax);*/
/*			fprintf(ofp,"\n%4i %4i",i,j);*/
			if (rmp > cij) fprintf(ofp," %6.2f",(float) lkmax - lke);
			else fprintf(ofp," %6.2f", (float) lke-lkmax);			
			clk += lkmax-lke;
                   }
		   else fprintf(ofp, "     NA");
                }
	}

	fprintf(ofp, "\n\nTotal deviation = %.3f\n\n", clk);
	fclose(ofp);
}
