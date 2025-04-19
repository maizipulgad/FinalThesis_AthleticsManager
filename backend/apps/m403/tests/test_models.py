from datetime import date, datetime

from django.test import TestCase
from apps.m403.models import (AgeClass, Athlete, AthleteCitizenship, AthleteCollective, CollectiveCountry, Competition,
                              CompetitionEvent,
                              CompetitionEventCompetitionAthlete, CompetitionAthlete, Collective, Event, EventType,
                              Round, Result,
                              JumpHeight)
from django.utils.timezone import make_aware


class TestAgeClassModel(TestCase):
    def test_create_age_class(self):
        age_class = AgeClass.objects.create(
            name="M",
            minimum_age=14,
            maximum_age=17,
            sex="M"
        )
        self.assertEqual(age_class.name, "M")
        self.assertEqual(age_class.minimum_age, 14)

    def test_update_age_class(self):
        age_class = AgeClass.objects.create(name="M", minimum_age=18, maximum_age=34, sex="M")
        age_class.maximum_age = 35
        age_class.save()
        updated = AgeClass.objects.get(pk=age_class.pk)
        self.assertEqual(updated.maximum_age, 35)


class TestAthleteModel(TestCase):
    def test_create_athlete(self):
        athlete = Athlete.objects.create(first_name="Argo", last_name="Golberg", sex="M",
                                         date_of_birth=date(1999, 12, 31))
        self.assertEqual(athlete.first_name, "Argo")
        self.assertEqual(athlete.sex, "M")

    def test_update_athlete(self):
        athlete = Athlete.objects.create(first_name="Argo", last_name="Golberg", sex="M",
                                         date_of_birth=date(1999, 12, 31))
        athlete.last_name = "Updated"
        athlete.save()
        updated = Athlete.objects.get(pk=athlete.pk)
        self.assertEqual(updated.last_name, "Updated")


class TestCollectiveModel(TestCase):
    def test_create_collective(self):
        collective = Collective.objects.create(name="Audentese SK", abbreviation="AUDE")
        self.assertEqual(collective.name, "Audentese SK")

    def test_update_collective(self):
        collective = Collective.objects.create(name="Audentese SK", abbreviation="AUDE")
        collective.name = "TÜ ASK"
        collective.save()
        self.assertEqual(Collective.objects.get(pk=collective.pk).name, "TÜ ASK")


class TestCompetitionModel(TestCase):
    def test_create_competition(self):
        comp = Competition.objects.create(name="Winter Cup", start_time="2025-01-01T10:00Z",
                                          end_time="2025-01-01T18:00Z")
        self.assertEqual(comp.name, "Winter Cup")

    def test_update_competition(self):
        comp = Competition.objects.create(name="Winter Cup", start_time="2025-01-01T10:00Z",
                                          end_time="2025-01-01T18:00Z")
        comp.name = "Spring Cup"
        comp.save()
        self.assertEqual(Competition.objects.get(pk=comp.pk).name, "Spring Cup")


class TestCompetitionEventModel(TestCase):
    def test_create_event(self):
        comp = Competition.objects.create(name="Spring Cup", start_time="2025-05-01T09:00Z",
                                          end_time="2025-05-01T17:00Z")
        age_class = AgeClass.objects.create(name="MU23", sex="M")
        event_type = EventType.objects.create(name="RUNNING")
        event = Event.objects.create(name="100m", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, start_time="2025-02-01T12:00Z",
                                                     age_class=age_class)
        self.assertEqual(comp_event.event.name, "100m")

    def test_update_event_link(self):
        comp = Competition.objects.create(name="Spring Cup", start_time="2025-05-01T09:00Z",
                                          end_time="2025-05-01T17:00Z")
        age_class = AgeClass.objects.create(name="MU23", sex="M")
        event_type1 = EventType.objects.create(name="RUNNING")
        event_type2 = EventType.objects.create(name="JUMP")
        event1 = Event.objects.create(name="100m", event_type=event_type1)
        event2 = Event.objects.create(name="Long Jump", event_type=event_type2)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event1, start_time="2025-02-01T12:00Z",
                                                     age_class=age_class)
        comp_event.event = event2
        comp_event.save()
        self.assertEqual(CompetitionEvent.objects.get(pk=comp_event.pk).event.name, "Long Jump")


