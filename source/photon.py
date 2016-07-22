# encoding: utf-8

# -- Libraries --
import http.server

import irc.bot
import irc.client
from jaraco.stream import buffer

from configparser import ConfigParser
import random

class Photon(irc.bot.SingleServerIRCBot):

    # Override to adapt any encodings


    def __init__(self, server, channel, port, nickname):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.nickname = nickname

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)


    def on_pubmsg(self, c, e):
        print(c.socket)
        print(e)
        if e.arguments[0] == 'nttchang おはよう':
            s = 'PRIVMSG {channel} :{string}'.format(channel=self.channel, string='黙れ')
            c.socket.send(s.encode(irc.client.ServerConnection.buffer_class.encoding) + b'\r\n')
        elif e.arguments[0] == '今日も一日':
            yo = 'が' + ''.join(random.sample('んばるぞ' ,4)) + 'い'
            s = 'PRIVMSG {channel} : {string}'.format(channel=self.channel, string=yo)
            c.socket.send(s.encode(irc.client.ServerConnection.buffer_class.encoding) + b'\r\n')


def read_config():
    parser = ConfigParser()
    parser.read('conf/default.conf') 
    return parser


def main():
    config = read_config()

    # set encoding
    irc.client.ServerConnection.buffer_class.encoding = config.get('IRC', 'encoding')

    # connect to IRC server
    server    = config.get('IRC', 'server_name')
    channel   = config.get('IRC', 'channel_name')
    port      = config.getint('IRC', 'port')
    nick_name = config.get('IRC', 'nick_name')
    bot = Photon(server, channel, port, nick_name)
    bot.start()


if __name__ == "__main__":
    main()
