from typing import List


class AbstractNode:
    def neighbors(self) -> List[AbstractNode]:
        raise NotImplementedError()
