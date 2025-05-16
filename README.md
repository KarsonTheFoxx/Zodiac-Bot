# Zodiac Bot
A simple Discord bot for 2Known and the Zodiac community written in Python using [Disnake](https://pypi.org/project/disnake/)

## TODO
- Create pubbubhubdub server (WebSub, I think the other name is funnier)
- Finish moderation commands
- Rewrite hardcoded sections to utilize a database to make the bot extendable + customizable
- Rewrite views to use low level components to allow cross-reboot usability
- (Maybe) Create RCON server extension for Minecraft Java
- Create documentation/instruction manual
- Create bot TOS and Privacy Policy (Currently no data is saved, and no commands require TOS)
## ISSUES
- Ticket embed will break between bot reboots/reconnects (Limitation of using views)

## VERSION
### V0.1.0
Changelog
- Added main.py
> Bot's core
- Added moderation.py
> Will contain any command that checks permission; I.e Ban, kick, ETC
- Added tickets.py
> A basic ticket system that uses a web of callbacks to function; QUICKREF: slash_command > newTicketEmbedModal > createTicketView > createTicketModal > closeTicketView

Notes
More features planned soonish. Depends on when I have time to write code for new features

### V0.1.1
Changelog
- Fixed typo in README.md
> Changed "WebServer" to "WebSub" in the TODO list

### V0.1.2
Changelog
- Fixed issue with extensions/tickets.py
> Hardcoded category_channel caused issues. Added permission changes to ticket
### V0.1.3
Changelog
- Updated changelog
> Changelog in last push was not updated
- Added moderator_role ping to the message sent to the ticket