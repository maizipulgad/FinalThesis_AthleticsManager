from django.db import models
from django.utils.translation import gettext_lazy as _


class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Competition Name"))
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name