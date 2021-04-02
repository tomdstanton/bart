#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher
from collections import defaultdict
from os import scandir
import logging

def choose_scheme(finch_out, db_path):
    logger = logging.getLogger('root')
    d = [f.name.split('.')[0] for f in scandir(f'{db_path}/mapping/')]
    genus = set([g.split('_')[0] for g in d])

    for i in genus:
        if SequenceMatcher(None, finch_out.split(' ')[0], i).ratio() == 1:
            d = [k for k in d if i in k]

    # More critical if no matching genus, good idea to exit program here and prompt to force scheme
    if len(d) < 1:
        logger.error(f"no matching schemes for {finch_out.split(' ')[0]}, check available schemes with bart --schemes")

    else: # check species now, if #1/#2 like in Ab, need to account for that
        logger.info(f"{len(d)} matching schemes for genus {finch_out.split(' ')[0]}")
        species = set([g.split('_')[1].split('#')[0] for g in d])
        s = []
        for i in species:
            if SequenceMatcher(None, finch_out.split(' ')[1], i).ratio() == 1:
                s.append(f'{finch_out.split(" ")[0]}_{i}')

        if len(s) >= 1:
            logger.info(f"matched species {finch_out.split(' ')[1]} to scheme {s[0]}")
            return s[0]

        else:
            logger.warning(f"no matching schemes for species {finch_out.split(' ')[1]}")
        # first go with spp, then try genus scheme with most alleles
            if 'spp' in species:
                d = [k for k in d if 'spp' in k]
            else:
                top_profiles = 0
                for i in species:
                    with open(f'{db_path}/mapping/{finch_out.split(" ")[0]}_{i}.tab', "r") as f:
                        profiles = len(f.readlines())
                        if profiles > top_profiles:
                            top_profiles = profiles
                            d = [f'{finch_out.split(" ")[0]}_{i}']

            logger.warning(f"{d[0]} might cover your species")

    return d[0]


def match_profile(sample, scheme, db_path):
    logger = logging.getLogger('root')
    with open(f'/tmp/{sample}.res', newline='\n') as res:
        r = res.read().splitlines()
    res_dict = {}
    for line in r[1:]:
        v = line.split('\t')
        v = [x.strip(' ') for x in v]
        k = v[0].rsplit('_', 1)[0]
        v[0] = v[0].rsplit('_', 1)[1]
        if k in list(res_dict):
            if int(v[1]) > int(res_dict[k][1]):
                res_dict[k] = v
        else:
            res_dict[k] = v

    scheme_dict = {}
    with open(f'{db_path}/mapping/{scheme}.tab', newline='\n') as tab:
        s = tab.read().splitlines()
    headers = s[0].split('\t')[1:]
    for line in s[1:]:
        v = line.split('\t')
        scheme_dict[int(v[0])] = {headers[i]: v[1:][i] for i in range(len(headers))}

    genes = [g for g in headers if g not in ['clonal_complex', 'species']]

    y = []
    for k, v in res_dict.items():
        if k in genes:
            y.append(v[0])

    exact = []
    for k, v in res_dict.items():
        if v[4] == '100.00' and v[5] == '100.00':
            exact.append(k)
        else:
            logger.info(f'potential novel allele for {k}')

    exact_dict = {}
    for i in exact:
        for st in list(scheme_dict.keys()):
            if scheme_dict[st][i] == res_dict[i][0]:
                #logger.info(f'removing {st} due to --exact')
                exact_dict[st] = scheme_dict[st]

    if len(exact_dict) != 1:
        logger.info(f'no exact profile match, finding closest')
        scheme_match = defaultdict(list)
        for st in scheme_dict.keys():
            profile = []
            for k, v in scheme_dict[st].items():
                if k in res_dict.keys() & genes:
                    profile.append(v)
            scheme_match[SequenceMatcher(None, profile, y).ratio()].append(st)

        # Invert the dictionary so match scores are keys and sort by key to take best ST match
        scheme_match = sorted(scheme_match.items(), key=lambda item: item[0], reverse=True)[0]

        if len(scheme_match[1]) > 1:
            logger.info(f'{len(scheme_match[1])} close matches found')
        sts = scheme_match[1]

    else:
        scheme_dict = exact_dict
        sts = scheme_dict.keys()

    print('Sample\tST\t'+"\t".join([str(x) for x in headers]))
    for st in sts:
        out = sample+'\t'+str(st)
        for k, v in scheme_dict[st].items():
            if k in headers:
                if v != '':
                    out += '\t'+v
            else: out += '\tno hit'
        print(out)

