from django.db.models import Prefetch
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ResultFilter, CompetitionAthleteFilter, CompetitionEventFilter
from rest_framework import status
from .models import Athlete, Competition, AgeClass, CompetitionEvent, UserUserRole, Event, CompetitionAthlete, \
    CompetitionEventCompetitionAthlete, Collective, Round, Result
from .models.jump_height import JumpHeight
from .serializers import AthleteSerializer, CompetitionSerializer, AgeClassSerializer, CompetitionEventSerializer, \
    EventSerializer, CompetitionAthleteSerializer, CompetitionEventCompetitionAthleteSerializer, CollectiveSerializer, \
    RoundSerializer, ResultSerializer, JumpHeightSerializer
from .permissions import IsEKJLUser
from rest_framework.decorators import action
from django.db import transaction


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            user_roles = list(UserUserRole.objects.filter(user=user).values_list('user_role__name', flat=True))

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'roles': user_roles

            })
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class AthleteViewSet(ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    permission_classes = [IsEKJLUser]

    # Overriding destroy to disable DELETE
    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "DELETE method not allowed."}, status=405)


class CompetitionViewSet(ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsEKJLUser]

    # Overriding destroy to disable DELETE
    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "DELETE method not allowed."}, status=405)


class ResultViewSet(ModelViewSet):
    queryset = Result.objects.select_related(
        'round',
        'competition_event_competition_athlete',
        'competition_event_competition_athlete__competition_athlete',
        'competition_event_competition_athlete__competition_athlete__athlete',
        'competition_event_competition_athlete__competition_event'

    )
    serializer_class = ResultSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResultFilter

    @action(detail=False, methods=["post"])
    def bulk_update_results(self, request):
        try:
            for entry in request.data:
                athlete_id = entry["competition_event_competition_athlete_id"]
                round_id = entry["round_id"]
                attempt_nr = entry.get("attempt_nr")  # Might be None
                wind = entry.get("wind_as_number")
                result = entry.get("result_as_number")
                starting_height = entry.get("starting_height")
                result_as_char = entry.get("result_as_char")
                result_as_number = entry.get("result_as_number")

                is_vertical_jump = result_as_char is not None and result_as_number is not None

                if is_vertical_jump:
                    # For high jump / pole vault — key: athlete + round + height
                    Result.objects.update_or_create(
                        competition_event_competition_athlete_id=athlete_id,
                        round_id=round_id,
                        result_as_number=result_as_number,  # use height as unique key
                        defaults={
                            "result_as_char": result_as_char,
                            "starting_height": starting_height,
                        }
                    )

                elif starting_height is not None:
                    # Special case: just setting starting_height for all results for this athlete+round
                    Result.objects.filter(
                        competition_event_competition_athlete_id=athlete_id,
                        round_id=round_id
                    ).update(starting_height=starting_height)

                else:
                    # Reuse lane if already exists
                    existing_result = Result.objects.filter(
                        competition_event_competition_athlete_id=athlete_id,
                        round_id=round_id
                    ).exclude(lane_or_order_number__isnull=True).first()

                    lane_number = existing_result.lane_or_order_number if existing_result else None

                    defaults = {}
                    if result is not None:
                        defaults["result_as_number"] = result
                    if wind is not None:
                        defaults["wind_as_number"] = wind
                    if lane_number is not None:
                        defaults["lane_or_order_number"] = lane_number

                    Result.objects.update_or_create(
                        competition_event_competition_athlete_id=athlete_id,
                        round_id=round_id,
                        attempt_nr=attempt_nr,
                        defaults=defaults
                    )

            return Response({"message": "Results updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AgeClassViewSet(ModelViewSet):
    queryset = AgeClass.objects.all()
    serializer_class = AgeClassSerializer
    permission_classes = [IsEKJLUser]

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "DELETE method not allowed."}, status=405)


