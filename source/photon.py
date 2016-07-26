# encoding: utf-8

# -- Libraries --
import http.server

import irc.bot
import irc.client
from jaraco.stream import buffer

from configparser import ConfigParser
import argparse
import importlib
import yaml
import re
import subprocess


#class Photon(irc.bot.SingleServerIRCBot):
#
#    def __init__(self, server, channel, port, nickname, brain):
#        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
#        self.channel = channel
#        self.nickname = nickname
#        self.brain = brain
#
#    def on_nicknameinuse(self, c, e):
#        c.nick(c.get_nickname() + "_")
#
#    def on_welcome(self, c, e):
#        c.join(self.channel)
#
#    def on_pubmsg(self, c, e):
#        reaction = self._proc_brain(self.brain, e.arguments[0])
#        if reaction:
#            s = 'PRIVMSG {channel} :{string}'.format(channel=self.channel, string=reaction)
#            c.socket.send(s.encode(irc.client.ServerConnection.buffer_class.encoding) + b'\r\n')

# do reaction from the received strings
def proc_brain(string):
    brain = load_brain()
    for b in brain:
        if re.match(b['keyword'], string):
            reaction = b['reaction']

            # judge what kind of reaction should be done
            if reaction['type'] == 'say':
                return reaction['do']
            elif reaction['type'] == 'cmd':
                return _do_command(reaction['do'])

    # return None if no keyword matched to the received string
    return None

# do Shell Commnad and return STDOUT
def _do_command(command):
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()
    ret = stdout.decode('utf-8')
    return ret


def read_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-a')
    args = p.parse_args()
    return args


def read_config(adapter):
    default_parser = ConfigParser()
    default_parser.read('conf/default.conf')

    adapter_parser = ConfigParser()
    adapter_parser.read('conf/{adapter}.conf'.format(adapter=adapter))
    return default_parser, adapter_parser


def load_brain():
    with open('brain/brain.yml', 'r') as f:
        return yaml.load(f)


def main():
    args = read_arguments()
    adapter = args.a

    default_config, adapter_config = read_config(adapter)

    

    # set encoding
    # irc.client.ServerConnection.buffer_class.encoding = config.get('IRC', 'encoding')

    # analyze brain.yml
    global brain
    brain = load_brain()
    print(brain)

    # connect to IRC server
    # server    = config.get('IRC', 'server_name')
    # channel   = config.get('IRC', 'channel_name')
    # port      = config.getint('IRC', 'port')
    # nick_name = config.get('IRC', 'nick_name')
    # bot = Photon(server, channel, port, nick_name, brain)
    # bot.start()

    m = importlib.import_module('adapter-{adapter}'.format(adapter=adapter))
    m.create_bot(default_config, adapter_config)


if __name__ == "__main__":
    brain = None
    main()
