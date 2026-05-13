import httpx
from httpx import Response


class Api:
    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._username = username
        self._password = password
        self._auth = httpx.BasicAuth(username=self._username, password=self._password)
        self._client = httpx.AsyncClient(auth=self._auth)

    async def call_api(self, path: str = "") -> Response:
        return await self._client.get(
            "http://" + self._host + "/" + path,
            timeout=10.0,
        )

    async def close(self):
        await self._client.aclose()
