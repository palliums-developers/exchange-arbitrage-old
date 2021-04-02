import typing
import requests
from util import Retry

DEFAULT_CONNECT_TIMEOUT_SECS: float = 5.0
DEFAULT_TIMEOUT_SECS: float = 30.0
DEFAULT_MAX_RETRIES: int = 15
DEFAULT_RETRY_DELAY: float = 0.2

class CodeError(Exception):
    pass

class NetworkError(Exception):
    pass

class Class:
    def __init__(
        self,
        session: typing.Optional[requests.Session] = None,
        timeout: typing.Optional[typing.Tuple[float, float]] = None,
        retry: typing.Optional[Retry] = None
    ):
        self._session = session or requests.Session()
        self._timeout = timeout or (DEFAULT_CONNECT_TIMEOUT_SECS, DEFAULT_TIMEOUT_SECS)
        self._retry: Retry = retry or Retry(DEFAULT_MAX_RETRIES, DEFAULT_RETRY_DELAY, NetworkError)


    def execute(self, method, params):
        return self._retry.execute(
            lambda :self.execute_without_retry(method, params)
        )

    def execute_without_retry(self, method, parmas):
        pass
