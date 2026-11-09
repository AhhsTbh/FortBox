"""FortBox Epic account bot (separate process from bot.py).

Logs into ONE Epic account (use a throwaway, not your main) and:
  - auto-accepts friend requests ONLY from OWNER_EPIC_NAME
  - auto-accepts party invites ONLY from that same friend

It cannot start matchmaking: Fortnite exposes no API for queueing; the party
leader does that in the game client. Uses the unofficial `rebootpy` library,
which Epic's terms of service do not allow, so the account may be banned.
"""
import json
import os

import rebootpy

OWNER_EPIC_NAME = os.environ.get('OWNER_EPIC_NAME', '').strip().lower()
AUTH_FILE = os.environ.get('DEVICE_AUTH_FILE', 'device_auths.json')

if not OWNER_EPIC_NAME:
    raise SystemExit('Set OWNER_EPIC_NAME to your Epic display name.')


def is_owner(name) -> bool:
    return bool(name) and name.strip().lower() == OWNER_EPIC_NAME


def load_auth() -> dict:
    if os.path.isfile(AUTH_FILE):
        with open(AUTH_FILE) as fp:
            return json.load(fp)
    return {}


class FortBoxClient(rebootpy.Client):
    def __init__(self):
        super().__init__(
            auth=rebootpy.AdvancedAuth(prompt_device_code=True, **load_auth())
        )

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
            print(f'Declined friend request from {request.display_name}')

    async def event_party_invite(self, invitation):
        if is_owner(invitation.sender.display_name):
            await invitation.accept()
            print(f'Joined party of {invitation.sender.display_name}')
        else:
            await invitation.decline()


if __name__ == '__main__':
    FortBoxClient().run()
