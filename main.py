#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config

from vadeonibus.api.vadeonibus import vadeonibus
from vadeonibus.live.livemodel import LiveModel

import os
from dotenv import load_dotenv



def main():
    load_dotenv(dotenv_path='.env', verbose=True)

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger('Main')
    logger.info('Stating Vadeonibus Data Loader')

    #API Parameters
    TOKEN = os.getenv("TOKEN")
    URL_BASE_WS = os.getenv("URL_BASE_WS")

    api = vadeonibus(TOKEN, URL_BASE_WS, 2)
    mantainer = LiveModel(api, '', 4)

    #run mantainer
    mantainer.run()

    logger.info('Leaving application')

if __name__ == '__main__':
    main()