class TestCompetitionAthleteModel(TestCase):
    def test_create_competition_athlete(self):
        comp = Competition.objects.create(name="Test Comp", start_time="2025-02-01T12:00Z",
                                          end_time="2025-02-01T15:00Z")
        athlete = Athlete.objects.create(first_name="Jane", last_name="Doe", sex="F", date_of_birth=date(1995, 4, 12))
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number=23)
        self.assertEqual(comp_athlete.BIB_number, 23)

    def test_update_bib_number(self):
        comp = Competition.objects.create(name="Test Comp", start_time="2025-02-01T12:00Z",
                                          end_time="2025-02-01T15:00Z")
        athlete = Athlete.objects.create(first_name="Jane", last_name="Doe", sex="F", date_of_birth=date(1995, 4, 12))
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number='23')
        comp_athlete.BIB_number = '99'
        comp_athlete.save()
        self.assertEqual(CompetitionAthlete.objects.get(pk=comp_athlete.pk).BIB_number, '99')


class TestCompetitionEventCompetitionAthleteModel(TestCase):
    def test_create_assignment(self):
        comp = Competition.objects.create(name="Test Meet", start_time="2025-06-01T10:00Z",
                                          end_time="2025-06-01T18:00Z")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event_type = EventType.objects.create(name="THROW")
        event = Event.objects.create(name="Discus", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-06-01T10:00Z")
        athlete = Athlete.objects.create(first_name="Leo", last_name="Smith", sex="M", date_of_birth=date(2003, 1, 2))
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number=77)
        assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=comp_event,
                                                                       competition_athlete=comp_athlete)
        self.assertEqual(assignment.competition_athlete.BIB_number, 77)

    def test_update_assignment(self):
        comp = Competition.objects.create(name="Test Meet", start_time="2025-06-01T10:00Z",
                                          end_time="2025-06-01T18:00Z")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event_type1 = EventType.objects.create(name="THROW")
        event_type2 = EventType.objects.create(name="JUMP")
        event1 = Event.objects.create(name="Discus", event_type=event_type1)
        event2 = Event.objects.create(name="High Jump", event_type=event_type2)
        comp_event1 = CompetitionEvent.objects.create(competition=comp, event=event1, age_class=age_class,
                                                      start_time="2025-02-01T13:00Z")
        comp_event2 = CompetitionEvent.objects.create(competition=comp, event=event2, age_class=age_class,
                                                      start_time="2025-02-01T12:00Z", )
        athlete = Athlete.objects.create(first_name="Leo", last_name="Smith", sex="M", date_of_birth=date(2003, 1, 2))
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number=77)
        assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=comp_event1,
                                                                       competition_athlete=comp_athlete)
        assignment.competition_event = comp_event2
        assignment.save()
        self.assertEqual(CompetitionEventCompetitionAthlete.objects.get(pk=assignment.pk).competition_event.event.name,
                         "High Jump")


class TestEventModel(TestCase):
    def test_create_event(self):
        event_type = EventType.objects.create(name="POLE_VAULT")
        event = Event.objects.create(name="Pole Vault", event_type=event_type)
        self.assertEqual(event.name, "Pole Vault")

    def test_update_event(self):
        event_type = EventType.objects.create(name="JUMP")
        event = Event.objects.create(name="Pole Vault", event_type=event_type)
        event.name = "High Jump"
        event.save()
        self.assertEqual(Event.objects.get(pk=event.pk).name, "High Jump")


