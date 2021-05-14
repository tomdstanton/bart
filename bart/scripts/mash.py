import logging
import os
from re import sub
from subprocess import Popen, PIPE


def choose_scheme(sample, pairs, reads, db_path):
    logger = logging.getLogger('root')

    t = '/tmp/choose_scheme.bart'  # Check /tmp/choose_scheme.bart
    if os.path.isfile(t):
        with open(t) as f:
            x = [i.split('\t')[1].strip() for i in f.readlines() if sample in i]
        if len(x) == 1:
            logger.info(f'{sample} found in {t}, using {x[0]}')
            return x[0]

    # Run refseq_masher
    cmd = ['refseq_masher', 'matches', pairs[reads][0]]
    logger.info(f'{" ".join(cmd)}')
    child = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    for line in child[1].decode('utf-8').splitlines():
        logger.info(line.lower())

    # Parse output
    mash_out = child[0].decode('utf-8').splitlines()[1].split('\t')[1]
    logger.info(f'closest refseq genome is {mash_out}')
    genus, species = sub(r'\W+', '', mash_out.split(' ')[0]), sub(r'\W+', '', mash_out.split(' ')[1])
    schemes = [f.name.split('.')[0] for f in os.scandir(f'{db_path}/mapping/')]

    # FIRST SOME LOGIC
    if 'Shigella' in mash_out or 'Escherichia coli' in mash_out:
        logger.warning('defaulting to Escherichia_coli#1, use -s to override this behavior')
        scheme = 'Escherichia_coli#1'

    elif 'baumannii' in mash_out:
        logger.warning('defaulting to Acinetobacter_baumannii#2, use -s to override this behavior')
        scheme = 'Acinetobacter_baumannii#2'

    else:
        genus_list = [s for s in schemes if genus in s]

        if not genus_list:  # critical if no matching genus, exit program here and prompt to force scheme
            logger.error(f"no matching schemes for {genus}"
                         f", check available schemes with bart-update -s")
            return None

        elif len(genus_list) == 1:
            logger.info(f"only 1 scheme for {genus}, using {genus_list[0]}")
            scheme = genus_list[0]

        else:  # check species now
            scheme = ''
            logger.info(f"{len(genus_list)} matching schemes for {genus}")
            species_list = list(set([g.split('_', 1)[1] for g in genus_list]))
            for s in species_list:
                if species in s:
                    logger.info(f"matched {species} to {s}")
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

    with open(t, 'a') as f:
        f.write(f'{sample}\t{scheme}\n')
    return scheme
