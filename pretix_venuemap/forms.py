from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm


class VenueMapSettingsForm(SettingsForm):
    venuemap_zoom = forms.IntegerField(
        label=_("Zoom level"),
        help_text=_("Higher values zoom in further (1 = world, 18 = single building)."),
        min_value=1,
        max_value=18,
        required=True,
    )
    venuemap_layout = forms.ChoiceField(
        label=_("Position"),
        choices=(
            ("beside", _("Next to the event information")),
            ("below", _("Below the event information")),
        ),
        required=True,
    )
