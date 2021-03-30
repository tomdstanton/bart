#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, DEVNULL
import logging

def index(infile, outfile):
    logger = logging.getLogger('root')
    cmd = ['kma', 'index', '-i', '--', '-o', outfile]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdin=PIPE, stderr=DEVNULL)
    child.stdin.write(infile.encode())
    return child.communicate()


def ipe(reads, outfile, percid, scheme, threads):
    logger = logging.getLogger('root')
    cmd = ['kma', '-ipe', reads[0], reads[1],
           '-ID', percid,
           '-1t1',
           #'-mrs', '90',
           '-dense',
           '-apm', 'u',
           '-o', outfile, '-t_db', scheme, '-t', threads]

    logger.info(f'{" ".join(cmd)}')
    return Popen(cmd, stderr=DEVNULL).communicate()