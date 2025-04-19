from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apps.m403.models import (Competition, Event, AgeClass, CompetitionEvent, Round, Result, EventType,
                              UserRole, UserUserRole, JumpHeight, CompetitionAthlete, Athlete,
                              Collective, CompetitionEventCompetitionAthlete)


class CompetitionEventViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        self.user_role = UserRole.objects.create(name="EKJL")
        self.user_user_role = UserUserRole.objects.create(user=self.user, user_role=self.user_role)
        self.client.force_authenticate(user=self.user)
        self.event_type = EventType.objects.create(name="JUMP")
        self.competition = Competition.objects.create(name="Test Comp", start_time="2025-01-01T10:00Z",
                                                      end_time="2025-01-01T12:00Z")
        self.event = Event.objects.create(name="100m", event_type=self.event_type)
        self.age_class = AgeClass.objects.create(name="M", sex="M")

    def test_create_competition_event_with_initial_round(self):
        url = reverse("timetable-list")
        payload = {
            "competition_id": self.competition.pk,
            "event_id": self.event.pk,
            "age_class_id": self.age_class.pk,
            "start_time": "2025-01-01T10:00Z"
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompetitionEvent.objects.count(), 1)
        self.assertEqual(Round.objects.filter(competition_event_id=response.data['competition_event_id']).count(), 1)

    def test_update_rounds_on_event_update(self):
        event = CompetitionEvent.objects.create(
            competition=self.competition,
            event=self.event,
            age_class=self.age_class,
            start_time="2025-01-01T10:00Z",
            number_of_rounds=1
        )
        Round.objects.create(competition_event=event, round_number=1, start_time="2025-01-01T10:00Z")

        url = reverse("timetable-detail", args=[event.competition_event_id])
        payload = {"number_of_rounds": 3}
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Round.objects.filter(competition_event=event).count(), 3)


class ResultViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        self.user_role = UserRole.objects.create(name="EKJL")
        self.user_user_role = UserUserRole.objects.create(user=self.user, user_role=self.user_role)
        self.client.force_authenticate(user=self.user)

    def test_bulk_update_results_empty(self):
        url = "/api/results/bulk_update_results/"  # Direct path instead of reverse()
        response = self.client.post(url, [], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Results updated successfully")

    def test_get_results_by_round(self):
        self.comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z",
                                               end_time="2025-01-01T15:00Z")
        self.event_type = EventType.objects.create(name="RUNNING")
        self.event = Event.objects.create(name="100m", event_type=self.event_type)
        self.age_class = AgeClass.objects.create(name="M", sex="M")
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event,
                                                          start_time="2025-01-01T09:00Z", age_class=self.age_class)
        round_obj = Round.objects.create(competition_event=self.comp_event, round_number=1,
                                         start_time="2025-01-01T10:00Z")
        url = f"/api/results/?round={round_obj.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JumpHeightViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        self.role = UserRole.objects.create(name="EKJL")
        UserUserRole.objects.create(user=self.user, user_role=self.role)
        self.client.force_authenticate(user=self.user)

        self.comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z",
                                               end_time="2025-01-01T15:00Z")
        self.event_type = EventType.objects.create(name="JUMP")
        self.event = Event.objects.create(name="HJ", event_type=self.event_type)
        self.age_class = AgeClass.objects.create(name="M", sex="M")
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event,
                                                          age_class=self.age_class, start_time="2025-01-01T09:00Z")
        self.round = Round.objects.create(competition_event=self.comp_event, round_number=1,
                                          start_time="2025-01-01T10:00Z")

    def test_create_jump_height(self):
        url = "/api/jump-heights/"
        payload = {"round": self.round.pk, "height": "1.50", "order": 1}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JumpHeight.objects.count(), 1)

    def test_filter_jump_height_by_round(self):
        JumpHeight.objects.create(round=self.round, height=1.45, order=1)
        url = f"/api/jump-heights/?round={self.round.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CompetitionEventAthleteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        self.role = UserRole.objects.create(name="EKJL")
        UserUserRole.objects.create(user=self.user, user_role=self.role)
        self.client.force_authenticate(user=self.user)

        self.comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z",
                                               end_time="2025-01-01T15:00Z")
        self.event_type = EventType.objects.create(name="RUNNING")
        self.event = Event.objects.create(name="100m", event_type=self.event_type)
        self.age_class = AgeClass.objects.create(name="M", sex="M")
        self.comp_event = CompetitionEvent.objects.create(competition=self.comp, event=self.event,
                                                          age_class=self.age_class, start_time="2025-01-01T09:00Z")

        self.athlete = Athlete.objects.create(first_name="Test", last_name="Person", date_of_birth="2000-01-01",
                                              sex="M")
        self.collective = Collective.objects.create(name="Club", abbreviation="CLUB")
        self.comp_athlete = CompetitionAthlete.objects.create(competition=self.comp, athlete=self.athlete,
                                                              BIB_number=101, collective=self.collective)

    def test_assign_athlete_to_event(self):
        url = "/api/competition-event-athletes/"
        payload = {
            "competition_event_id": self.comp_event.pk,
            "competition_athlete_id": self.comp_athlete.pk
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompetitionEventCompetitionAthlete.objects.count(), 1)

    def test_filter_by_competition_event(self):
        other_event = CompetitionEvent.objects.create(
            competition=self.comp,
            event=self.event,
            age_class=self.age_class,
            start_time="2025-01-01T11:00Z"
        )

        CompetitionEventCompetitionAthlete.objects.create(
            competition_event=self.comp_event,
            competition_athlete=self.comp_athlete
        )

        CompetitionEventCompetitionAthlete.objects.create(
            competition_event=other_event,
            competition_athlete=self.comp_athlete
        )

        url = f"/api/competition-event-athletes/?competition_event_id={self.comp_event.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one should match


class CompetitionAthleteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        self.role = UserRole.objects.create(name="EKJL")
        UserUserRole.objects.create(user=self.user, user_role=self.role)
        self.client.force_authenticate(user=self.user)

        self.comp = Competition.objects.create(name="Meet", start_time="2025-01-01T09:00Z",
                                               end_time="2025-01-01T15:00Z")
        self.athlete = Athlete.objects.create(first_name="John", last_name="Doe", date_of_birth="2000-01-01", sex="M")
        self.collective = Collective.objects.create(name="Test Club", abbreviation="TC")
        self.comp_athlete = CompetitionAthlete.objects.create(competition=self.comp, athlete=self.athlete,
                                                              BIB_number=12, collective=self.collective)

    def test_get_athletes_by_competition_id(self):
        url = f"/api/competition-athletes/?competition_id={self.comp.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class RoundViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='pass')
        role = UserRole.objects.create(name="EKJL")
        UserUserRole.objects.create(user=self.user, user_role=role)
        self.client.force_authenticate(user=self.user)

        self.comp = Competition.objects.create(name="Comp", start_time="2025-01-01T09:00Z", end_time="2025-01-01T10:00Z")
        event_type = EventType.objects.create(name="RUNNING")
        event = Event.objects.create(name="400m", event_type=event_type)
        age_class = AgeClass.objects.create(name="M", sex="M")
        self.comp_event = CompetitionEvent.objects.create(
            competition=self.comp, event=event, age_class=age_class, start_time="2025-01-01T09:00Z"
        )
        self.round = Round.objects.create(competition_event=self.comp_event, round_number=1, start_time="2025-01-01T09:30Z")

    def test_filter_rounds_by_competition_event(self):
        url = f"/api/rounds/?competition_event_id={self.comp_event.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
