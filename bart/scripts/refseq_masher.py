#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import sub
import os, logging
from subprocess import Popen, PIPE


def choose_scheme(pairs, reads, db_path):
    logger = logging.getLogger('root')
    cmd = ['refseq_masher', 'matches', pairs[reads][0]]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    for line in child[1].decode('utf-8').splitlines():
        logger.info(line.lower())
    mash_out = child[0].decode('utf-8').splitlines()[1].split('\t')[1]
    logger.info(f'closest refseq genome is {mash_out}')
    genus, species = sub(r'\W+', '', mash_out.split(' ')[0]), sub(r'\W+', '', mash_out.split(' ')[1])
    schemes = [f.name.split('.')[0] for f in os.scandir(f'{db_path}/mapping/')]
    scheme = ''

    # FIRST SOME LOGIC
    if 'Shigella' in mash_out or 'Escherichia coli' in mash_out:
        logger.warning(f'defaulting to {scheme}, use --scheme to override this behavior')
        scheme = 'Escherichia_coli#1'


    elif 'baumannii' in mash_out:
        logger.warning(f'defaulting to {scheme}, use --scheme to override this behavior')
        scheme = 'Acinetobacter_baumannii#2'


    else:
        genus_list = [s for s in schemes if genus in s]

        if not genus_list: # critical if no matching genus, exit program here and prompt to force scheme
            logger.error(f"no matching schemes for {genus}"
                         f", check available schemes with bart-update -s")
            return None

        elif len(genus_list) == 1:
            logger.info(f"only 1 scheme for {genus}, using {genus_list[0]}")
            scheme = genus_list[0]

        else: # check species now
            logger.info(f"{len(genus_list)} matching schemes for {genus}")
            species_list = list(set([g.split('_', 1)[1] for g in genus_list]))
            for s in species_list:
                if species in s:
                    logger.info(f"matched {species} to {scheme}")
                    scheme = f'{genus}_{s}'
                    break

            if not scheme:  # check to see if species is included in any schemes for genus
                logger.warning(f'no matching schemes for {species}')
                for i in genus_list:
                    with open(f'{db_path}/mapping/{i}.tab') as f:
                        if species in f.read():
                            logger.info(f'{scheme} covers {species}')
                            scheme = i
                            break

            if not scheme:  # check spp or complex schemes
                for s in species_list:
                    if 'spp' in s or 'complex' in s:
                        scheme = f'{genus}_{s}'
                        logger.info(f"{scheme} might cover your species")
                        break

            if not scheme: # finally give up
                logger.error("check available schemes with bart-update -s")
                return None

            else:
                return scheme