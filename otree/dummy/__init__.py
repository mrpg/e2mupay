from otree.api import *

doc = """
Dummy app
"""


class C(BaseConstants):
    NAME_IN_URL = "dummy"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.vars["e2mupay_amount"] = cu(17.42)


page_sequence = []
