#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import loads
from subprocess import Popen, PIPE, run
import os
from requests import get
import logging
import gzip
from shutil import copyfileobj


def sketch_input(finch, reads, sketch_out):
    logger = logging.getLogger('root')
    cmd = f'cat {reads[0]} {reads[1]} | {finch} sketch -o {sketch_out} -'
    logger.info(f'{cmd}')
    return run(cmd, shell=True)


def info(sketch, finch):
    logger = logging.getLogger('root')
    cmd = [finch, 'info', sketch]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = child.communicate()[0].decode('utf-8').split('\n')
    kmers, depth = r[1].split(': ')[1], r[2].split(': ')[1]
    gc = r[3].split(': ')[1].strip('%')
    return kmers, depth, gc


def dist(sketch, db_path, finch):
    logger = logging.getLogger('root')

    db_path = '/bart/db'
    ref = f'{db_path}/refseq_sketches_21_1000.sk'

    if not os.path.isfile(ref):
        logger.warning(f'{ref} not found')
        url = 'https://static.onecodex.com/public/finch-rs/refseq_sketches_21_1000.sk.gz'
        with open(f'{ref}.gz', mode='wb') as out:
            logger.info(f'downloading {url}')
            out.write(get(url).content)
        with gzip.open(f'{ref}.gz', 'r') as f_in, open(ref, 'wb') as f_out:
            logger.info(f'decompressing')
            copyfileobj(f_in, f_out)
        os.remove(f'{ref}.gz')
        logger.info(f'written to {ref}')

    cmd = [finch, 'dist', sketch, ref]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE)
    r = loads(child.communicate()[0])
    dist_dict = sorted(r, key=lambda k: k['mashDistance'])[:2]
    return dist_dict[0]["reference"]
