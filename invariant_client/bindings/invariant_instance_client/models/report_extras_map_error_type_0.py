from enum import Enum


class ReportExtrasMapErrorType0(str, Enum):
    NOT_FOUND = "not_found"
    NO_MATCH = "no_match"

    def __str__(self) -> str:
        return str(self.value)
