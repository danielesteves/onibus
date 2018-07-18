#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging


class vadeonibus(object):
    def __init__(self, token, base_url, timeout=5):
        self._token = token
        self._base_url = base_url
        self.timeout = timeout

        self.logger = logging.getLogger('vadeonibus')


    def obterinfoversaoapp(self, plataforma = 'android', nomeVersao='3.0.3', codigoVersao ='19'):
        """Obtem informações para o APP"""
        return self._call('obterinfoversaoapp', {'plataforma': plataforma, 'nomeVersao': nomeVersao, 'codigoVersao': codigoVersao})

    def obterlistalinhas(self, consulta=''):
        """Consulta informações sobre linhas"""
        return self._call('obterlistalinhas', {'consulta': consulta})

    def obteritinerarioslinha(self, routeName='', servico='REGULAR'):
        """Consulta os itinerarios de uma linha e a posição dos ônibus em tempo real"""
        return self._call('obteritinerarioslinha', {'routeName': routeName, 'servico': servico})

    def obtermunicipiosatendidoslonlat(self, latitude='', longitude=''):
        """Consulta a lista de municipios atendidos"""
        return self._call('obtermunicipiosatendidoslonlat', {'latitude': latitude, 'longitude': longitude})

    def obterpedproximogps(self, lat='', lon='', raio='800'):
        """Consulta pontos proximos"""
        return self._call('obterpedproximogps', {'lat': lat, 'lon': lon})

    def buscarlinhasproximasgps(self, latitude='', longitude=''):
        """Consulta linhas de ônibus próximas"""
        return self._call('buscarlinhasproximasgps', {'latitude': latitude, 'longitude': longitude})

    def obterlinhasdoponto(self, ponto_id=''):
        """Consulta linhas de onibus que param no ponto"""
        return self._call('obterlinhasdoponto', {'ponto_id': ponto_id})

    def obterrotas(self, origemLogradouro, origemNumero, origemMunicipio, destinoLogradouro, destinoNumero, destinoMunicipio, raioDeBusca = '800', metodoOrdenacao = '3'):
        """Consulta rotas para os endereços informados"""
        return self._call('obterrotas', {
            'origemLogradouro': origemLogradouro,
            'origemNumero': origemNumero,
            'origemMunicipio': origemMunicipio,
            'destinoLogradouro': destinoLogradouro,
            'destinoNumero': destinoNumero,
            'destinoMunicipio': destinoMunicipio,
            'raioDeBusca': raioDeBusca,
            'metodoOrdenacao': metodoOrdenacao})

    def enderecoautocomplete(self, consulta='', municipio=''):
        """Consulta endereços a partir da string"""
        return self._call('enderecoautocomplete', {'consulta': consulta, 'municipio': municipio})


    def _call(self, endpoint, parameters):
        url = self._base_url + endpoint
        payload = {'token': self._token}
        payload = {**payload, **parameters}
        headers = {'user-agent': '5.0 (Linux; Android 5.0.1; Nexus 9 Build/LRX22C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/42.0.2311.137 Safari/537.36 SalesforceMobileSDK/3.2.0.unstable android mobile/5.0.1 (Nexus 9) MyApp/1.1 Hybrid'}

        r1 = requests.get(url, params=payload, headers=headers, timeout=self.timeout)
        return r1.json()