class TestJumpHeightModel(TestCase):
    def test_create_jump_height(self):
        comp = Competition.objects.create(name="Test Meet", start_time="2025-07-01T10:00Z",
                                          end_time="2025-07-01T12:00Z")
        event_type = EventType.objects.create(name="JUMP")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event = Event.objects.create(name="HJ", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-07-01T10:00Z")
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 7, 1, 10)))
        height = JumpHeight.objects.create(round=round_obj, height=1.21, order=1)
        self.assertAlmostEqual(height.height, 1.21)

    def test_update_jump_height(self):
        comp = Competition.objects.create(name="Test Meet", start_time="2025-07-01T10:00Z",
                                          end_time="2025-07-01T12:00Z")
        event_type = EventType.objects.create(name="JUMP")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event = Event.objects.create(name="HJ", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-07-01T10:00Z")
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 7, 1, 10)))
        height = JumpHeight.objects.create(round=round_obj, height=1.23, order=1)
        height.height = 1.37
        height.save()
        self.assertAlmostEqual(float(JumpHeight.objects.get(pk=height.pk).height), 1.37, places=2)


class TestResultModel(TestCase):
    def test_create_result(self):
        comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z", end_time="2025-01-01T15:00Z")
        athlete = Athlete.objects.create(first_name="T", last_name="Test", sex="M", date_of_birth=date(2003, 1, 2))
        event_type = EventType.objects.create(name="RUNNING")
        event = Event.objects.create(name="200m", event_type=event_type)
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-07-01T10:00Z")
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number=100)
        assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=comp_event,
                                                                       competition_athlete=comp_athlete)
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 1, 1, 10)))
        result = Result.objects.create(
            competition_event_competition_athlete=assignment,
            round=round_obj,
            result_as_number=12.34
        )
        self.assertEqual(result.result_as_number, 12.34)

    def test_update_result(self):
        comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z", end_time="2025-01-01T15:00Z")
        athlete = Athlete.objects.create(first_name="T", last_name="Test", sex="M", date_of_birth=date(2003, 1, 2))
        event_type = EventType.objects.create(name="RUNNING")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event = Event.objects.create(name="200m", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-07-01T10:00Z")
        comp_athlete = CompetitionAthlete.objects.create(competition=comp, athlete=athlete, BIB_number=100)
        assignment = CompetitionEventCompetitionAthlete.objects.create(competition_event=comp_event,
                                                                       competition_athlete=comp_athlete)
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 1, 1, 10)))
        result = Result.objects.create(
            competition_event_competition_athlete=assignment,
            round=round_obj,
            result_as_number=12.34
        )
        result.result_as_number = 12.00
        result.save()
        self.assertEqual(Result.objects.get(pk=result.pk).result_as_number, 12.00)


class TestRoundModel(TestCase):
    def test_create_round(self):
        comp = Competition.objects.create(name="Indoor Champs", start_time="2025-03-01T10:00Z",
                                          end_time="2025-03-01T17:00Z")
        event_type = EventType.objects.create(name="RUNNING")
        event = Event.objects.create(name="60m", event_type=event_type)
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-08-01T10:00Z")
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 3, 1, 10)))
        self.assertEqual(round_obj.round_number, 1)

    def test_update_round_name(self):
        comp = Competition.objects.create(name="Indoor Champs", start_time="2025-03-01T10:00Z",
                                          end_time="2025-03-01T17:00Z")
        event_type = EventType.objects.create(name="RUNNING")
        age_class = AgeClass.objects.create(name="NU23", sex="F")
        event = Event.objects.create(name="60m", event_type=event_type)
        comp_event = CompetitionEvent.objects.create(competition=comp, event=event, age_class=age_class,
                                                     start_time="2025-08-01T10:00Z")
        round_obj = Round.objects.create(competition_event=comp_event, round_number=1,
                                         start_time=make_aware(datetime(2025, 3, 1, 10)), name="Heat A")
        round_obj.name = "Heat B"
        round_obj.save()
        self.assertEqual(Round.objects.get(pk=round_obj.pk).name, "Heat B")
