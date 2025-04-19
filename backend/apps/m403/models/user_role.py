from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("User Role Name"))
    upper_user_role_id = models.IntegerField(null=True, blank=True, verbose_name=_("Upper User Role ID"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return self.name