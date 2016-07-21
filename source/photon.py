import http.server
import irc.bot
import irc.client
from jaraco.stream import buffer


class Photon(irc.bot.SingleServerIRCBot):
    pass


def main():
    
    # set encoding
    client.ServerConnection.buffer_class.encoding = 

    # connect to IRC server
    bot = Photon()
    bot.start()


if __name__ == "__main__":
        main()
