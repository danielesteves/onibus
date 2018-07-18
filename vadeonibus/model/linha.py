#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..helper import ToJSON

class Linha(object):
    def __init__(self, jsonObj):
        self.numero_linha = jsonObj['numero_linha']
        self.vista = jsonObj['vista']
        self.servico = jsonObj['servico']
        self.operadora = jsonObj['operadora']
        self.tarifa = jsonObj['tarifa']
        self.route_name = jsonObj['route_name']
        self.consorcio = jsonObj['consorcio']
        self.corconsorcio = jsonObj['corconsorcio']
        self.municipio = jsonObj['municipio']

        self.itinerarios = []

    @staticmethod
    def load_from_json(jsonObj):
        return Linha(jsonObj)

    @ToJSON(['itinerarios'])
    def to_json(self):
        pass
