# ba(cterial) r(ead) t(yper)
![Image](https://github.com/tomdstanton/bart/blob/master/Bart_Simpson_200px.png)

_By Tom Stanton_ \
Schneiders Lab - University of Edinburgh

Issues/queries/advice?
[email me!](mailto:s1895738@ed.ac.uk?subject=[bart])

[![alt text][1.1]][1]
[![alt text][6.1]][6]

[1]: http://twitter.com/tomstantonmicro
[1.1]: http://i.imgur.com/tXSoThF.png (twitter icon with padding)
[6]: http://www.github.com/tomdstanton
[6.1]: http://i.imgur.com/0o48UoR.png (github icon with padding)

### Introduction
bart is a short-read bacterial MLST tool,
designed to be very not-slow and very easy to use.
It can guess the species and choose the best scheme for
your reads and outputs a single tab-separated line.
You can also ue bart to get genome metrics of your reads
such as estimated size, coverage, %GC and species containment.

**Please cite:**
```
bart - ba(cterial) r(ead) t(yper)
Thomas David Stanton, 2021
https://github.com/tomdstanton/bart
```
### Dependencies
```
python >=3.8
kma
finch
```
### Installation
Clone repo and install with python:
```
git clone --recursive https://github.com/tomdstanton/bart
cd bart
python setup.py install
```
### Usage ###
Before first use, run this quick command to
index the latest MLST schemes from PubMLST: \
```
bart --update mlst
```
Now you can run:
```
bart -i read_1.fq.gz read_2.fq.gz --mlst
```
It's easy to run MLST on a bunch of 
input reads and pipe the results to 
a tabular file for downstream usage. Just suppress
output with the quiet flag and you're golden.
```
bart -i *.fq.gz --mlst -q >> mlst.tab
```
Alternatively, if you know the species of your reads
or the specific scheme you would like to use, you can speed 
up the analysis.
First run```bart --schemes```to see if it's included, now
you can run:
```
bart -i *.fq.gz --mlst --use_scheme Acinetobacter_baumannii#2
```
Currently only works on paired-end reads. Support for
single-end and long reads is coming.