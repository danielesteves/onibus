#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GPS(object):
    def __init__(self, jsonObj):
        self.datahora = jsonObj['datahora']
        self.latitude = jsonObj['latitude']
        self.linha = jsonObj['linha']
        self.longitude = jsonObj['longitude']
        self.ordem = jsonObj['ordem']
        self.sentido = jsonObj['sentido']
        self.velocidade = jsonObj['velocidade']
