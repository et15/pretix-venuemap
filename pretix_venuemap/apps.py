from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PLUGIN_LEVEL_EVENT, PluginConfig
except ImportError:
    raise RuntimeError(
        "Please use pretix 2026.0.0 or above to run this plugin!",
    ) from None


class PluginApp(PluginConfig):
    default = True
    name = "pretix_venuemap"
    verbose_name = "Venue map"

    class PretixPluginMeta:
        name = gettext_lazy("Venue map")
        author = "ET15"
        description = gettext_lazy(
            "Shows a map of the event location using the tile server"
        )
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2026.0.0"
        level = PLUGIN_LEVEL_EVENT
        settings_links = []
        navigation_links = []

    def ready(self):
        from . import signals  # NOQA
