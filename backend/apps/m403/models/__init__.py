# models/__init__.py
from .athlete import Athlete
from .country import Country
from .athlete_citizenship import AthleteCitizenship
from .collective import Collective
from .athlete_collective import AthleteCollective
from .collective_country import CollectiveCountry
from .stadium import Stadium
from .competition import Competition
from .competition_on_stadium import CompetitionOnStadium
from .event import Event
from .event_type import EventType
from .competition_event import CompetitionEvent
from .age_class import AgeClass
from .competition_athlete import CompetitionAthlete
from .competition_event_competition_athlete import CompetitionEventCompetitionAthlete
from .round import Round
from .result import Result
from .person import Person
from .relation import Relation
from .person_role import PersonRole
from .user_role import UserRole
from .user_user_role import UserUserRole
from .user_person import UserPerson
from .jump_height import JumpHeight

# Enabling translatable fields using gettext_lazy
from django.utils.translation import gettext_lazy as _