#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import logging

class InThreads(object):

    def __init__(self, argument):
        self.argument = argument
        self.num_threads = 1

        self.logger = logging.getLogger('InThreads')

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            self.num_threads = args[0].paraleling if args[0].paraleling is not None and isinstance(args[0].paraleling, int) else 1
            output = []
            threads = []

            self.logger.debug('Running annotated method in ' + str(self.num_threads) + ' threads')

            #for s_arg in self._split_argument_list(args[self.argument]):
            #    new_arg = list(args)
            #    new_arg[self.argument] = s_arg
            #    f(*tuple(new_arg))

            for s_arg in self._split_argument_list(args[self.argument]):
                new_arg = list(args)
                new_arg[self.argument] = s_arg
                t= threading.Thread(target=f, args=[*tuple(new_arg)])
                t.start()
                threads.append(t)
            for t in threads:
                t.join()

        return wrapped_f

    def _split_argument_list(self, argument):
        if(type(argument) is not list):
            raise Exception()
        if(self.num_threads == 1):
            return [argument]

        return [argument[i::self.num_threads] for i in range(self.num_threads)]

class ToJSON(object):
    def __init__(self, atributes=[]):
        self.atributes = atributes

    def get_values(self, value):
        if (callable(getattr(value,'to_json',None))):
            return value.to_json()
        if (type(value) == dict):
            return value
        if (type(value) == list):
            return [self.get_values(v) for v in value]
        return value.__dict__

    def __call__(self, f):
        def wrapped_f(*args):
            obj = args[0]
            obj_dict = obj.__dict__
            for attr in self.atributes:
                obj_dict[attr] = self.get_values(obj_dict[attr])
            return obj_dict

            #return f(*args)
        return wrapped_f
