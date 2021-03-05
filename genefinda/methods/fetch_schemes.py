#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import pandas as pd
from glob import glob


url = 'https://rest.pubmlst.org/db/pubmlst_abaumannii_seqdef/loci/Oxf_gltA/alleles_fasta'
r = requests.get(url)


def fetch_schemes(params, outfile):
    print(f'[>] Downloading from {url}...')
        try:
            r = requests.get(url, params, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024
            t = tqdm(total=total_size, unit='iB', unit_scale=True, position=0, leave=True, )
            with open(outfile, 'wb') as f:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            # if total_size != 0 and t.n != total_size:
            #     print("\n[!] ERROR, something went wrong")
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    return outfile