# SPDX-License-Identifier: 0BSD
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.smithereens import *

DESCRIPTION = "Dummy app"
LANDING_PAGE = False


def new_player(player: PlayerType) -> None:
    player.e2mupay_amount = 17.42  # Final payment in real currency


page_order: list[Any] = []
