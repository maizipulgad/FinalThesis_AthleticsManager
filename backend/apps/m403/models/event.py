from django.db import models
from django.utils.translation import gettext_lazy as _

from .event_type import EventType


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Event Name"))
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name=_("Event Type"))
    comb_event_var_a = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Combination Variable A"))
    comb_event_var_b = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Combination Variable B"))
    comb_event_var_c = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Combination Variable C"))
    upper_event_id = models.IntegerField(null=True, blank=True, verbose_name=_("Upper Event ID"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name
