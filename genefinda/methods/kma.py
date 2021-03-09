#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger
from subprocess import Popen, PIPE

logger = getLogger('\x1b[6;30;42m' + 'kma' + '\x1b[0m')

def index(infile, outfile):
    cmd = ['kma', 'index', '-i', '--', '-o', outfile]
    logger.info(f'Running: {" ".join(cmd)}')
    child = Popen(cmd, stdin=PIPE)
    child.stdin.write(infile.encode())
    return child.communicate()

def ipe(reads, id, index, threads):
    cmd = ['kma', '-ipe', reads, '-ID', id,
           '-o', '/dev/stdout', '-t_db', index, '-t', threads]
    # -na -nf -bc90 -mct 0
    logger.info(f'Running: {" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    return child.communicate()[0].decode()