# FortBox V2 — Private Discord controller

A deployable, owner-locked Discord control panel for a proposed three-account Fortnite squad. **No Fortnite accounts are connected and no actual Fortnite matchmaking occurs.** The bot deliberately reports this accurately.

## What works
- `/panel`: persistent Search, Cancel, Party buttons (private ephemeral panel)
- `/mode`: Battle Royale / Zero Build / Reload controller setting
- `/search`, `/cancel`, `/party`, `/myid`
- Server and user ID authorization; no open-access bootstrap mode
- Railway worker deployment

## Deploy on Railway (iPhone friendly)
1. Upload the *contents* of this folder to the root of your private GitHub repository. Replace old files `bot.py`, `requirements.txt`, `README.md`, `.env.example`, `.gitignore`; remove old `epic_client.py` and `epic_bot.py` if not using them. Do not upload a real `.env` or tokens.
2. In Discord, enable Developer Mode; copy your own User ID and the SLAM Society Server ID. Both are numeric.
3. In Discord Developer Portal > Bot, reset/copy the bot token **privately**. Never paste it into chat or GitHub.
4. Railway > New Project > Deploy from GitHub repo > select `FortBox`.
5. Railway > Variables: add `DISCORD_TOKEN`, `OWNER_ID`, `GUILD_ID` with the correct values. Do not include quotes. Railway should use `python bot.py` as start command (also specified in `railway.json`).
6. Deploy, inspect logs for `FortBox V2 online`. In SLAM Society use `/panel`.

If slash commands do not appear, confirm the application is installed with `applications.commands` and `bot` scopes, and that `GUILD_ID` is correct. Only the owner can use controller commands; `/myid` is available to everyone but reveals only the caller's own ID.

## Future game integration
Bot 1 leadership, Bot 2/3 authentication, party membership, and real queue actions require a separate compatible, permitted game integration. The Discord controller does not simulate success. Unofficial Fortnite automation can violate Epic's rules and put accounts at risk. Never store account secrets in GitHub or print them in logs.

## Known limitations
Mode and request state are in memory and reset on restart. The Discord buttons record requests only. No actual matchmaking, friend acceptance, party joining, or client automation is implemented.
