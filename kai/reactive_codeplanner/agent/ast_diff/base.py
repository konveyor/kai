from abc import ABC, abstractmethod
from typing import Any, Iterator, Self, Generic

from typing_extensions import TypeVar


KT = TypeVar("KT")
VT = TypeVar("VT", bound="DiffableSummary")


class DiffableSummary[KT, VT: "DiffableSummary"](ABC):
    """DiffableSummary is a class to store token information that can
    generate a diff with another version of same type of info
    """

    @abstractmethod
    def to_dict(self) -> dict[KT, VT]:
        """Returns a dict representation of info

        Returns:
            dict[str, Any]: Structured info about this file
        """
        pass

    @abstractmethod
    def diff(self, o: Self) -> dict[str, Any]:
        """Computes diff between current info and another version of same type of info

        Args:
            o (Self): Another version of same type of info

        Returns:
            dict[str, Any]: Structured diff
        """
        pass


class DiffableDict[KT, VT: DiffableSummary](dict[KT, VT], DiffableSummary):
    """A dict that's also a diffable, used to store nested tokens"""

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            if set(self.keys()) != set(o.keys()):
                return False
            for key in self.keys():
                if self[key] != o[key]:
                    return False
            return True
        return False

    def iter_values(self) -> Iterator[VT]:
        values: list[VT] = list(self.values())
        for v in values:
            yield v.to_dict()

    def to_dict(self) -> dict[KT, VT]:
        return {str(k): v.to_dict() for k, v in self.items()}

    def diff(self, o: Self) -> dict[KT, VT]:
        diff = {}
        added = [o[key].to_dict() for key in set(o.keys()) - set(self.keys())]
        if added:
            diff["added"] = added
        removed = [self[key].to_dict() for key in set(self.keys()) - set(o.keys())]
        if removed:
            diff["removed"] = removed
        modified = [
            self[key].diff(o[key])
            for key in set(self.keys()) & set(o.keys())
            if self[key].diff(o[key])
        ]
        if modified:
            diff["modified"] = modified
        return diff
