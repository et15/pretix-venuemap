from django.urls import path

from .views import VenueMapSettings

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/venuemap/settings",
        VenueMapSettings.as_view(),
        name="settings",
    ),
]
