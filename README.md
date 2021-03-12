# genefinda
genefinda is written in Python, optimised in Rust. \
I've tried to use as few dependencies and imports as possible.
This program is designed to be fast and very easy to use. \
There are a purposefully limited number of options 
but the bells and whistles can be

### Basic Usage ###
```genefinda reads_1.fq.gz reads_2.fq.gz [options]```

Currently only works on paired-end reads. Support for
single-end and log reads is coming... O.o

To keep genefinda light and fresh outta the box,
none of the required files are included...

Before you give an exasperated "ffs", you only need to
run 3 simple commands to get you up and running.

(these literally take like 5 minutes guys, chill)


```genefinda update indexes``` - creates kma indexes
for each PubMLST scheme.

```genefinda update schemes``` - downloads the scheme information

```genefinda update map``` - creates a scheme::species mapping file

### Issues ###
Probably lots right now, be kind, give us a shout! \
I'm not sure how genefinda will handle cases where
there are multiple schemes per species. Tbh this
shouldn't even be a thing anyway... unify your schemes people!


![alt text](logo.png)