#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import User
import Situation
import Sistem
import pickle
import time


class Pingponger:
    def __init__(self, a_number, interfaces={}, users_database=None, situations_database=None):
        self.a_number = a_number
        self.interfaces = interfaces
        
        self.users = []
        # todo - importing users from databse

        self.situations = []
        # todo - importing situations from databse

        self.sistems = []
        # todo - importing sistems from databse

    def load_from_dump(self, filename):
        try:
            f = open(filename, 'rb')
            return pickle.load(f)
        except Exception:
            return self

    def update(self):
        Situation.Situation(None, update_max_id=len(self.situations)-1)
        Sistem.Sistem(None, update_max_id=len(self.sistems)-1)
        User.User(None, {}, update_max_id=len(self.sistems)-1)

    def dump_interfaces(self):
        reversed_interface_dict = {}
        for key in self.interfaces:
            reversed_interface_dict[self.interfaces[key]] = key
        
        for sit in self.situations:
            sit.interface = reversed_interface_dict[sit.interface]
        
        ret = self.interfaces
        self.interfaces = {}
        return ret

    def load_interfaces(self, interfaces):
        self.interfaces = interfaces

        for sit in self.situations:
            sit.interface = self.interfaces[sit.interface]

    def add_interface(self, key, interface):
        self.interfaces[key] = interface

    def register_user(self, name, interface_ids_dict):
        user = User.User(name, interface_ids_dict)
        self.users.append(user)

    def add_situation(self, situation):
        self.situations.append(situation)

        usr = situation.user
        print(usr.sistems)
        for sis in usr.sistems:
            if not sis in usr.muted:
                sis.add_situation(situation)
        
        usr.created_situation(situation)

    def add_sistem(self, sistem):
        self.sistems.append(sistem)

    def remove_situation(self, situation):
        situation.end_time = int(time.time())
    
    def init_situation_creation(self, user):
        pass

    def user_by_tg_chat_id(self, chat_id):
        for user in self.users:
            if user.tg_chat_id == chat_id:
                return user
        return None

    def situation_by_id(self, id):
        for sit in self.situations:
            if sit.id == id and sit.status != Situation.FINISHED:
                return sit
        return None

    def sistem_by_id(self, id):
        for sis in self.sistems:
            if sis.id == id:
                return sis
        return None

    def remove_sistem(self, sis):
        sis.delete()
        del self.sistems[self.sistems.index(sis)]

    def check_situations(self):
        for sit in self.situations:
            sit.check()

    def text_dump(self):
        print(self.situations)
        print(self.users)
