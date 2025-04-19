from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Phone Number"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
