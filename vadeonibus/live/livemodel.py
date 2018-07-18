#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import logging
import threading
import queue
import sys
import math

from urllib3.exceptions import ConnectTimeoutError

from vadeonibus.model.linha import Linha
from vadeonibus.model.itinerario import Itinerario

class LiveModel(object):

    def __init__(self, api, filter_str='', paraleling=1):
        self.api = api
        self.filter_str = filter_str
        self.paraleling = paraleling

        self.logger = logging.getLogger('LiveModel')

    def run(self):

        #carrega linhas
        self.logger.info('Carregando Linhas...')
        self.linhas = self.load_linhas(self.filter_str)
        self.logger.info('Linhas Carregadas!')

        #carrega itinerarios
        self.logger.info('Carregando Itinerarios...')
        self.linhas = self.load_itinerarios(self.linhas)
        self.logger.info('Itinerarios Carregados!')


        self.logger.info("Iniciando looping de atualização")

        while(self.keepRunning()):
            before = datetime.datetime.now()

            self.load_itinerarios(self.linhas)

            after = datetime.datetime.now()

            self.logger.info('Loop complete after {} seconds'.format((after-before).total_seconds()))

            to_sleep = (60 * 0) - (after-before).total_seconds()
            if (to_sleep > 0):
                self.logger.info('Aguardando {0} segundos para próximo update'.format(to_sleep))
                time.sleep(to_sleep)
        self.logger.info('No more runners.')

    def keepRunning(self):
        ## TODO: Implement
        return True

    def load_linhas(self, filter):
        linhas = []
        try:
            linhas_from_api = self.api.obterlistalinhas(filter)
        except ConnectTimeoutError:
            linhas_from_api = None

        if((linhas_from_api) and ('linhas' in linhas_from_api)):
            linhas = list(map(Linha.load_from_json, linhas_from_api['linhas']))

        return linhas

    def load_itinerarios_linha(self, linha):
        try:
            _itinerarios = self.api.obteritinerarioslinha(linha.route_name, linha.servico)

            if(_itinerarios and ('itinerarios' in _itinerarios)):
                linha.itinerarios = list(map(Itinerario.load_from_json, _itinerarios['itinerarios']))
            else:
                linha.itinerarios = []
        except Exception as e:
            self.logger.error('Error fetching itinerarios for line: {} {}'.format(linha.route_name, linha.vista))
            #self.logger.error('Error' + str(e))
            linha.itinerarios = []
        return linha

    def get_status(self, elapsed_seconds, initial_size, current_size, bar_size=50):
        output = '[%s%s] %d%% in %d seconds'
        percent = 1 - current_size / initial_size
        output = output % (('#' * math.floor(percent*bar_size)) , ('-' * math.floor(bar_size - percent*bar_size)), (percent*100), elapsed_seconds)
        return output

    def load_itinerarios(self, linhas, callback=None):
        def worker():
            while True:
                try:
                    linha = q.get(False)
                    sys.stdout.write('\r' + self.get_status((datetime.datetime.now()-before).total_seconds(), len(linhas), q.qsize()))
                except queue.Empty:
                    break
                try:
                    linha = self.load_itinerarios_linha(linha)
                    if(callback):
                        callback(linha)
                    q.task_done()
                except ConnectTimeoutError:
                    pass

        threads = []
        q = queue.Queue()
        for li in linhas:
            q.put(li)

        before = datetime.datetime.now()

        for tx in range(self.paraleling):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        q.join()
        for tx in threads:
            tx.join()

        return linhas

    def _linha_to_dict(self, linhas):
        _dict = {}
        for linha in linhas:
            _dict[linha.route_name] = linha.to_json().copy()
            _itinerarios = {}
            for itinerario in _dict[linha.route_name]['itinerarios']:
                _itinerarios[itinerario['itinerario_id']] = itinerario.copy()
            _dict[linha.route_name]['itinerarios'] = _itinerarios.copy()
        return _dict.copy()

    def getLinhasData(self, _linhas):
        linhas = self._linha_to_dict(_linhas)
        #Limpezad de dados para o Firebase
        for k_linha in list(linhas.keys()):
            del linhas[k_linha]['itinerarios']
        return linhas

    def getLinhasItinerariosData(self, _linhas):
        linhas = self._linha_to_dict(_linhas)
        #Limpezad de dados para o Firebase
        for k_linha in list(linhas.keys()):
            for kk_linha in list(linhas[k_linha].keys()):
                if(kk_linha not in ['itinerarios']):
                        del linhas[k_linha][kk_linha]
            for itinerario_id in linhas[k_linha]['itinerarios']:
                for k_it in list(linhas[k_linha]['itinerarios'][itinerario_id].keys()):
                    if('gps' in linhas[k_linha]['itinerarios'][itinerario_id]):
                        del linhas[k_linha]['itinerarios'][itinerario_id]['gps']
        return linhas

    def getLinhasGPSData(self, _linhas):
        linhas = self._linha_to_dict(_linhas)
        #Limpezad de dados para o Firebase
        for k_linha in list(linhas.keys()):
            for kk_linha in list(linhas[k_linha].keys()):
                if(kk_linha not in ['itinerarios']):
                        del linhas[k_linha][kk_linha]
            for itinerario_id in linhas[k_linha]['itinerarios']:
                for k_it in list(linhas[k_linha]['itinerarios'][itinerario_id].keys()):
                    if(k_it not in ['gps','tempo_viagem', 'itinerario_id']):
                        del linhas[k_linha]['itinerarios'][itinerario_id][k_it]
        return linhas

    def getLinhaGPSData(self, _linha):
        linha = self._linha_to_dict([_linha])
        linha = linha[list(linha)[0]]

        for kk_linha in list(linha.keys()):
            if(kk_linha not in ['itinerarios']):
                    del linha[kk_linha]
        for itinerario_id in linha['itinerarios']:
            for k_it in list(linha['itinerarios'][itinerario_id].keys()):
                if(k_it not in ['gps','tempo_viagem', 'itinerario_id']):
                    del linha['itinerarios'][itinerario_id][k_it]
        return linha
