from django.db import models
from .stadium import Stadium
from .competition import Competition
from django.utils.translation import gettext_lazy as _


class CompetitionOnStadium(models.Model):
    competition_on_stadium_id = models.AutoField(primary_key=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, verbose_name=_("Stadium"))
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name=_("Competition"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.competition} at {self.stadium}"

