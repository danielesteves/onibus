#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..helper import ToJSON

class Itinerario(object):

    def __init__(self, jsonObj):
        self.itinerario_id = jsonObj['itinerario_id']
        self.sentido = jsonObj['sentido']
        self.brs = jsonObj['brs'] if 'brs' in jsonObj else ''
        self.polyline = jsonObj['polyline']
        self.bounding_box = jsonObj['bounding_box']
        self.gps = jsonObj['gps'] if 'gps' in jsonObj else []
        self.tempo_viagem = jsonObj['tempo_viagem']
        self.paradas = jsonObj['paradas'] if 'paradas' in jsonObj else []


    @staticmethod
    def load_from_json(jsonObj):
        return Itinerario(jsonObj)

    @ToJSON(['gps','paradas','bounding_box'])
    def to_json(self):
        pass
