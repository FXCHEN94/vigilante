from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

#from otree_tools.models.fields import OtherModelField

import random
import itertools

author = 'FX CHEN'

doc = """
This is a TPPG with leader not punishing.
"""


class Constants(BaseConstants):
    name_in_url = 'vigilante'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'karl/aInstructions.html'

    endowment = c(100)
    initial_endowment = c(100)
    take_away_endo = c(50)
    pool_multiplier = c(1.6)
    answer_increment = c(1)

    leader_decision = currency_range(0, take_away_endo, answer_increment)
    leader_decision_count = len(leader_decision)



class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        self.group_randomly()


class Group(BaseGroup):

    total_removed = models.CurrencyField()

    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    decision_member1 = models.CurrencyField(choices=Constants.leader_decision,
                                            label='')
    decision_member2 = models.CurrencyField(choices=Constants.leader_decision,
                                            label='')
    decision_member3 = models.CurrencyField(choices=Constants.leader_decision,
                                            label='')

    current_payoff = models.CurrencyField()

    p1_current = models.CurrencyField()
    p2_current = models.CurrencyField()
    p3_current = models.CurrencyField()

    p1_payoff2 = models.CurrencyField()
    p2_payoff2 = models.CurrencyField()
    p3_payoff2 = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()]) + 68
        self.individual_share = self.total_contribution * Constants.pool_multiplier / 4
        self.total_removed = self.decision_member3 + self.decision_member1 + self.decision_member2
        for p in self.get_players():
            p.payoff2 = Constants.endowment - p.contribution + self.individual_share
            if self.subsession.round_number == 1:
                p.p1_payoff2 = sum([+80, -5,
                                     -self.decision_member1,
                                     +self.individual_share,
                                     ])
                p.p2_payoff2 = sum([+85, -11,
                                     -self.decision_member2,
                                     +self.individual_share,
                                     ])
                p.p3_payoff2 = sum([+67, -2,
                                     -self.decision_member3,
                                     +self.individual_share,
                                     ])
                p.payoff = Constants.endowment - p.contribution + self.individual_share - self.decision_member1 - self.decision_member2 - self.decision_member3 - 6
                p.current_payoff = Constants.endowment - p.contribution + self.individual_share
                p.participant.vars['earning1'] = p.payoff2


    def current(self):
        self.total_contribution= sum([p.contribution for p in self.get_players()]) + 68
        self.individual_share = self.total_contribution * Constants.pool_multiplier / 4
        self.p1_current = sum([+80,+self.individual_share, -5])
        self.p2_current = sum([+85,+self.individual_share, -11])
        self.p3_current = sum([+67,+self.individual_share, -2])
        self.current_payoff = sum([p.contribution for p in self.get_players()]) + self.individual_share
        for p in self.get_players():
            p.payoff2 = Constants.endowment - p.contribution + self.individual_share - 6
            p.payoff = Constants.endowment - p.contribution + self.individual_share
            p.participant.vars['earning1'] = p.payoff2
            p.payoff = Constants.endowment - p.contribution + self.individual_share
            p.participant.vars['earning2'] = p.payoff2


class Player(BasePlayer):
    total_removed = models.CurrencyField()

    pointremoved = models.CurrencyField()

    current_payoff = models.CurrencyField()


    payoff2 = models.CurrencyField()

    p1_payoff2 = models.CurrencyField()
    p2_payoff2 = models.CurrencyField()
    p3_payoff2 = models.CurrencyField()

    p1_current = models.CurrencyField()
    p2_current = models.CurrencyField()
    p3_current = models.CurrencyField()

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    def member_id(self):
        # player 1 is the leader, so member 1 is actually player 2
        return (self.id_in_group)






