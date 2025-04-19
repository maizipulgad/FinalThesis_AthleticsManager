from django.db import models
from .competition_event_competition_athlete import CompetitionEventCompetitionAthlete
from .round import Round
from django.utils.translation import gettext_lazy as _


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    competition_event_competition_athlete = models.ForeignKey(CompetitionEventCompetitionAthlete, on_delete=models.CASCADE, related_name="results", verbose_name=_("Competition Event Competition Athlete"))
    result_as_number = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name=_("Result as Number"))
    round = models.ForeignKey(Round, on_delete=models.CASCADE, verbose_name=_("Round"))
    lane_or_order_number = models.IntegerField(null=True, blank=True, verbose_name=_("Lane or Order Number"))
    wind_as_number = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Wind as Number"))
    attempt_nr = models.IntegerField(null=True, blank=True, verbose_name=_("Attempt Number"))
    starting_height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Starting Height"))
    points_from_result = models.IntegerField(null=True, blank=True, verbose_name=_("Points from Result"))
    result_as_char = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Result as Character"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    class Meta:
        unique_together = ('competition_event_competition_athlete', 'round', 'attempt_nr')

    def __str__(self):
        return f"Result {self.result_as_number} for {self.competition_event_competition_athlete}"
