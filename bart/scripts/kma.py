from subprocess import Popen, PIPE, DEVNULL
import logging


def index(infile, outfile):
    cmd = ['kma', 'index', '-i', '--', '-o', outfile]
    logger = logging.getLogger('root')
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdin=PIPE, stderr=DEVNULL)
    child.stdin.write(infile.encode())
    return child.communicate()


def kma(reads, outfile, percid, scheme, threads, readtype):
    logger = logging.getLogger('root')

    if readtype == 'pe':  #optimised for illumina paired end
        cmd = ['kma', '-ipe', reads[0], reads[1], '-ID', percid, '-o', outfile, '-t_db', scheme, '-t', threads,
               '-1t1', '-apm', 'f']

    if readtype == 'se': #optimised for pacbio
        cmd = ['kma', '-i', reads[0], '-ID', percid, '-o', outfile, '-t_db', scheme, '-t', threads]

    if readtype == 'ont': #optimised for nanopore
        cmd = ['kma', '-i', reads[0], '-ID', percid, '-o', outfile, '-t_db', scheme, '-t', threads, '-bcNano', '-1t1', '-cge' ,'-ont'  ]

    if readtype == 'int':
        cmd = ['kma', '-int', reads[0], '-ID', percid,  '-o', outfile, '-t_db', scheme, '-t', threads,
               '-1t1', '-apm', 'f']


    logger.info(f'{" ".join(cmd)}') # metrics from https://doi.org/10.1101/2020.05.28.121251

    return Popen(cmd, stderr=DEVNULL).communicate()