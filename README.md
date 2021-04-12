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
First run: ```bart-update -p```\
wait a few seconds, then you're good to go!

```
bart * >> mlst.tab
```
* It's easy to run MLST on a bunch of 
input reads and pipe the results to 
a tabular file for downstream usage. For this reason,
an output option isn't included.

* bart guesses the read pairs of input
files based on the filename and suffix. Try to make
  sure the paired end read files have the same sample name.

Alternatively, if you know the species of your reads
or the specific scheme you would like to use, you can bypass
scheme choosing heuristics. For example if you have Listera reads, run:
```
bart-update -s | grep -i listeria
```
Now you can run:
```
bart SRR14091226* --use-scheme Listeria_monocytogenes >> SRR14091226_mlst.tab
```
* Sketching the input reads for containment analysis takes the 
most time so by selecting a scheme, you can speed up initial analysis.

* The read sketches are kept in your ```/tmp/``` directory until system reboot
which speeds up analysis if you want to run bart again.

**Output example:**

| Sample      | Scheme                 | ST  | abcZ | bglA | cat | dapE | dat | ldh | lhkA | CC   | Lineage | 
|-------------|------------------------|-----|------|------|-----|------|-----|-----|------|------|---------| 
| SRR14091226 | Listeria_monocytogenes | 451 | 7    | 5    | 10  | 21   | 1   | 4   | 1    | CC11 | II      |

* (*) indicates alleles have less than 100% identity
* (?) indicates alleles have less than 100% coverage

### bart-update
The ```bart-update``` script handles the scheme manipulation and has several options:
* ```-s``` prints all available MLST schemes in database
* ```-p``` indexes all schemes from pubmlst (this sounds slow but takes <1 min)
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
bart-update -a scheme.fna scheme.tab
```
Sometimes there are 2 schemes for a species which is problematic because
the heuristics will pick the same one every time. For _A. baumannii_,
I don't want the Oxford  scheme to be considered, so I simply run:
```
bart-update -r Acinetobacter_baumannii#1
```

**Bugs / issues / development:**
* Currently only works on paired-end reads. Support for
single-end and long reads is coming.

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