from django_filters import rest_framework as filters
from .models import Result, CompetitionAthlete, CompetitionEvent


class ResultFilter(filters.FilterSet):
    competition_event = filters.NumberFilter(
        field_name='competition_event_competition_athlete__competition_event_id'
    )

    class Meta:
        model = Result
        fields = ['round', 'competition_event']


class CompetitionAthleteFilter(filters.FilterSet):
    competition_event_id = filters.NumberFilter(
        method='filter_by_event'
    )

    class Meta:
        model = CompetitionAthlete
        fields = ['competition_id', 'competition_athlete_id', 'competition_event_id']

    def filter_by_event(self, queryset, name, value):
        return queryset.filter(
            competitioneventcompetitionathlete__competition_event_id=value
        ).distinct()


class CompetitionEventFilter(filters.FilterSet):
    class Meta:
        model = CompetitionEvent
        fields = ['competition_id']