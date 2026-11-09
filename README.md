# FortBox private Discord controller

This bot supports `/myid`, `/mode`, `/search`, `/cancel`, and `/party`. **It does not control Fortnite or queue matches.**

## Setup
1. Create a Discord application at https://discord.com/developers/applications and create its bot.
2. Install it in your own server with `bot` and `applications.commands` scopes; no administrator permission needed.
3. Host this Python project with a persistent worker on a service supporting Python. Set `DISCORD_TOKEN` as a private environment secret. Start command: `python bot.py`.
4. Optionally set `GUILD_ID` to your server's numerical ID to register commands to that server quickly.
5. Initially set `OWNER_ID=0` so you can run `/myid`. **During this bootstrap phase other server members can use controller commands.** Use a private server without other members, or preferably obtain your ID first and set `OWNER_ID` before starting the bot.
6. Set `OWNER_ID` to the numerical ID reported by `/myid`, then restart. Only that user can run controller commands (other than `/myid`, which reveals only the caller's own ID).

Never share the bot token. Do not commit `.env` files. The in-memory mode and request state reset on restart.
