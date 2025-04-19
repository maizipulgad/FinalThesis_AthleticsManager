from django.db import models
from .person import Person
from .person_role import PersonRole
from .stadium import Stadium
from .competition import Competition
from .competition_event import CompetitionEvent
from .collective import Collective
from django.utils.translation import gettext_lazy as _


class Relation(models.Model):
    relation_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_("Person"))
    person_role = models.ForeignKey(PersonRole, on_delete=models.CASCADE, verbose_name=_("Person Role"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Stadium"))
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Competition"))
    competition_event = models.ForeignKey(CompetitionEvent, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Competition Event"))
    collective = models.ForeignKey(Collective, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Collective"))
    created_at_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    valid_until_dt = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid Until"))

    def __str__(self):
        return f"{self.person} - {self.person_role}"
