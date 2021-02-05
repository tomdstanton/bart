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
