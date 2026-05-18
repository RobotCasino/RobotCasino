from typing import Optional, Literal


class Cookie:
    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._value: Optional[str] = None
        self._url: str = ""
        self._domain: str = ""
        self._path: Optional[str] = None
        self._expires: Optional[float] = None
        self._httpOnly: Optional[bool] = None
        self._secure: Optional[bool] = None
        self._sameSite: Optional[Literal["Lax", "None", "Strict"]] = None

    def set_name(self, name: str) -> "Cookie":
        self._name = name
        return self

    def set_value(self, value: str) -> "Cookie":
        self._value = value
        return self

    def set_url(self, url: Optional[str]) -> "Cookie":
        self._url = url or ""
        return self

    def set_domain(self, domain: Optional[str]) -> "Cookie":
        self._domain = domain or ""
        return self

    def set_path(self, path: Optional[str]) -> "Cookie":
        self._path = path
        return self

    def set_expires(self, expires: float | int | None) -> "Cookie":
        if expires is None:
            self._expires = None
        else:
            self._expires = float(expires)

        return self

    def set_http_only(self, http_only: Optional[bool]) -> "Cookie":
        self._httpOnly = http_only
        return self

    def set_secure(self, secure: Optional[bool]) -> "Cookie":
        self._secure = secure
        return self

    def set_same_site(self, same_site: Optional[Literal["Lax", "None", "Strict"]]) -> "Cookie":
        if same_site is not None and same_site not in ("Lax", "None", "Strict"):
            raise ValueError("sameSite must be one of: 'Lax', 'None', 'Strict'")
        self._sameSite = same_site
        return self

    def get_name(self) -> Optional[str]:
        return self._name

    def get_value(self) -> Optional[str]:
        return self._value

    def get_url(self) -> str:
        return self._url

    def get_domain(self) -> str:
        return self._domain

    def get_path(self) -> Optional[str]:
        return self._path

    def get_expires(self) -> Optional[float]:
        return self._expires

    def get_http_only(self) -> Optional[bool]:
        return self._httpOnly

    def get_secure(self) -> Optional[bool]:
        return self._secure

    def get_same_site(self) -> Optional[Literal["Lax", "None", "Strict"]]:
        return self._sameSite

    def to_dict(self) -> dict[str, str | bool | float]:
        data: dict[str, str | bool | float] = {}
        if self._name is not None:
            data["name"] = self._name
        if self._value is not None:
            data["value"] = self._value
        if self._domain:
            data["domain"] = self._domain
        if self._path is not None:
            data["path"] = self._path
        if self._secure is not None:
            data["secure"] = self._secure
        if self._httpOnly is not None:
            data["httpOnly"] = self._httpOnly
        if self._expires is not None:
            data["expires"] = self._expires
        if self._url:
            data["url"] = self._url
        if self._sameSite is not None:
            data["sameSite"] = self._sameSite

        return data