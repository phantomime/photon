# -- Libraries --
import http.server

import irc.bot
import irc.client
from jaraco.stream import buffer

from configparser import ConfigParser


class Photon(irc.bot.SingleServerIRCBot):
    def __init__(self, server, channel, port, nickname):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)


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
