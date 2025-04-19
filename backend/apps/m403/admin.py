from django.contrib import admin
from .models import (
    Athlete, Country, AthleteCitizenship, Collective, AthleteCollective,
    CollectiveCountry, Stadium, Competition, CompetitionOnStadium, Event,
    EventType, CompetitionEvent, AgeClass, CompetitionAthlete,
    CompetitionEventCompetitionAthlete, Round, Result, Person, Relation,
    PersonRole, UserRole, UserUserRole, UserPerson
)
from .models.jump_height import JumpHeight

# Registering models
admin.site.register(Athlete)
admin.site.register(Country)
admin.site.register(AthleteCitizenship)
admin.site.register(Collective)
admin.site.register(AthleteCollective)
admin.site.register(CollectiveCountry)
admin.site.register(Stadium)
admin.site.register(Competition)
admin.site.register(CompetitionOnStadium)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(CompetitionEvent)
admin.site.register(AgeClass)
admin.site.register(CompetitionAthlete)
admin.site.register(CompetitionEventCompetitionAthlete)
admin.site.register(Round)
admin.site.register(Result)
admin.site.register(Person)
admin.site.register(Relation)
admin.site.register(PersonRole)
admin.site.register(UserRole)
admin.site.register(UserUserRole)
admin.site.register(UserPerson)
admin.site.register(JumpHeight)
