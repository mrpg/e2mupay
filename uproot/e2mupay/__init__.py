# While this software is FLOSS, making changes is not recommended unless you are a
# lab manager or similar. Ordinary experimenters should merely put e2mupay into their
# uproot projects (as the LAST app) and call it a day.
# More information: https://github.com/mrpg/e2mupay
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt
# - OpenPGP.js: LGPL v3+, see _static/LICENSE

import secrets
import string
import zoneinfo
from datetime import datetime

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "E²MU Payment App"
LANDING_PAGE = False


class C:
    TIMEZONE = "Australia/Melbourne"
    TIMEOUT_SECONDS = 60 * 60
    CODE_ALPHABET = string.ascii_uppercase + string.digits
    CODE_LENGTH = 9


def now() -> str:
    return datetime.now(zoneinfo.ZoneInfo(C.TIMEZONE)).isoformat()


def code_display(player: PlayerType) -> str:
    code = player.e2mupay_code

    return "-".join(code[i : i + 3] for i in range(0, len(code), 3))


def new_player(player: PlayerType) -> None:
    # Runs when the player is initialized, i.e., normally when they start the study
    player.e2mupay_start = now()
    player.e2mupay_code = "".join(
        secrets.choice(C.CODE_ALPHABET) for _ in range(C.CODE_LENGTH)
    )
    player.e2mupay_pay_to = None


class PaymentData(Page):
    # Only the ciphertext is ever sent to the server. The contact inputs on this page
    # have no name attribute, so the browser never submits their plaintext.
    fields = dict(e2mupay_pay_to=StringField())
    timeout = C.TIMEOUT_SECONDS

    @classmethod
    def before_once(page, player: PlayerType) -> None:
        player.e2mupay_end = now()

    @classmethod
    def validate(page, player: PlayerType, data: dict[str, Any]) -> str | None:
        if not data["e2mupay_pay_to"].startswith("-----BEGIN PGP MESSAGE-----|"):
            return "Your contact data could not be encrypted. Please try again."

        return None

    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        return dict(
            amount_display=f"{player.e2mupay_amount:.2f}",
            code_display=code_display(player),
        )

    @classmethod
    def jsvars(page, player: PlayerType) -> dict[str, Any]:
        return dict(
            e2mupay_metadata=dict(
                session_code=player.session.name,
                participant_code=player.name,
                payment_code=player.e2mupay_code,
                amount=str(player.e2mupay_amount),
            ),
        )


class Results(Page):
    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        return dict(code_display=code_display(player))


page_order = [
    PaymentData,
    Results,
]
