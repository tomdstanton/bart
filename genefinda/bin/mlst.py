#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher, get_close_matches
from collections import defaultdict
from os import scandir
from re import DOTALL, findall
from requests import get
import logging

def update_db(db_path):
    from .kma import index
    logger = logging.getLogger('root')
    # [f.unlink() for f in Path(f'{db_path}/mapping/').glob("*") if f.is_file()]
    for s in findall('<species>(.*?)</species>',
                     get('https://pubmlst.org/static/data/dbases.xml').text, DOTALL):
        scheme = s.split('\n')
        name = scheme[0].replace(' ','_').replace('/','_').strip('.')
        urls = []
        for l in scheme:
            if any(ft in l for ft in ['csv', 'fasta']):
                urls.append(l.split('>')[1].split('<')[0])

        with open(f'{db_path}/mapping/{name}.tab', 'ab') as f:
            f.write(get(urls[0]).content)
        logger.info(f'written scheme map to {db_path}/mapping/{name}.tab')
        i = ''
        for url in urls[1:]:
            i += get(url).text
        index(i, f'{db_path}/indexes/{name}')


def choose_scheme(finch_out, db_path):
    logger = logging.getLogger('root')
    d = [f.name.split('.')[0] for f in scandir(f'{db_path}/mapping/')]
    finch_out = finch_out.replace(' ','_')
    search_string = ''
    for i in finch_out.split('_'):
        search_string += f'{i}_'
        matches = get_close_matches(search_string.strip('_'), d)
        if len(matches) == 1:
            break
        elif len(matches) > 1:
            logger.info(f'multiple schemes for {search_string.strip("_")}, refining search')
            continue
        elif search_string.strip('_') == finch_out:
            logger.info(f'multiple schemes for {search_string.strip("_")}, will use {matches}')
            break
    return matches[0]


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

    for i in exact:
        for st in list(scheme_dict.keys()):
            if scheme_dict[st][i] != res_dict[i][0]:
                #logger.info(f'removing {st} due to --exact')
                scheme_dict.pop(st)

    if len(scheme_dict.keys()) > 1:
        scheme_match = defaultdict(list)
        for st in scheme_dict.keys():
            profile = []
            for k, v in scheme_dict[st].items():
                if k in res_dict.keys() & genes:
                    profile.append(v)
            scheme_match[SequenceMatcher(None, profile, y).ratio()].append(st)
        scheme_match = sorted(scheme_match.items(), key=lambda item: item[0], reverse=True)[0]
        if len(scheme_match[1]) > 1:
            logger.info(f'{len(scheme_match[1])} close matches found')
        sts = scheme_match[1]

    else:
        sts = scheme_dict.keys()

    for st in sts:
        out = [sample, scheme, st]#({int(scheme_match[0]*100)}%)']
        for k, v in scheme_dict[st].items():
            if k in headers:
                if  v != '':
                    out.append(f'{k}({v})')
            else: out.append(f'{k} no hit')
    return out



def print_schemes(db_path):
    d = [f.name.split('.')[0] for f in scandir(f'{db_path}/mapping/')]
    return print(*sorted(d), sep="\n")