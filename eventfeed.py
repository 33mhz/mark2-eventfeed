from twisted.internet import protocol, reactor, defer

from mk2.plugins import Plugin
from mk2.events import PlayerChat, PlayerJoin, PlayerQuit, PlayerDeath, ServerStopped, ServerStarted

class EventFeed(Plugin):
    script_cmd = Plugin.Property(required=True)
    shell = Plugin.Property(default="/bin/sh")
    parsable_format = Plugin.Property(default=False)

    on_chat = Plugin.Property(default=True)
    on_join = Plugin.Property(default=True)
    on_quit = Plugin.Property(default=True)
    on_death = Plugin.Property(default=True)
    on_shutdown = Plugin.Property(default=True)
    on_restart = Plugin.Property(default=True)

    def setup(self):
        if self.on_restart:
            self.register(self.startup, ServerStarted)
        if self.on_shutdown:
            self.register(self.shutdown, ServerStopped)
        if self.on_join:
            self.register(self.join, PlayerJoin)
        if self.on_quit:
            self.register(self.quit, PlayerQuit)
        if self.on_chat:
            self.register(self.chat, PlayerChat)
        if self.on_death:
            self.register(self.death, PlayerDeath)
    
    def startup(self, event):
        if self.parsable_format:
            str = " 'startup'"
        else:
            str = " 'Server Started'"
        self.execute(self.script_cmd+str)

    def shutdown(self, event):
        if self.parsable_format:
            str = " 'shutdown'"
        else:
            str = " 'Server Shut Down'"
        self.execute(self.script_cmd+str)

    def join(self, event):
        if self.parsable_format:
            str = " 'join' '" + event.username + "'"
        else:
            str = " '" + event.username + " joined'"
        self.execute(self.script_cmd+str)

    def quit(self, event):
        if self.parsable_format:
            str = " 'quit' '" + event.username + "'"
        else:
            str = " '" + event.username + " left'"
        self.execute(self.script_cmd+str)
    
    def chat(self, event):
        if self.parsable_format:
            str = " 'chat' '" + event.username + "' '" + event.message.replace("'", "'\\''") + "'"
        else:
            str = " '" + event.username + ": '" + event.message.replace("'", "'\\''") + "'"
        self.execute(self.script_cmd+str)

    def death(self, event):
        if self.parsable_format:
            str = " 'death' '" + event.username + "' '" + event.killer + "' '" + event.weapon + "' '" + event.cause + "'"
        else:
            str = " '" + event.text + "'"
        self.execute(self.script_cmd+str)


    def execute(self, cmd):
        execute = defer.succeed(None)

        def execute_next(fn, *a, **kw):
            execute.addCallback(lambda r: fn(*a, **kw))
            execute.addErrback(lambda f: True)

        d = defer.Deferred()

        p = protocol.ProcessProtocol()
        p.outReceived = lambda d: [execute_next(self.execute_reduced, l, cmd) for l in d.split("\n")]
        p.processEnded = lambda r: d.callback(None)

        reactor.spawnProcess(p, self.shell, [self.shell, '-c', cmd])

        d.addCallback(lambda r: execute)
        return d
