from django.db import models
from django.utils.translation import gettext_lazy as _


class PersonRole(models.Model):
    person_role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Person Role Name"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name