class CompetitionEventViewSet(ModelViewSet):
    queryset = CompetitionEvent.objects.all()
    serializer_class = CompetitionEventSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompetitionEventFilter
    lookup_field = "competition_event_id"

    def create(self, request, *args, **kwargs):
        competition_id = request.data.get("competition_id")
        if not competition_id:
            raise ValidationError({"competition": "This field is required."})

        with transaction.atomic():  # Ensures atomic DB transactions
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            competition_event = serializer.save()  # Save and get the created instance

            # Create an initial round
            Round.objects.create(
                competition_event=competition_event,
                round_number=1,  # Default first round
                start_time=competition_event.start_time  # Initial start time
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Allow PATCH for partial updates
        instance = self.get_object()
        previous_rounds = instance.number_of_rounds  # Store previous round count before update

        # Validate and update fields dynamically
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            self.perform_update(serializer)
            instance.refresh_from_db()

            num_rounds = instance.number_of_rounds or 1

            if previous_rounds != num_rounds:
                existing_rounds = Round.objects.filter(competition_event=instance).order_by("round_number")
                existing_round_count = existing_rounds.count()

                if existing_round_count < num_rounds:
                    # Create additional rounds
                    for round_number in range(existing_round_count + 1, num_rounds + 1):
                        Round.objects.create(
                            competition_event=instance,
                            round_number=round_number,
                            start_time=instance.start_time
                        )

                elif existing_round_count > num_rounds:
                    # Delete excess rounds
                    existing_rounds[num_rounds:].delete()

        return Response(serializer.data, status=status.HTTP_200_OK)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEKJLUser]

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "DELETE method not allowed."}, status=405)


class CompetitionAthleteViewSet(ModelViewSet):
    queryset = CompetitionAthlete.objects.all()
    serializer_class = CompetitionAthleteSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompetitionAthleteFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        competition_event_id = self.request.query_params.get("competition_event_id")

        if competition_event_id:
            queryset = queryset.filter(
                competitioneventcompetitionathlete__competition_event_id=competition_event_id
            ).distinct()

        return queryset.prefetch_related(
            Prefetch(
                "competitioneventcompetitionathlete_set",
                queryset=CompetitionEventCompetitionAthlete.objects.select_related("competition_event"),
                to_attr="assigned_event_list",
            ),
            "competition",
            "athlete",
            "collective"
        )

    @action(detail=False, methods=['post'], url_path='assign-rounds-lanes')
    def assign_rounds_and_lanes(self, request):
        """
        Update round_number and lane_number for each athlete in the competition.
        """
        data = request.data

        for athlete_data in data:
            competition_event_competition_athlete_id = athlete_data.get("competition_event_competition_athlete_id")
            round_id = athlete_data.get("round_number")
            lane_number = athlete_data.get("lane_number")

            if not competition_event_competition_athlete_id or not round_id or not lane_number:
                return Response({"error": "Missing fields in request"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                event_athlete = CompetitionEventCompetitionAthlete.objects.get(
                    pk=competition_event_competition_athlete_id)
                round_instance = Round.objects.get(pk=round_id)  # ✅ Fetch `Round` by `round_id`

                # Update all results (e.g. all attempts) for this athlete & round
                results = Result.objects.filter(
                    competition_event_competition_athlete=event_athlete,
                    round=round_instance
                )

                if results.exists():
                    results.update(lane_or_order_number=lane_number)
                else:
                    # Create at least one result to store lane (can be updated later with actual result)
                    Result.objects.create(
                        competition_event_competition_athlete=event_athlete,
                        round=round_instance,
                        lane_or_order_number=lane_number
                    )

            except (CompetitionEventCompetitionAthlete.DoesNotExist, Round.DoesNotExist):
                return Response(
                    {
                        "error": f"Invalid competition_event_competition_athlete_id {competition_event_competition_athlete_id} or round_id {round_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({"message": "Assignments saved successfully"}, status=status.HTTP_200_OK)


class CompetitionEventCompetitionAthleteViewSet(ModelViewSet):
    queryset = CompetitionEventCompetitionAthlete.objects.all()
    serializer_class = CompetitionEventCompetitionAthleteSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["competition_event_id"]


class CollectiveViewSet(ModelViewSet):
    queryset = Collective.objects.all()
    serializer_class = CollectiveSerializer
    permission_classes = [IsEKJLUser]


class RoundViewSet(ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["competition_event_id"]

    def create(self, request, *args, **kwargs):
        """
        Prevent direct creation via API (Rounds should be created via CompetitionEvent updates).
        """
        return Response({"error": "Rounds must be created via CompetitionEvent updates."},
                        status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class JumpHeightViewSet(ModelViewSet):
    queryset = JumpHeight.objects.all().order_by('round', 'order')
    serializer_class = JumpHeightSerializer
    permission_classes = [IsEKJLUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["round"]

    @action(detail=False, methods=["post"], url_path="bulk_create")
    def bulk_create(self, request):
        data = request.data

        if not isinstance(data, list):
            return Response({"detail": "Expected a list of heights."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = JumpHeightSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
