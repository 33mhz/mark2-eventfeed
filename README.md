# mark2-eventfeed
A simple event plugin for the [Mark2](https://github.com/gsand/mark2) Minecraft wrapper.


This plugin simply listens for the common hooks in Mark2 and executes your own script with the events.


## Installation

1) Place the `eventfeed.py` file in your Mark2 plugins folder (default: /usr/mark2/mk2/plugins).

2) Edit your `mark2.properties` file to activate the plugin and configure it. Look at the example configuration for ideas:


## Example Configuration (default options)

You may omit any of these options if you like their default setting.
The `script_cmd` can be any shell/bash script, Python, PHP, Rust--whatever you like.

```
plugin.eventfeed.enabled=true # REQUIRED
plugin.eventfeed.script_cmd=python /home/user/parseTheEvents.py # REQUIRED
plugin.eventfeed.shell="/bin/sh"
plugin.eventfeed.parsable_format=false
plugin.eventfeed.on_chat=true
plugin.eventfeed.on_join=true
plugin.eventfeed.on_quit=true
plugin.eventfeed.on_death=true
plugin.eventfeed.on_shutdown=true
plugin.eventfeed.on_restart=true
```

## Parsing

These are examples of what is output to your `script_cmd` program/file.

|event|`parsable_format` output|default output|
|---|---|---|
|player chat|`'chat' '33mhz' 'hello darkness, my old friend.'`|`'33mhz: hello darkness, my old friend.'`|
|player join|`'join' '33mhz'`|`'33mhz joined'`|
|player quit|`'quit' '33mhz'`|`'33mhz quit'`|
|player death|`'death' '33mhz' 'killer' 'weapon' 'cause'`|`'33mhz thought he could fly.'`|
|server shutdown|`'shutdown'`|`'Server Shut Down'`|
|server restart|`'startup'`|`'Server Started'`|
