from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import LoginView, EventViewSet, AthleteViewSet, CompetitionViewSet, AgeClassViewSet, \
    CompetitionEventViewSet, CompetitionAthleteViewSet, CompetitionEventCompetitionAthleteViewSet, CollectiveViewSet, \
    RoundViewSet, ResultViewSet, JumpHeightViewSet
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = DefaultRouter()
router.register(r'athletes', AthleteViewSet, basename='athletes')
router.register(r'competitions', CompetitionViewSet, basename='competitions')
router.register(r'collectives', CollectiveViewSet, basename='collectives')
router.register(r'age-classes', AgeClassViewSet, basename='age-classes')
router.register(r'events', EventViewSet, basename='events')
router.register('timetable', CompetitionEventViewSet, basename='timetable')
router.register(r'competition-athletes', CompetitionAthleteViewSet, basename='competition-athlete')
router.register(r'competition-event-athletes', CompetitionEventCompetitionAthleteViewSet, basename='competition-event-athlete')
router.register(r'rounds', RoundViewSet, basename='rounds')
router.register(r'results', ResultViewSet, basename='results')
router.register(r'jump-heights', JumpHeightViewSet, basename='jump-heights')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login (POST)
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh Token (POST)

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # Swagger
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),  # Swagger
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # Swagger
]
