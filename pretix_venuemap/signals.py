from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.settings import global_settings_object, settings_hierarkey
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import front_page_top, html_head

settings_hierarkey.add_default("venuemap_zoom", 15, int)
settings_hierarkey.add_default("venuemap_layout", "beside", str)


def _tile_settings(request):
    """
    Use the tile server configured in the global settings, i.e. the same one the
    backend map uses. Without one there is nothing to show.
    """
    gs = global_settings_object(request).settings
    if not gs.leaflet_tiles:
        return None
    return gs.leaflet_tiles, gs.leaflet_tiles_attribution or ""


def _coordinates(ev):
    # Only show a map if the shop shows a location at all, so that organizers who
    # hide the location do not leak it through stray coordinates.
    if not ev.location or ev.geo_lat is None or ev.geo_lon is None:
        return None
    return ev.geo_lat, ev.geo_lon


@receiver(html_head, dispatch_uid="venuemap_html_head")
def presale_html_head(sender, request=None, **kwargs):
    if getattr(request, "pci_dss_payment_page", False):
        return ""
    url = resolve(request.path_info)
    if url.namespace != "presale" or url.url_name != "event.index":
        return ""
    if not _tile_settings(request):
        return ""
    return get_template("pretix_venuemap/head.html").render({})


@receiver(front_page_top, dispatch_uid="venuemap_front_page_top")
def presale_front_page_top(sender, request=None, subevent=None, **kwargs):
    tiles = _tile_settings(request)
    if not tiles:
        return ""
    ev = subevent or sender
    coords = _coordinates(ev)
    if not coords:
        return ""
    return get_template("pretix_venuemap/front_page.html").render(
        {
            "tiles": tiles[0],
            "attribution": tiles[1],
            "lat": coords[0],
            "lon": coords[1],
            "zoom": sender.settings.venuemap_zoom,
            "layout": sender.settings.venuemap_layout,
            "location": ", ".join(
                line.strip() for line in str(ev.location).splitlines() if line.strip()
            ),
        },
        request,
    )


@receiver(nav_event_settings, dispatch_uid="venuemap_nav")
def control_nav(sender, request=None, **kwargs):
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_change_event_settings", request=request
    ):
        return []
    url = resolve(request.path_info)
    return [
        {
            "label": _("Venue map"),
            "url": reverse(
                "plugins:pretix_venuemap:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.event.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_venuemap",
        }
    ]
