# While this software is FLOSS, making changes is not recommended unless you are a
# lab manager or similar. Ordinary experimenters should merely put e2mupay_start and
# e2mupay_end into their oTree projects and call it a day.
# More information: https://github.com/mrpg/e2mupay

import logging
import random
import string
import textwrap
import zoneinfo
from datetime import datetime, timezone

from otree.api import *

doc = """
E²MU Payment App 2
"""

__version__ = "3.0.0"


class C(BaseConstants):
    NAME_IN_URL = "e2mupay_end"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    code = models.StringField(initial="")
    start_ = models.StringField(initial="")
    end_ = models.StringField(initial="")
    amount = models.CurrencyField()
    pay_to = models.LongStringField(blank=True)


def creating_session(subsession):
    for player in subsession.get_players():
        player.code = "".join(random.choices(string.ascii_uppercase + string.digits, k=9))


# PAGES
class PaymentData(Page):
    form_fields = ["pay_to"]
    form_model = "player"
    timeout_seconds = 60 * 60

    @staticmethod
    def is_displayed(player):
        dt_local = datetime.now(zoneinfo.ZoneInfo("Australia/Melbourne"))
        player.participant.vars["e2mupay_end"] = dt_local.isoformat()
        player.amount = player.participant.vars["e2mupay_amount"]
        player.start_ = player.participant.vars["e2mupay_start"]
        player.end_ = player.participant.vars["e2mupay_end"]

        return True

    @staticmethod
    def vars_for_template(player):
        return dict(code_display="-".join(textwrap.wrap(player.code, 3)))


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(code_display="-".join(textwrap.wrap(player.code, 3)))


page_sequence = [
    PaymentData,
    Results,
]
