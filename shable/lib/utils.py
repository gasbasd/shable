from tg.controllers.util import LazyUrl

class JSONLazyUrl(LazyUrl):
    def __json__(self):
        return str(self)


def json_lurl(base_url=None, params=None):
    return JSONLazyUrl(base_url, params)
