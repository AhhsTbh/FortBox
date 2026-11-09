"""Epic account client shared by bot.py (Discord) and epic_bot.py (standalone).

Uses the unofficial `rebootpy` library (against Epic's terms; use a throwaway account).
Only the owner's friend requests / party invites are accepted.
"""
import json
import os

import rebootpy

OWNER_EPIC_NAME = os.environ.get('OWNER_EPIC_NAME', '').strip().lower()
AUTH_FILE = os.environ.get('DEVICE_AUTH_FILE', 'device_auths.json')

# UNVERIFIED defaults: override with env vars once you confirm the real IDs
# (e.g. from fortnite-api.com /v1/playlists). Wrong IDs just fail to apply.
PLAYLISTS = {
    'Battle Royale': os.environ.get('PLAYLIST_BR', 'Playlist_DefaultSquad'),
    'Zero Build': os.environ.get('PLAYLIST_ZB', 'Playlist_NoBuild_Squad'),
    'Reload': os.environ.get('PLAYLIST_RELOAD', 'Playlist_Respawn_24_Squad'),
}


def is_owner(name) -> bool:
    return bool(name) and bool(OWNER_EPIC_NAME) and name.strip().lower() == OWNER_EPIC_NAME


def load_auth() -> dict:
    if os.path.isfile(AUTH_FILE):
        with open(AUTH_FILE) as fp:
            return json.load(fp)
    return {}


class FortBoxClient(rebootpy.Client):
    def __init__(self):
        super().__init__(auth=rebootpy.AdvancedAuth(prompt_device_code=True, **load_auth()))

    async def event_device_auth_generate(self, details, email=None):
        with open(AUTH_FILE, 'w') as fp:
            json.dump(details, fp)
        print('Device auth saved.')

    async def event_ready(self):
        print(f'Epic bot ready as {self.user.display_name}. Add this account as a friend.')

    async def event_friend_request(self, request):
        if is_owner(request.display_name):
            await request.accept()
            print(f'Accepted friend request from {request.display_name}')
        else:
            await request.decline()

    async def event_party_invite(self, invitation):
        if is_owner(invitation.sender.display_name):
            await invitation.accept()
            print(f'Joined party of {invitation.sender.display_name}')
        else:
            await invitation.decline()

    # --- helpers used by Discord commands ---
    def party_summary(self) -> str:
        party = getattr(self, 'party', None)
        if not party:
            return 'Epic bot is not in a party.'
        leader = getattr(party, 'leader', None)
        names = []
        for m in party.members:
            crown = '👑 ' if leader and m.id == leader.id else ''
            names.append(f'{crown}{m.display_name}')
        return 'Party: ' + ', '.join(names)

    async def apply_mode(self, mode: str) -> str:
        party = getattr(self, 'party', None)
        if not party:
            return 'Epic bot is not in a party, so the playlist was not changed.'
        try:
            await party.set_playlist(playlist=PLAYLISTS[mode])
            return f'Party playlist set to {mode}.'
        except Exception as e:  # not leader, bad ID, etc.
            return f'Could not set playlist ({type(e).__name__}); bot may not be party leader or the ID is wrong.'
