from django.db import models

from .age_class import AgeClass
from .competition import Competition
from .event import Event
from django.utils.translation import gettext_lazy as _


class CompetitionEvent(models.Model):
    competition_event_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name=_("Competition"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("Event"))
    age_class = models.ForeignKey(AgeClass, on_delete=models.CASCADE, verbose_name=_("Age Class"))
    number_of_attempts = models.IntegerField(default=1, verbose_name=_("Number of Attempts"))
    regrouping = models.BooleanField(default=False, verbose_name=_("Regrouping After Attempts"))
    regrouping_done = models.BooleanField(default=False,  verbose_name=_("Regrouping Done?"))
    finalists_attempt_count = models.IntegerField(default=3, verbose_name=_("Attempts for Finalists"))
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    wind_measurement = models.BooleanField(default=False, verbose_name=_("Wind Measurement"))
    printout = models.BinaryField(null=True, blank=True, verbose_name=_("Printout"))
    number_of_rounds = models.IntegerField(null=True, blank=True, verbose_name=_("Number of Rounds"))
    athlete_max_count = models.IntegerField(null=True, blank=True, verbose_name=_("Athlete Max Count"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.competition} - {self.event}"
