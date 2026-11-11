# While this software is FLOSS, making changes is not recommended unless you are a
# lab manager or similar. Ordinary experimenters should merely put e2mupay_start and
# e2mupay_end into their oTree projects and call it a day.
# More information: https://github.com/mrpg/e2mupay

import os
import shutil
import tarfile
import zoneinfo
from datetime import datetime, timezone

from otree.api import *

doc = """
E²MU Payment App (start)
"""


def init():
    target = "_static/e2mupay"  # DO NOT CHANGE THIS
    package = "e2mupay_start/e2mupay_static.tgz"
    files_to_check = [
        "DO_NOT_MESS_WITH_THIS_DIRECTORY.txt",
        ".gitignore",
        "key.js",
        "LICENSE",
        "openpgp.min.js",
    ]

    with tarfile.open(package, "r:*") as tar:
        # Refresh stale keys and library files when the bundled archive changes.
        for filename in files_to_check:
            path = f"{target}/{filename}"
            if not os.path.isfile(path):
                break
            member = f"e2mupay/{filename}"
            with open(path, "rb") as current, tar.extractfile(member) as bundled:
                if current.read() != bundled.read():
                    break
        else:
            return

        if os.path.exists(target):
            shutil.rmtree(target)

        tar.extractall("_static")


class C(BaseConstants):
    NAME_IN_URL = "e2mupay_start"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Hello(Page):
    @staticmethod
    def is_displayed(player):
        dt_local = datetime.now(zoneinfo.ZoneInfo("Australia/Melbourne"))
        player.participant.vars["e2mupay_start"] = dt_local.isoformat()

        return False


page_sequence = [
    Hello,
]

init()
