from django.db import models
from .round import Round
from django.utils.translation import gettext_lazy as _


class JumpHeight(models.Model):
    jump_height_id = models.AutoField(primary_key=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="heights")
    height = models.DecimalField(max_digits=4, decimal_places=2)
    order = models.PositiveIntegerField()
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.round} - {self.height}, order: {self.order}"