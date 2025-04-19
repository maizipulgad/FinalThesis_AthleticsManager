from django.db import models
from django.utils.translation import gettext_lazy as _


class AgeClass(models.Model):
    age_class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Age Class Name"))
    minimum_age = models.IntegerField(verbose_name=_("Minimum Age"), null=True, blank=True)
    maximum_age = models.IntegerField(verbose_name=_("Maximum Age"), null=True, blank=True)
    sex = models.CharField(max_length=10, verbose_name=_("Sex"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name
