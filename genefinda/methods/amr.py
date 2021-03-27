#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import get
import logging

def update_db(db_path):
    from .kma import index
    logger = logging.getLogger('root')
    url = 'https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMR_CDS'
    logger.info(f'indexing {url}')
    index(get(url).text, f'{db_path}/indexes/amr')