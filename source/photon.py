# encoding: utf-8

# -- Libraries --
import http.server

import irc.bot
import irc.client
from jaraco.stream import buffer

from configparser import ConfigParser
import yaml
import re
import subprocess


class Photon(irc.bot.SingleServerIRCBot):

    def __init__(self, server, channel, port, nickname, brain):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.nickname = nickname
        self.brain = brain

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        reaction = self._proc_brain(self.brain, e.arguments[0])
        if reaction:
            s = 'PRIVMSG {channel} :{string}'.format(channel=self.channel, string=reaction)
            c.socket.send(s.encode(irc.client.ServerConnection.buffer_class.encoding) + b'\r\n')

    # do reaction from the received strings
    def _proc_brain(self, brain, string):
        for b in brain:
            if re.match(b['keyword'], string):
                reaction = b['reaction']

                # judge what kind of reaction should be done
                if reaction['type'] == 'say':
                    return reaction['do']
                elif reaction['type'] == 'cmd':
                    return self._do_command(reaction['do'])

        # return None if no keyword matched to the received string
        return None

    # do Shell Commnad and return STDOUT
    def _do_command(self, command):
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, _ = p.communicate()
        ret = stdout.decode('utf-8')
        return ret


def read_config():
    parser = ConfigParser()
    parser.read('conf/default.conf') 
    return parser


def load_brain():
    with open('brain/brain.yml', 'r') as f:
        return yaml.load(f)


def main():
    config = read_config()

    # set encoding
    irc.client.ServerConnection.buffer_class.encoding = config.get('IRC', 'encoding')

    # analyze brain.yml
    brain = load_brain()
    print(brain)

    # connect to IRC server
    server    = config.get('IRC', 'server_name')
    channel   = config.get('IRC', 'channel_name')
    port      = config.getint('IRC', 'port')
    nick_name = config.get('IRC', 'nick_name')
    bot = Photon(server, channel, port, nick_name, brain)
    bot.start()


if __name__ == "__main__":
    main()
