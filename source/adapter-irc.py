# coding: utf-8

import photon

import irc.bot
import irc.client
from jaraco.stream import buffer


class IrcBot(irc.bot.SingleServerIRCBot):

    def __init__(self, server, channel, port, nickname):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.nickname = nickname
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        reaction = photon.proc_brain(e.arguments[0])
        if reaction:
            s = 'PRIVMSG {channel} :{string}'.format(channel=self.channel, string=reaction)
            c.socket.send(s.encode(irc.client.ServerConnection.buffer_class.encoding) + b'\r\n')


def create_bot(default_conf, irc_conf):
    irc.client.ServerConnection.buffer_class.encoding = irc_conf.get('IRC', 'encoding')

    server    = irc_conf.get('IRC', 'server_name')
    channel   = irc_conf.get('IRC', 'channel_name')
    port      = irc_conf.getint('IRC', 'port')
    nick_name = default_conf.get('COMMON', 'nick_name')
    bot = IrcBot(server, channel, port, nick_name)
    bot.start()
