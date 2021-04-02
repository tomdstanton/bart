# bart
######BActerial Read Typer
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
It uses heuristics to choose the best scheme for
your reads and prints results in a standard tab-separated format.

**If you found bart helpful, please cite:**
```
bart - BActerial Read Typer
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
```
bart read_1.fq.gz read_2.fq.gz
```
It's easy to run MLST on a bunch of 
input reads and pipe the results to 
a tabular file for downstream usage.
```
bart * >> mlst.tab
```
Alternatively, if you know the species of your reads
or the specific scheme you would like to use, you can bypass
scheme choosing heuristics.
First run```bart-update --schemes```to see if it's included, now
you can run:
```
bart SRR14091226* --use-scheme Listeria_monocytogenes >> SRR14091226_mlst.tab
```
This took 4 seconds on a 4-core laptop.

Currently only works on paired-end reads. Support for
single-end and long reads is coming.