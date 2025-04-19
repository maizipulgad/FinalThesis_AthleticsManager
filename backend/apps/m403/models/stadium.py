from django.db import models
from django.utils.translation import gettext_lazy as _


class Stadium(models.Model):
    stadium_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Stadium Name"))
    location = models.CharField(max_length=200, verbose_name=_("Location"))
    number_of_lanes = models.IntegerField(verbose_name=_("Number of Lanes"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name
