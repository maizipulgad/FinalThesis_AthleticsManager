from django.db import models
from .competition_event import CompetitionEvent
from .competition_athlete import CompetitionAthlete
from django.utils.translation import gettext_lazy as _


class CompetitionEventCompetitionAthlete(models.Model):
    competition_event_competition_athlete_id = models.AutoField(primary_key=True)
    competition_event = models.ForeignKey(CompetitionEvent, on_delete=models.CASCADE, verbose_name=_("Competition Event"))
    competition_athlete = models.ForeignKey(CompetitionAthlete, on_delete=models.CASCADE, verbose_name=_("Competition Athlete"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    class Meta:
        unique_together = ["competition_event", "competition_athlete"]  # Prevent duplicates

    def __str__(self):
        return f"{self.competition_athlete} in {self.competition_event}"

