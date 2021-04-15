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
bart is a short-read bacterial MLST tool,
designed to be very not-slow and very easy to use.
It uses heuristics to choose the best scheme for
your reads and prints results in a standard tab-separated format.

**If you found bart helpful, please cite:**
```
bart - BActerial Read Typer
Thomas David Stanton, 2021
https://github.com/tomdstanton/bart
```
### Dependencies
* Linux (might work on Mac, not tested)
* python >=3.7
* [kma](https://anaconda.org/bioconda/kma)
* [finch](https://github.com/onecodex/finch-rs) (binary included)

## Installation
Clone repo and install with python:
```
git clone --recursive https://github.com/tomdstanton/bart
cd bart
python setup.py install
```
### Usage
```
$ bart reads >> mlst.tab
```
I like to test bart on SRA reads like so:
```
$ fasterq-dump SRR14224855 -S && pigz SRR14224855* && bart SRR14224855*
```
* Sketching the input reads for containment analysis takes the 
most time so by selecting a scheme, you can speed up initial analysis.
* The read sketches are kept in your ```/tmp/``` directory until system reboot
which speeds up analysis if you want to run bart again.
If you already know the species of your reads
or the specific scheme you would like to use, you can bypass
scheme choosing heuristics. For example if you have Staphylococcus reads,
see if the scheme is included:
```
$ bart-update -s | grep -i Staphylococcus
Staphylococcus_aureus
Staphylococcus_chromogenes
Staphylococcus_epidermidis
Staphylococcus_haemolyticus
Staphylococcus_hominis
Staphylococcus_lugdunensis
Staphylococcus_pseudintermedius
```
Now you can run:
```
$ bart SRR14224855* --use-scheme Staphylococcus_aureus
```
| Sample      | Scheme                | ST   | arcC! | aroE | glpF | gmk | pta | tpi | yqiL | clonal_complex | 
|-------------|-----------------------|------|-------|------|------|-----|-----|-----|------|----------------| 
| SRR14224855 | Staphylococcus_aureus | 9    | 3     | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 

* (*) indicates alleles have less than 100% identity
* (?) indicates alleles have less than 100% coverage
* (!) indicates alleles have less than 100% coverage and identity

It looks like we have a novel allele for _arcC_!

By default, bart will assume that the allele for non-exact 
hits is the most similar to the novel allele 
and will assign a profile with this assumption.

Passing the ```--exact``` flag with make
bart display the closest profiles based on exact allele hits only.
```
$ bart SRR14224855* --use-scheme Staphylococcus_aureus --exact
```
| Sample      | Scheme                | ST   | arcC! | aroE | glpF | gmk | pta | tpi | yqiL | clonal_complex | 
|-------------|-----------------------|------|-------|------|------|-----|-----|-----|------|----------------| 
| SRR14224855 | Staphylococcus_aureus | 9    | 3     | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 63   | 1     | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 706  | 86    | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 1569 | 244   | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 2423 | 262   | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 4987 | 5     | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 5471 | 657   | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 5717 | 331   | 3    | 1    | 1   | 1   | 1   | 10   | CC1            | 
| SRR14224855 | Staphylococcus_aureus | 6556 | 767   | 3    | 1    | 1   | 1   | 1   | 10   | CC1            |

### bart-update
The ```bart-update``` script handles the scheme manipulation and has several options:
* ```-s``` prints all available MLST schemes in database
* ```-p``` updates and indexes all schemes from pubmlst (this sounds slow but takes <1 min)
* ```-a``` adds a custom scheme from a fasta and tab mapping file
* ```-r``` removes the listed schemes in the database

You can even add your own schemes to the database! You just need to
provide an allele fasta and corresponding TAB-seprarated profile mapping
file in the PubMLST format. Check out an example 
[fasta](https://rest.pubmlst.org/db/pubmlst_mflocculare_seqdef/loci/adk/alleles_fasta) 
and 
[mapping](https://rest.pubmlst.org/db/pubmlst_mflocculare_seqdef/schemes/1/profiles_csv)
file.
```
$ bart-update -a scheme.fna scheme.tab
```
Sometimes there are 2 schemes for a species which is problematic because
the heuristics will pick the same one every time. For _A. baumannii_,
I don't want the Oxford  scheme to be considered, so I simply run:
```
$ bart-update -r Acinetobacter_baumannii#1
```

**Bugs / issues / development:**
* Currently only works on paired-end reads. Support for
single-end and long reads is coming.
* bart guesses the read pairs of input 
  files based on the filename and suffix. Try to make 
  sure the paired end read files have the same sample name.

**References:**
* [Philip T.L.C. Clausen, Frank M. Aarestrup & Ole Lund, "Rapid and precise alignment 
  of raw reads against redundant databases with KMA", BMC Bioinformatics, 2018;19:307.
  ](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2336-6)
  
* [Jolley KA, Bray JE and Maiden MCJ. "Open-access bacterial population genomics: 
  BIGSdb software, the PubMLST.org website and their applications", 
  Wellcome Open Res 2018, 3:124
  ](https://doi.org/10.12688/wellcomeopenres.14826.1)
  
* [Bovee et al., (2018). Finch: a tool adding dynamic abundance filtering to genomic 
MinHashing. Journal of Open Source Software, 3(22), 505
](https://doi.org/10.21105/joss.00505)