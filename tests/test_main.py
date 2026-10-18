from pretix.base.plugins import PLUGIN_LEVEL_EVENT, get_all_plugins

from pretix_venuemap import __version__

MODULE = "pretix_venuemap"


def test_plugin_is_registered():
    metas = [m for m in get_all_plugins() if m.module == MODULE]
    assert len(metas) == 1
    assert metas[0].version == __version__
    assert metas[0].level == PLUGIN_LEVEL_EVENT
