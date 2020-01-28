from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class aIntroduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class vigilante(Page):

    pass


class aContribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']


class bPleaseproceed(Page):
    timeout_seconds = 45

class cResults(Page):
    def vars_for_template(self):
        return self.group.current()

class dLeaderDecision(Page):
    def vars_for_template(self):
        return {
            'current':self.group.current_payoff,
        }

    form_model = models.Group
    form_fields = ['decision_member1', 'decision_member2', 'decision_member3']

    def error_message(self, values):
        if values["decision_member1"] + values["decision_member2"] + values["decision_member3"] > self.player.payoff2:
            return 'The total number of points you remove exceeds what you currently have.'


class eResults2(Page):
    def vars_for_template(self):
        return self.group.set_payoffs()


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.current()

class SimpleWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.current()

    body_text = "Waiting for other group members."


    pass

class SimpleWaitPage2(WaitPage):
    def after_all_players_arrive(self):
        self.group.current()

    body_text = "Waiting for other group members."


    pass


page_sequence = [
    aIntroduction,
    aContribute,
    bPleaseproceed,
    SimpleWaitPage,
    cResults,
    SimpleWaitPage2,
    vigilante,
    dLeaderDecision,
    eResults2,

]
