from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional


@dataclass
class Node:
    """No simples usado na implementacao manual da lista ligada."""

    value: int
    next: Optional["Node"] = None


class LinkedList:
    """Lista ligada simples sem apoio de estruturas nativas para armazenar os nos."""

    def __init__(self, values: Optional[Iterable[int]] = None) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length = 0

        if values is not None:
            for value in values:
                self.append(int(value))

    def append(self, value: int) -> None:
        """Insere um elemento ao final da lista."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def copy(self) -> "LinkedList":
        """Cria uma copia no a no, preservando a lista original."""
        copied = LinkedList()
        current = self.head
        while current is not None:
            copied.append(current.value)
            current = current.next
        return copied

    def to_list(self) -> list[int]:
        """Converte a lista ligada em lista Python apenas para exibicao e validacao."""
        values: list[int] = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def __iter__(self) -> Iterator[int]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return f"LinkedList(length={self.length})"
