"""Run the Epic account bot on its own (without Discord)."""
import sys

from epic_client import OWNER_EPIC_NAME, FortBoxClient

if not OWNER_EPIC_NAME:
    sys.exit('Set OWNER_EPIC_NAME to your Epic display name.')

if __name__ == '__main__':
    FortBoxClient().run()
