#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger
from json import loads
from subprocess import Popen, PIPE
from requests import get

logger = getLogger('\x1b[6;30;42m' + 'finch' + '\x1b[0m')
finch = '/home/tom/.cargo/bin/finch'

def get_ref(path):
    url = 'https://static.onecodex.com/public/finch-rs/refseq_sketches_21_1000.sk.gz'
    # need to gunzip
    with open(path, 'wb') as out:
        logger.info(f'Downloading {url}')
        out.write(get(url).content)
        logger.info(f'Written to {path}')
    return path

def sketch_input(reads, sketch):
    cmd = ['finch', 'sketch', '-o', sketch, '-']
    logger.info(f'Running: {" ".join(cmd)}')
    child = Popen(cmd, stdin=PIPE)
    child.stdin.write(reads.encode())
    return child.communicate()

def info(sketch):
    cmd = [finch, 'info', sketch]
    logger.info(f'Running: {" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = child.communicate()[0].decode('utf-8').split('\n')
    return [r.slice(1,3,1).split(': ')] #uniq_kmers, ave_depth, gc%

def dist(sketch, ref):
    cmd = [finch, 'dist', sketch, ref]
    logger.info(f'Running: {" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = loads(child.communicate()[0])
    return sorted(r, key=lambda k: k['mashDistance'])[0]