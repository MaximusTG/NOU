#!/usr/bin/env python3  
# -*- coding: utf-8 -*-


from threading import Thread
import Pingponger
import Tg_interface
import telebot
import time
import pickle


PP = Pingponger.Pingponger(6319)
token = '779667318:AAFO_3Ptkf2Y7uYstagrckMrBqpt9criQEo'
bot = telebot.TeleBot(token)


DUMP_FILE = 'pp.txt'


@bot.message_handler(func=lambda x: True)
def recieve_message(message):
    PP.interfaces['telegram'].handle(message)


def launch_tg_bot(bot):
    print('Starting telegram bot')
    bot.polling(interval=1)
    print('Telegram bot shut down')


def everysecond_check():
    t = 0
    while True:
        t += 1
        if t % 5 == 2:
            print('[{}]Checking is OK.'.format(int(time.time())))
            f = open(DUMP_FILE, 'wb')
            interfaces = PP.dump_interfaces()
            pickle.dump(PP, f)
            PP.load_interfaces(interfaces)
            f.close()

        PP.check_situations()
        time.sleep(1)


def main():
    global PP
    global INTERFACES
    INTERFACES = {}
    PP = PP.load_from_dump(DUMP_FILE)
    PP.update()
    print('Starting PingPonger, current time = {}'.format(int(time.time())))


    TG_INTERFACE_OBJECT = Tg_interface.TgBot(PP, 'TgBot', bot)
    INTERFACES['telegram'] = TG_INTERFACE_OBJECT

    PP.load_interfaces(INTERFACES)

    tg_bot_thread = Thread(target=launch_tg_bot, args=(bot,))
    tg_bot_thread.start()

    everysecond_check_thread = Thread(target=everysecond_check)
    everysecond_check_thread.start()


if __name__ == "__main__":
    main()
