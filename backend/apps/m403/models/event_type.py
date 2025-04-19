from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Event Type Name"))
    upper_event_type_id = models.IntegerField(null=True, blank=True, verbose_name=_("Upper Event Type ID"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name

