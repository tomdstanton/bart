# bart
**ba**cterial **r**ead **t**yper

<centre>![Image](https://github.com/tomdstanton/bart/blob/master/bart_logo.png)

_By Tom Stanton_ \
[![alt text][1.1]][1] [![alt text][6.1]][6] \
Issues/queries/advice?
[email me!](mailto:s1895738@ed.ac.uk?subject=[bart])

[1]: http://twitter.com/tomstantonmicro
[1.1]: http://i.imgur.com/tXSoThF.png (twitter icon with padding)
[6]: http://www.github.com/tomdstanton
[6.1]: http://i.imgur.com/0o48UoR.png (github icon with padding)

### Introduction
bart is a bacterial MLST tool for NGS reads,
designed to be fast and very easy to use.
It uses heuristics to choose the best scheme for
your reads and prints results in a standard tab-separated format.

**If you found bart helpful, please cite:**
```
bart - BActerial Read Typer
Thomas David Stanton, 2021
https://github.com/tomdstanton/bart
```
### Dependencies
* python >=3.7
* [kma](https://anaconda.org/bioconda/kma) (use conda)
* [refseq_masher](https://anaconda.org/bioconda/refseq_masher) (use conda)

## Installation

```sh
git clone --recursive https://github.com/tomdstanton/bart && cd bart && python setup.py install
```
### Usage
```sh
usage: bart input.fq.gz [options] > outfile.tab

--options [defaults]:
  -r {pe,se,ont,int}  read-type (paired/single/nanopore/interleaved)
  -s [scheme]         force scheme, see bart-update -s
  -p [95]             template percent identity cutoff
  -o [input path]     export alleles to fasta
  -k, --keep          keep temporary files
  -a, --alt           consider alternative hits when assigning ST
  -amr [90]           screen for AMR genes, add percid
  -l [cwd]            create logfile
  -t [4]              number of threads
  -v, --verbose       print allele and alt-hits if different from profile
  -vv, --verboser     verbose with percid, coverage and depth
  -q, --quiet         silence messages
  -h, --help          show this help message and exit
```
I like to test bart on SRA reads like so:
```sh
fastq-dump SRR14224855 --split-files --gzip && bart SRR14224855*
```
* MLST of these reads completed in 9.6 seconds on a 4-core laptop.

If you already know the species of your reads,
or the specific scheme you would like to use, you can bypass
scheme choosing heuristics. 

For example if you have Staphylococcus reads,
see if the scheme is included:
```sh
$ bart-update -s | grep Staphylococcus
Staphylococcus_aureus
Staphylococcus_chromogenes
Staphylococcus_epidermidis
Staphylococcus_haemolyticus
Staphylococcus_hominis
Staphylococcus_lugdunensis
Staphylococcus_pseudintermedius
```
Now you can run:
```sh
bart SRR14224855* -s Staphylococcus_aureus
```
Output is now a single tab-separated line.
Alleles are presented like so:
* gene(allele), where the allele is from the matching, or nearest matching profile.
* '?'  indicates a non-perfect hit
* '~' indicates a potential novel hit
* '-' indicates no hit.

| SRR14224855 | Staphylococcus_aureus | 9 | arcC(3)                             | aroE(3)                             | glpF(1)                      | gmk(1)                        | pta(1)                         | tpi(1)                         | yqiL(10)                         | clonal_complex(CC1) |
|-------------|-----------------------|---|-------------------------------------|-------------------------------------|------------------------------|-------------------------------|--------------------------------|--------------------------------|----------------------------------|---------------------|

Verbose `-v` prints the top hit allele in square brackets next to the allele number
if different from the profile allele.
Alternative allele hits that were found will also be printed.
This means you can make an informed decision about the ST if there are several near-profile assignments.

| SRR14224855 | Staphylococcus_aureus | 9 | arcC(3)346,616                      | aroE(3)260,415                      | glpF(1)                      | gmk(1)85                      | pta(1)777                      | tpi(1)269                      | yqiL(10)816                      | clonal_complex(CC1) |
|-------------|-----------------------|---|-------------------------------------|-------------------------------------|------------------------------|-------------------------------|--------------------------------|--------------------------------|----------------------------------|---------------------|

"Verboser" `-vv` does the same, but prints mapping data 
of the top hit in the following format:
`gene(allele: %identity, %coverage, depth) alternative alleles`

or if the top allele hit isn't the same as the assigned profiles:
`gene(allele)[top hit allele: %identity, %coverage, depth] alternative alleles`

| SRR14224855 | Staphylococcus_aureus | 9 | arcC(3: 100.00 100.00 40.52)346,616 | aroE(3: 100.00 100.00 27.58)260,415 | glpF(1: 100.00 100.00 27.84) | gmk(1: 100.00 100.00 24.42)85 | pta(1: 100.00 100.00 36.66)777 | tpi(1: 100.00 100.00 52.26)269 | yqiL(10: 100.00 100.00 44.92)816 | clonal_complex(CC1) |
|-------------|-----------------------|---|-------------------------------------|-------------------------------------|------------------------------|-------------------------------|--------------------------------|--------------------------------|----------------------------------|---------------------|

The `-amr` option screens your reads for genes from
the NCBI AMRFinderPlus database.
This is performed _instead_ of MLST.

The results are printed in a tab-separated format and can be piped to a file:

```sh
bart SRR14224855* -amr > SRR14224855_amr.tab
```

| sample      | gene       | description                                                                                                | length | identity | coverage | depth  | 
|-------------|------------|------------------------------------------------------------------------------------------------------------|--------|----------|----------|--------| 
| SRR14224855 | sel27      | staphylococcal enterotoxin type 27                                                                         | 753    | 98.41    | 100.00   | 39.25  | 
| SRR14224855 | sel28      | staphylococcal enterotoxin type 28                                                                         | 726    | 98.90    | 100.00   | 20.16  | 
| SRR14224855 | hlgA       | bi-component gamma-hemolysin HlgAB subunit A                                                               | 930    | 99.68    | 100.00   | 48.64  | 
| SRR14224855 | icaC       | polysaccharide intercellular adhesin biosynthesis/export protein IcaC                                      | 1053   | 99.15    | 100.00   | 46.09  | 
| SRR14224855 | mepA       | multidrug efflux MATE transporter MepA                                                                     | 1356   | 99.78    | 100.00   | 56.13  | 
| SRR14224855 | arsR_pI258 | As(III)-sensing metalloregulatory transcriptional repressor ArsR                                           | 315    | 99.68    | 100.00   | 40.15  | 
| SRR14224855 | arsB_pI258 | arsenite efflux transporter membrane subunit ArsB                                                          | 1290   | 99.84    | 100.00   | 53.85  | 
| SRR14224855 | arsC_thio  | thioredoxin-dependent arsenate reductase                                                                   | 396    | 98.74    | 100.00   | 58.92  | 
| SRR14224855 | mco        | multi-copper oxidase Mco                                                                                   | 1389   | 99.71    | 100.00   | 36.77  | 
| SRR14224855 | selX       | staphylococcal enterotoxin-like toxin X                                                                    | 612    | 96.41    | 100.00   | 37.06  | 
| SRR14224855 | aur        | zinc metalloproteinase aureolysin                                                                          | 1530   | 99.15    | 100.00   | 82.74  | 
| SRR14224855 | mecA       | PBP2a family beta-lactam-resistant peptidoglycan transpeptidase MecA                                       | 2007   | 99.95    | 100.00   | 47.73  | 
| SRR14224855 | blaZ       | penicillin-hydrolyzing class A beta-lactamase BlaZ                                                         | 846    | 97.99    | 100.00   | 17.73  | 
| SRR14224855 | blaZ       | penicillin-hydrolyzing class A beta-lactamase BlaZ                                                         | 846    | 96.81    | 100.00   | 20.74  | 
| SRR14224855 | blaPC1     | BlaZ family penicillin-hydrolyzing class A beta-lactamase PC1                                              | 846    | 99.41    | 100.00   | 33.72  | 
| SRR14224855 | dfrG       | trimethoprim-resistant dihydrofolate reductase DfrG                                                        | 498    | 100.00   | 100.00   | 30.99  | 
| SRR14224855 | fosB-Saur  | FosB1/FosB3 family fosfomycin resistance bacillithiol transferase                                          | 420    | 99.29    | 100.00   | 33.94  | 
| SRR14224855 | erm(C)     | 23S rRNA (adenine(2058)-N(6))-methyltransferase Erm(C)                                                     | 735    | 99.05    | 100.00   | 34.10  | 
| SRR14224855 | ant(4')-Ia | aminoglycoside O-nucleotidyltransferase ANT(4')-Ia                                                         | 762    | 99.87    | 100.00   | 100.94 | 
| SRR14224855 | aac(6')-Ie | bifunctional aminoglycoside N-acetyltransferase AAC(6')-Ie/aminoglycoside O-phosphotransferase APH(2'')-Ia | 1440   | 100.00   | 100.00   | 82.66  | 
| SRR14224855 | blaR1      | beta-lactam sensor/signal transducer BlaR1                                                                 | 1758   | 99.15    | 100.00   | 45.90  | 
| SRR14224855 | tet(38)    | tetracycline efflux MFS transporter Tet(38)                                                                | 1353   | 100.00   | 100.00   | 62.72  | 
| SRR14224855 | blaI_of_Z  | penicillinase repressor BlaI                                                                               | 381    | 99.48    | 100.00   | 57.88  | 
| SRR14224855 | tet(L)     | tetracycline efflux MFS transporter Tet(L)                                                                 | 1377   | 100.00   | 100.00   | 48.56  | 
| SRR14224855 | ant(6)-Ia  | aminoglycoside nucleotidyltransferase ANT(6)-Ia                                                            | 864    | 100.00   | 100.00   | 50.48  | 
| SRR14224855 | spw        | ANT(9) family aminoglycoside nucleotidyltransferase Spw                                                    | 810    | 100.00   | 100.00   | 60.14  | 
| SRR14224855 | lsa(E)     | ABC-F type ribosomal protection protein Lsa(E)                                                             | 1485   | 100.00   | 100.00   | 51.94  | 
| SRR14224855 | lnu(B)     | lincosamide nucleotidyltransferase Lnu(B)                                                                  | 804    | 100.00   | 100.00   | 42.03  | 
| SRR14224855 | erm(C)     | 23S rRNA (adenine(2058)-N(6))-methyltransferase Erm(C)                                                     | 735    | 98.78    | 100.00   | 4.08   | 
| SRR14224855 | fexA       | chloramphenicol/florfenicol efflux MFS transporter FexA                                                    | 1428   | 98.88    | 100.00   | 46.28  | 
| SRR14224855 | hld        | delta-hemolysin                                                                                            | 81     | 100.00   | 100.00   | 20.65  | 
| SRR14224855 | hlgC       | bi-component gamma-hemolysin HlgCB subunit C                                                               | 948    | 95.15    | 100.00   | 49.72  | 
| SRR14224855 | lmrS       | multidrug efflux MFS transporter LmrS                                                                      | 1443   | 99.10    | 100.00   | 43.66  | 
| SRR14224855 | sel26      | staphylococcal enterotoxin type 26                                                                         | 753    | 95.75    | 99.34    | 31.14  | 
| SRR14224855 | erm(C)     | 23S rRNA (adenine(2058)-N(6))-methyltransferase Erm(C)                                                     | 735    | 98.91    | 100.00   | 6.39   | 
| SRR14224855 | sey        | staphylococcal enterotoxin type Y                                                                          | 666    | 98.80    | 100.00   | 51.46  | 

* This completed in 3.6 seconds on a 4-core laptop.

### bart-update
```sh
usage: bart-update [options]

--options [defaults]:
  -s            print available MLST schemes
  -S            -s with genes
  -p            update pubMLST schemes
  -a [ [ ...]]  path to custom scheme fasta and csv
  -r [ [ ...]]  name of scheme(s) to remove
  -amr          update AMR index
  -h            show this help message and exit
```
You can even add your own schemes to the database! You just need to
provide an allele fasta and corresponding TAB-seprarated profile mapping
file in the PubMLST format. Check out an example 
[fasta](https://rest.pubmlst.org/db/pubmlst_mflocculare_seqdef/loci/adk/alleles_fasta) 
and 
[mapping](https://rest.pubmlst.org/db/pubmlst_mflocculare_seqdef/schemes/1/profiles_csv)
file.
```sh
bart-update -a scheme.fna scheme.tab
```
Sometimes there are 2 schemes for a species which is problematic because
the heuristics will pick the same one every time. For _A. baumannii_,
I don't want the Oxford  scheme to be considered, so I simply run:
```sh
bart-update -r Acinetobacter_baumannii#1
```
### bart-profile
`bart-profile` is an interactive script which returns the ST
or closest ST(s) for a combination of alleles in a scheme.
```sh
usage: bart-profile [scheme] [ST]
```
```sh
$ bart-profile Helicobacter_cinaedi
enter allele for 23S_rRNA: 4
enter allele for ppa: 2
enter allele for aspA: 2
enter allele for aroE: 2
enter allele for atpA: 2
enter allele for tkt: 1
enter allele for cdtB: 2
scheme: Helicobacter_cinaedi	ST: 10	23S_rRNA(4)	ppa(2)	aspA(2)	aroE(2)	atpA(2)	tkt(1)	cdtB(2)	clonal_complex(9)
```
Alternatively, type STs after the scheme to display the allelic profiles.
```sh
$ bart-profile Helicobacter_cinaedi 10 11 12
scheme: Helicobacter_cinaedi	ST: 10	23S_rRNA(4)	ppa(2)	aspA(2)	aroE(2)	atpA(2)	tkt(1)	cdtB(2)	clonal_complex(9)
scheme: Helicobacter_cinaedi	ST: 11	23S_rRNA(2)	ppa(2)	aspA(2)	aroE(2)	atpA(2)	tkt(1)	cdtB(2)	clonal_complex(9)
scheme: Helicobacter_cinaedi	ST: 12	23S_rRNA(5)	ppa(5)	aspA(2)	aroE(5)	atpA(5)	tkt(1)	cdtB(3)	clonal_complex(12)
```

**References:**
* [Philip T.L.C. Clausen, Frank M. Aarestrup & Ole Lund, "Rapid and precise alignment 
  of raw reads against redundant databases with KMA", BMC Bioinformatics, 2018;19:307.
  ](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2336-6)
  
* [Jolley KA, Bray JE and Maiden MCJ. "Open-access bacterial population genomics: 
  BIGSdb software, the PubMLST.org website and their applications", 
  Wellcome Open Res 2018, 3:124
  ](https://doi.org/10.12688/wellcomeopenres.14826.1)
