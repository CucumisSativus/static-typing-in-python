from typing import Protocol
from abc import abstractmethod
from random import random

class AbstractAVScanner(Protocol):
    @abstractmethod
    def scan(self, contents: str) -> bool:
        pass

def route(scanner: AbstractAVScanner) -> str:
    return f"is file malicious?{scanner.scan('content')}"

class EicarDetector:
    def scan(self, content: str) -> bool:
        return 'eicar' in content

class ActualDetector:
    def __run_av(self, content: str) -> bool:
        # run AV, as a suprocess and take output
        return random() > 0.5

    def scan(self, content: str) -> bool:
        return self.__run_av(content)

route(EicarDetector())
route(ActualDetector())

class SealDetector:
    def scan(self, contents: str) -> bool:
        return "seal" in contents

route(SealDetector())
