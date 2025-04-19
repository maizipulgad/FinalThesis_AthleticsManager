from django.db import models
from .competition_event import CompetitionEvent
from django.utils.translation import gettext_lazy as _


class Round(models.Model):
    round_id = models.AutoField(primary_key=True)
    round_number = models.IntegerField(verbose_name=_("Round Number"))
    competition_event = models.ForeignKey(CompetitionEvent, on_delete=models.CASCADE, related_name="rounds", verbose_name=_("Competition Event"))
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_("End Time"))
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name=_("Round Name"))
    printout = models.BinaryField(null=True, blank=True, verbose_name=_("Printout"))
    upper_round_id = models.IntegerField(null=True, blank=True, verbose_name=_("Upper Round ID"))
    number_of_sub_rounds = models.IntegerField(null=True, blank=True, verbose_name=_("Number of Sub-Rounds"))
    number_of_max_athletes = models.IntegerField(null=True, blank=True, verbose_name=_("Number of Max Athletes"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"Round {self.round_number} for {self.competition_event}"
