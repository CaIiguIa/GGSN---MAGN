from typing import List, Self


class AbstractNode:
    def neighbors(self) -> List[Self]:
        raise NotImplementedError()
