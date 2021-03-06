#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import Situation
import Sistem


class User:
    max_id = 0
    def __init__(self, name, interface_ids_dict, update_max_id=0):
        User.max_id += 1
        self.id = User.max_id

        self.name = name
        for key in interface_ids_dict:
            self.add_interface(key, interface_ids_dict[key])

        self.situations = []
        self.own_situations = []

        self.creating_situation = 0
        self.new_situation = Situation.Situation(self)

        self.creating_sistem = 0
        self.new_sistem = Sistem.Sistem(self)

        self.sistems = []
        self.muted = []

        if update_max_id:
            User.max_id = update_max_id

    def add_interface(self, key, value):
        self.__dict__[key] = value

    def add_situation(self, situation):
        if self in situation.pingers:
            return False

        situation.connect_pinger(self)
        User.max_id = len(situation.interface.platform.users) - 1
        self.situations.append(situation)

        return True

    def remove_situation(self, situation):
        for i in range(len(self.situations)):
            sit = self.situations[i]
            if sit == situation:
                sit.disconnect_pinger(self)
                del self.situations[i]

    def join_sistem(self, sistem):
        if sistem in self.sistems:
            return False
        else:
            self.sistems.append(sistem)
            return True

    def exit_sistem(self, sistem):
        del self.sistems[self.sistems.index(sistem)]

    def created_situation(self, situation):
        print(self.own_situations)
        self.own_situations.append(situation)
        for sis in self.sistems:
            if not sis in self.muted:
                sis.add_situation(situation)

    def ponged(self):
        for sit in self.own_situations:
            if sit.status == Situation.RUNNING:
                print('sit[{}] ponged'.format(sit.name))
                sit.ponged()

    def get_sistem_list(self):
        text = ''
        for i in range(len(self.sistems)):
            sis = self.sistems[i]
            text += '{}) \n'.format(sis.name)
        text = text[:-1]
        return text
