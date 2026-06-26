from dataclasses import asdict, dataclass
from typing import Any, Final
from collections.abc import Sequence


class Unset:
    pass


UNSET: Final[Unset] = Unset()


@dataclass(frozen=True, kw_only=True, slots=True)
class ToDictMixin:
    def to_dict(self, exclude_fields: Sequence[str] = ("id",)) -> dict[str, Any]:
        return {
            field_name: field_value
            for field_name, field_value in asdict(self).items()
            if field_name not in exclude_fields and not isinstance(field_value, Unset)
        }
