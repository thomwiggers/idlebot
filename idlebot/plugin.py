from irc3.plugins.command import command
import irc3

@irc3.plugin
class IdlePlugin(object):
    """
    Idle plugin
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log
        self.config = bot.config.get(__name__, {})
        self.idlebot_nick = self.config.get('idlebot_nick', 'IdleBot')
        self.login_command = self.config.get('login_command', 
                'LOGIN {nick} {password}')
        self.idle_name = self.config.get('character_name', 'DutchIdle')
        self.idle_password = self.config.get('idle_password')
        self.idle_channel = "#" + self.config.get('channel', 'irpg-idle')
        self.identified = False


    @irc3.event(irc3.rfc.JOIN)
    def login_bot_on_join(self, mask, channel):
        if channel[1:] == self.idle_channel and not self.identified:
            self._log_in_idlebot()
        if mask.nick == self.idlebot_nick:
            self._log_in_idlebot()

    @command
    def login(self, mask, target, args):
        """Login with Idlebot

            %%login
        """
        self._log_in_idlebot()

    def _log_in_idlebot(self):
        self.bot.log.info("Sending login command to {}".format(self.idlebot_nick))
        self.bot.privmsg(self.idlebot_nick, 
                self.login_command.format(nick=self.idle_name,
                    password=self.idle_password))
        self.identified = True

    def connection_made(self):
        self.identified = False


@irc3.event(r':(?P<ns>NickServ)!services@what-network.net? NOTICE (?P<nick>.*?) :'
            r'This nickname is registered.*')
def register(bot, ns=None, nick=None):
    bot.log.info("Logging in with NickServ")
    try:
        password = bot.config[bot.config.host][nick]
    except KeyError:
        pass
    else:
        bot.privmsg(ns, 'identify {passw}'.format(passw=password))
