#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import loads
from subprocess import Popen, PIPE, run
from os import path
from requests import get
import logging


def sketch_input(reads, sketch_out):
    logger = logging.getLogger('root')
    cmd = f'cat {reads[0]} {reads[1]} | finch sketch -o {sketch_out} -'
    logger.info(f'{cmd}')
    return run(cmd, shell=True)


def info(sketch):
    logger = logging.getLogger('root')
    cmd = ['finch', 'info', sketch]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = child.communicate()[0].decode('utf-8').split('\n')
    kmers, depth = r[1].split(': ')[1], r[2].split(': ')[1]
    gc = r[3].split(': ')[1].strip('%')
    return kmers, depth, gc


def dist(sketch, db_path):
    logger = logging.getLogger('root')
    ref = f'{db_path}/refseq_sketches_21_1000.sk'
    if not path.isfile(ref):
        logger.warning(f'{ref} not found')
        url = 'https://static.onecodex.com/public/finch-rs/refseq_sketches_21_1000.sk.gz'
        with open(ref, mode='wb') as out:
            logger.info(f'downloading {url}')
            out.write(get(url).content)
        logger.info(f'Written to {path}')

    cmd = ['finch', 'dist', sketch, ref]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = loads(child.communicate()[0])
    dist_dict = sorted(r, key=lambda k: k['mashDistance'])[:2]
    logger.info(f'closest refseq genome is {dist_dict[0]["reference"]}')
    return dist_dict[0]["reference"]
