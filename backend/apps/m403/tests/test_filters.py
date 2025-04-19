from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime, date
from apps.m403.models import (
    Competition, Athlete, Event, CompetitionEvent,
    CompetitionAthlete, CompetitionEventCompetitionAthlete,
    Round, Result, EventType, AgeClass
)
from apps.m403.filters import ResultFilter, CompetitionAthleteFilter, CompetitionEventFilter


class TestResultFilter(TestCase):
    def setUp(self):
        self.comp = Competition.objects.create(name="Test Comp", start_time="2025-01-01T10:00Z", end_time="2025-01-01T17:00Z")
        self.event_type = EventType.objects.create(name="RUNNING")
        self.age_class = AgeClass.objects.create(name="MU20", sex="M")
        self.event = Event.objects.create(name="100m", event_type=self.event_type)
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event, age_class=self.age_class, start_time="2025-01-01T10:00Z")
        self.athlete = Athlete.objects.create(first_name="A", last_name="B", sex="M", date_of_birth=date(2003, 1, 2))
        self.comp_athlete = CompetitionAthlete.objects.create(competition=self.comp, athlete=self.athlete, BIB_number=101)
        self.assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=self.comp_event, competition_athlete=self.comp_athlete)
        self.round = Round.objects.create(competition_event=self.comp_event, round_number=1, start_time=make_aware(datetime(2025, 1, 1, 12)))
        self.result = Result.objects.create(competition_event_competition_athlete=self.assignment, round=self.round, result_as_number=12.34)

    def test_result_filter_by_round(self):
        qs = Result.objects.all()
        f = ResultFilter({"round": self.round.round_id}, queryset=qs)
        self.assertEqual(len(f.qs), 1)

    def test_result_filter_by_competition_event(self):
        qs = Result.objects.all()
        f = ResultFilter({"competition_event": self.comp_event.competition_event_id}, queryset=qs)
        self.assertEqual(len(f.qs), 1)


class TestCompetitionAthleteFilter(TestCase):
    def setUp(self):
        self.comp = Competition.objects.create(name="Test", start_time="2025-01-01T09:00Z", end_time="2025-01-01T17:00Z")
        self.event_type = EventType.objects.create(name="JUMP")
        self.age_class = AgeClass.objects.create(name="MU20", sex="M")
        self.athlete = Athlete.objects.create(first_name="T", last_name="Tester", sex="F", date_of_birth=date(2003, 1, 2))
        self.comp_athlete = CompetitionAthlete.objects.create(competition=self.comp, athlete=self.athlete, BIB_number=999)
        self.event = Event.objects.create(name="High Jump", event_type=self.event_type)
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event, start_time="2025-01-01T09:00Z", age_class=self.age_class)
        self.assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=self.comp_event, competition_athlete=self.comp_athlete)

    def test_filter_by_competition_id(self):
        qs = CompetitionAthlete.objects.all()
        f = CompetitionAthleteFilter({"competition_id": self.comp.pk}, queryset=qs)
        self.assertEqual(len(f.qs), 1)

    def test_filter_by_competition_event_id(self):
        qs = CompetitionAthlete.objects.all()
        f = CompetitionAthleteFilter({"competition_event_id": self.comp_event.pk}, queryset=qs)
        self.assertEqual(len(f.qs), 1)


class TestCompetitionEventFilter(TestCase):
    def setUp(self):
        self.comp = Competition.objects.create(name="My Meet", start_time="2025-04-01T08:00Z", end_time="2025-04-01T16:00Z")
        self.event_type = EventType.objects.create(name="JUMP")
        self.age_class = AgeClass.objects.create(name="TU18", sex="N")
        self.event = Event.objects.create(name="Long Jump", event_type=self.event_type)
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event, start_time="2025-04-01T08:00Z", age_class=self.age_class)

    def test_filter_by_competition_id(self):
        qs = CompetitionEvent.objects.all()
        f = CompetitionEventFilter({"competition_id": self.comp.pk}, queryset=qs)
        self.assertEqual(len(f.qs), 1)
