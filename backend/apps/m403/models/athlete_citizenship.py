from django.db import models
from .athlete import Athlete
from .country import Country
from django.utils.translation import gettext_lazy as _


class AthleteCitizenship(models.Model):
    athlete_nationality_id = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, verbose_name=_("Athlete"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.athlete} - {self.country}"
