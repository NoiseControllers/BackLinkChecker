class UrlModel(object):
    def __init__(self, url: str, pos: int, found: str, _type: str):
        self._url = url
        self._pos = pos
        self._found = found
        self._type = _type

    @property
    def url(self) -> str:
        return self._url

    @property
    def pos(self) -> int:
        return self._pos

    @property
    def found(self) -> str:
        return self._found

    @property
    def type(self) -> str:
        return self._type

    @found.setter
    def found(self, value):
        self._found = value

    @type.setter
    def type(self, value):
        self._type = value
