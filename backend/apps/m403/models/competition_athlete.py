from django.db import models
from .competition import Competition
from .athlete import Athlete
from .collective import Collective
from django.utils.translation import gettext_lazy as _


class CompetitionAthlete(models.Model):
    competition_athlete_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name=_("Competition"))
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, verbose_name=_("Athlete"))
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name=_("Collective"))
    BIB_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("BIB Number"))
    team_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Team Name"))
    upper_competition_athlete_id = models.IntegerField(null=True, blank=True,
                                                       verbose_name=_("Upper Competition Athlete ID"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    class Meta:
        unique_together = ["athlete", "competition"]

    def __str__(self):
        return f"{self.athlete} in {self.competition}"
