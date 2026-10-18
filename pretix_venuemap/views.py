from django.urls import reverse
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin

from .forms import VenueMapSettingsForm


class VenueMapSettings(EventSettingsViewMixin, EventSettingsFormView):
    template_name = "pretix_venuemap/settings.html"
    form_class = VenueMapSettingsForm
    permission = "can_change_event_settings"

    def get_success_url(self):
        return reverse(
            "plugins:pretix_venuemap:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
