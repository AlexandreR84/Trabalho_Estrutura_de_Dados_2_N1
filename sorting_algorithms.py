from __future__ import annotations

from typing import Callable

from linked_list import LinkedList, Node


SortArrayResult = tuple[list[int], int, int]
SortLinkedListResult = tuple[LinkedList, int, int]


def bubble_sort_array(data: list[int]) -> SortArrayResult:
    """Ordena um array com Bubble Sort e contabiliza comparacoes e trocas."""
    arr = list(data)
    comparisons = 0
    swaps = 0
    n = len(arr)

    for end in range(n - 1, 0, -1):
        swapped = False
        for index in range(end):
            comparisons += 1
            if arr[index] > arr[index + 1]:
                arr[index], arr[index + 1] = arr[index + 1], arr[index]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return arr, comparisons, swaps


def selection_sort_array(data: list[int]) -> SortArrayResult:
    """Ordena um array com Selection Sort e contabiliza comparacoes e trocas."""
    arr = list(data)
    comparisons = 0
    swaps = 0
    n = len(arr)

    for start in range(n - 1):
        min_index = start
        for index in range(start + 1, n):
            comparisons += 1
            if arr[index] < arr[min_index]:
                min_index = index
        if min_index != start:
            arr[start], arr[min_index] = arr[min_index], arr[start]
            swaps += 1

    return arr, comparisons, swaps


def insertion_sort_array(data: list[int]) -> SortArrayResult:
    """Ordena um array com Insertion Sort e contabiliza comparacoes e deslocamentos."""
    arr = list(data)
    comparisons = 0
    swaps = 0

    for index in range(1, len(arr)):
        key = arr[index]
        position = index - 1

        while position >= 0:
            comparisons += 1
            if arr[position] > key:
                arr[position + 1] = arr[position]
                swaps += 1
                position -= 1
            else:
                break

        arr[position + 1] = key

    return arr, comparisons, swaps


def bubble_sort_lista(linked_list: LinkedList) -> SortLinkedListResult:
    """Bubble Sort para lista ligada, trocando os valores dos nos."""
    lista = linked_list.copy()
    comparisons = 0
    swaps = 0

    if lista.head is None:
        return lista, comparisons, swaps

    swapped = True
    while swapped:
        swapped = False
        current = lista.head
        while current is not None and current.next is not None:
            comparisons += 1
            if current.value > current.next.value:
                current.value, current.next.value = current.next.value, current.value
                swaps += 1
                swapped = True
            current = current.next

    return lista, comparisons, swaps


def selection_sort_lista(linked_list: LinkedList) -> SortLinkedListResult:
    """Selection Sort para lista ligada, procurando o menor valor no restante da lista."""
    lista = linked_list.copy()
    comparisons = 0
    swaps = 0

    current = lista.head
    while current is not None:
        min_node = current
        search = current.next
        while search is not None:
            comparisons += 1
            if search.value < min_node.value:
                min_node = search
            search = search.next
        if min_node is not current:
            current.value, min_node.value = min_node.value, current.value
            swaps += 1
        current = current.next

    return lista, comparisons, swaps


def _sorted_insert(
    sorted_head: Node | None,
    node: Node,
) -> tuple[Node, int, int]:
    """Insere um no na sublista ordenada usada pelo Insertion Sort em lista ligada."""
    comparisons = 0
    swaps = 0

    if sorted_head is None:
        node.next = None
        return node, comparisons, swaps

    comparisons += 1
    if node.value < sorted_head.value:
        node.next = sorted_head
        swaps += 1
        return node, comparisons, swaps

    current = sorted_head
    while current.next is not None:
        comparisons += 1
        if current.next.value > node.value:
            break
        current = current.next

    node.next = current.next
    current.next = node
    swaps += 1
    return sorted_head, comparisons, swaps


def insertion_sort_lista(linked_list: LinkedList) -> SortLinkedListResult:
    """Insertion Sort para lista ligada, religando os nos em ordem crescente."""
    lista = linked_list.copy()
    comparisons = 0
    swaps = 0
    sorted_head: Node | None = None
    current = lista.head

    while current is not None:
        next_node = current.next
        sorted_head, local_comparisons, local_swaps = _sorted_insert(sorted_head, current)
        comparisons += local_comparisons
        swaps += local_swaps
        current = next_node

    lista.head = sorted_head
    tail = None
    current = lista.head
    while current is not None:
        tail = current
        current = current.next
    lista.tail = tail

    return lista, comparisons, swaps


ARRAY_ALGORITHMS: dict[str, Callable[[list[int]], SortArrayResult]] = {
    "Bubble Sort": bubble_sort_array,
    "Selection Sort": selection_sort_array,
    "Insertion Sort": insertion_sort_array,
}


LINKED_LIST_ALGORITHMS: dict[str, Callable[[LinkedList], SortLinkedListResult]] = {
    "Bubble Sort": bubble_sort_lista,
    "Selection Sort": selection_sort_lista,
    "Insertion Sort": insertion_sort_lista,
}
