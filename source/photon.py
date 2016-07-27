# encoding: utf-8

# -- Libraries --
from configparser import ConfigParser
import argparse
import importlib
import yaml
import re
import subprocess


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

    m = importlib.import_module('adapter-{adapter}'.format(adapter=adapter))
    m.create_bot(default_config, adapter_config)


if __name__ == "__main__":
    brain = None
    main()
