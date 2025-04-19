from django.db import models
from django.contrib.auth.models import User
from .user_role import UserRole
from django.utils.translation import gettext_lazy as _


class UserUserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name=_("User Role"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.user} - {self.user_role}"
