from django.db import models
from django.utils.translation import gettext_lazy as _


class Athlete(models.Model):
    athlete_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))
    personal_code = models.CharField(max_length=50, unique=True, verbose_name=_("Personal Code"), null=True, blank=True,)
    sex = models.CharField(max_length=10, verbose_name=_("Sex"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
