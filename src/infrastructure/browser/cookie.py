from typing import Optional, Dict, Any, Literal


class Cookie:
    """Builder-style Cookie helper.

    Usage:
        cookie = (
            Cookie()
            .set_name("session")
            .set_value("abc")
            .set_domain("example.com")
            .set_path("/")
            .set_http_only(True)
            .build()
        )

    The `build()` method returns a dict matching the cookie schema:
    {name, value, url, domain, path, expires, httpOnly, secure, sameSite}
    """

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

    def build(self) -> Dict[str, Any]:
        if self._name is None or self._value is None:
            raise ValueError("Both 'name' and 'value' are required for a cookie")

        return {
            "name": self._name,
            "value": self._value,
            "url": self._url,
            "domain": self._domain,
            "path": self._path,
            "expires": self._expires,
            "httpOnly": self._httpOnly,
            "secure": self._secure,
            "sameSite": self._sameSite,
        }
