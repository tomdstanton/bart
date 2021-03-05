# git clone https://bitbucket.org/genomicepidemiology/kma.git
# cd kma && make
#
# ./kma index -i templates.fsa.gz -o templates
# ./kma -i reads_se.fq.gz -o output/name -t_db templates
# ./kma -ipe reads_1.fq.gz reads_2.fq.gz -o output/name -t_db templates
#
#
# ./kma/kma index -i test/ab_mlst_pasteur/* -o test/ab_mlst
#
# ./kma/kma -ipe test/*R1* test/*R2* -ID 80 -o kma_test -t_db test/ab_mlst

# ./tools/kma/kma -ipe test/1543722_R1_001.fastq.gz test/1543722_R2_001.fastq.gz -t_db amr_genes -o testttt -na -nf -ID 50 -bc90 -mct 0 -t 4

# cat db/genes/Acinetobacter\ baumannii/pi* | ./tools/kma/kma index -i -- -t_db amr_genes

# http://backup.mediterranee-infection.com/arkotheque/client/ihumed/_depot_arko/articles/2042/arg-annot-v4-nt-may2018_doc.fasta
