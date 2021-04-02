import time
import typing
import dataclasses

class AmountNotEnough(Exception):
    pass

class NetWorkError(Exception):
    pass

class ResponseStatusError(Exception):
    pass

DEFAULT_MAX_RETRIES: int = 3
DEFAULT_RETRY_DELAY: float = 0.2

@dataclasses.dataclass
class Retry:
    max_retries: int = DEFAULT_MAX_RETRIES
    delay_secs: float = DEFAULT_RETRY_DELAY
    exception: typing.Type[Exception] = NetWorkError

    def execute(self, fn: typing.Callable):  # pyre-ignore
        tries = 0
        while tries < self.max_retries:
            tries += 1
            try:
                return fn()
            except self.exception as e:
                if tries < self.max_retries:
                    # simplest backoff strategy: tries * delay
                    time.sleep(self.delay_secs * tries)
                else:
                    raise e
