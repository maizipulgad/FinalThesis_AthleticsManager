from django.db import models
from .collective import Collective
from .country import Country
from django.utils.translation import gettext_lazy as _


class CollectiveCountry(models.Model):
    collective_country_id = models.AutoField(primary_key=True)
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE, verbose_name=_("Collective"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.collective} - {self.country}"
