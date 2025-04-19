from rest_framework import serializers
from .models import Athlete, Competition, AgeClass, CompetitionEvent, Event, CompetitionAthlete, \
    CompetitionEventCompetitionAthlete, Collective, Round, Result, EventType
from rest_framework.exceptions import ValidationError

from .models.jump_height import JumpHeight


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class AgeClassSerializer(serializers.ModelSerializer):
    minimum_age = serializers.IntegerField(allow_null=True, required=False)
    maximum_age = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = AgeClass
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert empty strings to None for nullable integer fields
        for field in ['minimum_age', 'maximum_age']:
            if field in data and data[field] == '':
                data[field] = None
        return super().to_internal_value(data)


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class JumpHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpHeight
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    round_number = serializers.IntegerField(source="round.round_number", read_only=True)
    athlete = serializers.SerializerMethodField()
    BIB_number = serializers.IntegerField(
        source='competition_event_competition_athlete.competition_athlete.BIB_number',
        read_only=True
    )

    class Meta:
        model = Result
        fields = [
            'result_id',
            'competition_event_competition_athlete',
            'round',
            'round_number',
            'result_as_number',
            'wind_as_number',
            'result_as_char',
            'starting_height',
            'lane_or_order_number',
            'attempt_nr',
            'points_from_result',
            'result_as_char',
            'created_at_dt',
            'valid_until_dt',
            'athlete',
            'BIB_number',
        ]

    def get_athlete(self, obj):
        athlete = obj.competition_event_competition_athlete.competition_athlete.athlete
        return {
            "first_name": athlete.first_name,
            "last_name": athlete.last_name,
        }


class CollectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collective
        fields = '__all__'


class AthleteAssignmentSerializer(serializers.ModelSerializer):
    """ Serializer to include athlete round and lane assignments """
    results = ResultSerializer(many=True, read_only=True)
    round_number = serializers.IntegerField(source="round.round_number", read_only=True)
    lane_number = serializers.IntegerField(source="result.lane_or_order_number",
                                           read_only=True)

    class Meta:
        model = CompetitionEventCompetitionAthlete
        fields = ['competition_event_competition_athlete_id', 'round_number', 'lane_number', 'results']


class RoundSerializer(serializers.ModelSerializer):
    assigned_athletes = AthleteAssignmentSerializer(many=True, read_only=True, source='competitionathlete_set')

    class Meta:
        model = Round
        fields = [
            'round_id', 'round_number', 'start_time', 'end_time', 'name',
            'printout', 'upper_round_id', 'number_of_sub_rounds', 'number_of_max_athletes',
            'assigned_athletes'
        ]


class CompetitionEventSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    age_class = AgeClassSerializer(read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)

    # For POST request, we use PrimaryKeyRelatedField to accept IDs
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), write_only=True,
                                                        required=False)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, required=False)
    age_class_id = serializers.PrimaryKeyRelatedField(queryset=AgeClass.objects.all(), write_only=True, required=False)

    class Meta:
        model = CompetitionEvent
        fields = ['competition_event_id', 'start_time', 'end_time', 'competition', 'event', 'age_class',
                  'wind_measurement', 'printout', 'number_of_rounds', 'athlete_max_count',
                  'competition_id', 'event_id', 'age_class_id', 'rounds', 'number_of_attempts', 'regrouping',
                  'finalists_attempt_count', 'regrouping_done', 'comments']

    def create(self, validated_data):
        competition = validated_data.pop('competition_id', None)
        event = validated_data.pop('event_id', None)
        age_class = validated_data.pop('age_class_id', None)

        competition_event = CompetitionEvent.objects.create(
            **validated_data,
            competition=competition,
            event=event,
            age_class=age_class,
        )

        return competition_event

    def update(self, instance, validated_data):
        competition = validated_data.pop('competition_id', None)
        event = validated_data.pop('event_id', None)
        age_class = validated_data.pop('age_class_id', None)

        if competition:
            instance.competition = competition
        if event:
            instance.event = event
        if age_class:
            instance.age_class = age_class

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CompetitionAthleteSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)  # For GET request
    athlete = AthleteSerializer(read_only=True)  # For GET request
    collective = CollectiveSerializer(read_only=True)

    assigned_events = serializers.SerializerMethodField()

    # For POST request, we use PrimaryKeyRelatedField to accept IDs
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), write_only=True)
    athlete_id = serializers.PrimaryKeyRelatedField(queryset=Athlete.objects.all(), write_only=True)
    collective_id = serializers.PrimaryKeyRelatedField(queryset=Collective.objects.all(), write_only=True)

    BIB_number = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = CompetitionAthlete
        fields = ['competition_athlete_id', 'BIB_number', 'collective', 'competition', 'athlete',
                  'competition_id', 'athlete_id', 'assigned_events', 'collective_id']

    def get_assigned_events(self, obj):
        """Fetch related competition events and ensure only unique athletes are shown."""
        assigned_events = CompetitionEventCompetitionAthlete.objects.filter(competition_athlete=obj)

        return [
            {
                "competition_event_competition_athlete_id": event.pk,
                "competition_event_id": event.competition_event.competition_event_id,
                "event_name": event.competition_event.event.name,
                "age_class": event.competition_event.age_class.name,
                "results": ResultSerializer(event.results.all(), many=True).data,

            }
            for event in assigned_events  # Uses optimized prefetch data
        ]

    def create(self, validated_data):
        competition = validated_data.pop('competition_id', None)
        athlete = validated_data.pop('athlete_id', None)
        collective = validated_data.pop('collective_id', None)

        # Check if the record already exists
        existing_entry = CompetitionAthlete.objects.filter(
            competition=competition,
            athlete=athlete
        ).first()

        if existing_entry:
            return existing_entry

        # Create the object with foreign key relationships
        competition_athlete = CompetitionAthlete.objects.create(
            **validated_data,
            competition=competition,
            athlete=athlete,
            collective=collective,
        )

        return competition_athlete

    def update(self, instance, validated_data):
        competition = validated_data.pop('competition_id', None)
        athlete = validated_data.pop('athlete_id', None)
        collective = validated_data.pop('collective_id', None)

        if competition:
            instance.competition = competition
        if athlete:
            instance.athlete = athlete
        if collective:
            instance.collective = collective

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CompetitionEventCompetitionAthleteSerializer(serializers.ModelSerializer):
    competition_event = CompetitionEventSerializer(read_only=True)  # For GET request

    # For POST request, we use PrimaryKeyRelatedField to accept IDs
    competition_event_id = serializers.PrimaryKeyRelatedField(queryset=CompetitionEvent.objects.all(), write_only=True)
    competition_athlete_id = serializers.PrimaryKeyRelatedField(queryset=CompetitionAthlete.objects.all(),
                                                                write_only=True)

    class Meta:
        model = CompetitionEventCompetitionAthlete
        fields = ['competition_event_competition_athlete_id', 'competition_event',
                  'competition_event_id', 'competition_athlete_id']

    def create(self, validated_data):
        competition_event = validated_data.pop('competition_event_id', None)
        competition_athlete = validated_data.pop('competition_athlete_id', None)

        # Check if the record already exists
        existing_entry = CompetitionEventCompetitionAthlete.objects.filter(
            competition_event=competition_event,
            competition_athlete=competition_athlete
        ).first()

        if existing_entry:
            raise ValidationError({
                "detail": f"Athlete {competition_athlete.athlete.first_name} {competition_athlete.athlete.last_name} "
                          f"is already registered for {competition_event.name}"
            })

        competition_event_athlete = CompetitionEventCompetitionAthlete.objects.create(
            **validated_data,
            competition_event=competition_event,
            competition_athlete=competition_athlete,
        )

        return competition_event_athlete

    def update(self, instance, validated_data):
        competition_event = validated_data.pop('competition_event_id', None)
        competition_athlete = validated_data.pop('competition_athlete_id', None)

        if competition_event:
            instance.competition_event = competition_event
        if competition_athlete:
            instance.competition_athlete = competition_athlete

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
