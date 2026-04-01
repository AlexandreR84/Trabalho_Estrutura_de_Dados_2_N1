from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from linked_list import LinkedList
from sorting_algorithms import ARRAY_ALGORITHMS, LINKED_LIST_ALGORITHMS


CASE_LABELS = {
    "melhor": "Melhor Caso",
    "medio": "Caso Medio",
    "pior": "Pior Caso",
}


def gera_dados(size: int):
    """Gera os tres cenarios exigidos no enunciado."""
    # Usa int64 para evitar estouro quando size * size ultrapassa o limite de int32.
    caso_medio = np.random.randint(0, size * size, size=size, dtype=np.int64)
    caso_melhor = np.sort(caso_medio)
    caso_pior = caso_melhor[::-1]
    return caso_medio, caso_melhor, caso_pior


def _assert_sorted(values: list[int]) -> None:
    if values != sorted(values):
        raise ValueError("O algoritmo nao ordenou os dados corretamente.")


def _run_array_algorithm(
    algorithm_name: str,
    structure_name: str,
    case_name: str,
    size: int,
    data: np.ndarray,
    algorithm: Callable[[list[int]], tuple[list[int], int, int]],
) -> dict[str, object]:
    start = perf_counter()
    sorted_values, comparisons, swaps = algorithm(data.tolist())
    elapsed = perf_counter() - start
    _assert_sorted(sorted_values)

    return {
        "estrutura": structure_name,
        "algoritmo": algorithm_name,
        "caso": case_name,
        "tamanho": size,
        "tempo_segundos": elapsed,
        "comparacoes": comparisons,
        "trocas": swaps,
    }


def _run_linked_list_algorithm(
    algorithm_name: str,
    structure_name: str,
    case_name: str,
    size: int,
    data: np.ndarray,
    algorithm: Callable[[LinkedList], tuple[LinkedList, int, int]],
) -> dict[str, object]:
    linked_list = LinkedList(data)
    start = perf_counter()
    sorted_list, comparisons, swaps = algorithm(linked_list)
    elapsed = perf_counter() - start
    _assert_sorted(sorted_list.to_list())

    return {
        "estrutura": structure_name,
        "algoritmo": algorithm_name,
        "caso": case_name,
        "tamanho": size,
        "tempo_segundos": elapsed,
        "comparacoes": comparisons,
        "trocas": swaps,
    }


def benchmark_all_for_size(size: int) -> pd.DataFrame:
    """Executa todos os algoritmos para melhor caso, caso medio e pior caso."""
    caso_medio, caso_melhor, caso_pior = gera_dados(size)
    cases = {
        CASE_LABELS["melhor"]: caso_melhor,
        CASE_LABELS["medio"]: caso_medio,
        CASE_LABELS["pior"]: caso_pior,
    }
    rows: list[dict[str, object]] = []

    for case_name, data in cases.items():
        for algorithm_name, algorithm in ARRAY_ALGORITHMS.items():
            rows.append(
                _run_array_algorithm(
                    algorithm_name=algorithm_name,
                    structure_name="Array",
                    case_name=case_name,
                    size=size,
                    data=data,
                    algorithm=algorithm,
                )
            )
        for algorithm_name, algorithm in LINKED_LIST_ALGORITHMS.items():
            rows.append(
                _run_linked_list_algorithm(
                    algorithm_name=algorithm_name,
                    structure_name="Lista Ligada",
                    case_name=case_name,
                    size=size,
                    data=data,
                    algorithm=algorithm,
                )
            )

    return pd.DataFrame(rows)


def build_average_case_plot(
    sizes: list[int],
    output_path: Path,
) -> pd.DataFrame:
    """Gera os dados do caso medio e salva o grafico comparativo em PNG."""
    rows: list[dict[str, object]] = []

    for size in sizes:
        caso_medio, _, _ = gera_dados(size)
        for algorithm_name, algorithm in ARRAY_ALGORITHMS.items():
            rows.append(
                _run_array_algorithm(
                    algorithm_name=algorithm_name,
                    structure_name="Array",
                    case_name=CASE_LABELS["medio"],
                    size=size,
                    data=caso_medio,
                    algorithm=algorithm,
                )
            )
        for algorithm_name, algorithm in LINKED_LIST_ALGORITHMS.items():
            rows.append(
                _run_linked_list_algorithm(
                    algorithm_name=algorithm_name,
                    structure_name="Lista Ligada",
                    case_name=CASE_LABELS["medio"],
                    size=size,
                    data=caso_medio,
                    algorithm=algorithm,
                )
            )

    plot_df = pd.DataFrame(rows)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))

    for (structure, algorithm), group in plot_df.groupby(["estrutura", "algoritmo"]):
        ordered = group.sort_values("tamanho")
        ax.plot(
            ordered["tamanho"],
            ordered["tempo_segundos"],
            marker="o",
            linewidth=2,
            label=f"{algorithm} - {structure}",
        )

    ax.set_title("Tempo de Execucao no Caso Medio")
    ax.set_xlabel("Tamanho da Entrada")
    ax.set_ylabel("Tempo de Execucao (s)")
    ax.set_xticks(sizes)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return plot_df


def format_results_table(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df.sort_values(["estrutura", "algoritmo", "caso"]).copy()
    ordered["tempo_segundos"] = ordered["tempo_segundos"].map(lambda value: f"{value:.6f}")
    return ordered


def build_summary(df: pd.DataFrame) -> dict[str, str]:
    row_max_comparisons = df.loc[df["comparacoes"].idxmax()]
    row_max_swaps = df.loc[df["trocas"].idxmax()]
    row_fastest = df.loc[df["tempo_segundos"].idxmin()]

    return {
        "mais_comparacoes": (
            f"{row_max_comparisons['algoritmo']} em {row_max_comparisons['estrutura']} "
            f"({row_max_comparisons['caso']}, n={row_max_comparisons['tamanho']}) "
            f"com {int(row_max_comparisons['comparacoes'])} comparacoes."
        ),
        "mais_trocas": (
            f"{row_max_swaps['algoritmo']} em {row_max_swaps['estrutura']} "
            f"({row_max_swaps['caso']}, n={row_max_swaps['tamanho']}) "
            f"com {int(row_max_swaps['trocas'])} trocas."
        ),
        "mais_rapido": (
            f"{row_fastest['algoritmo']} em {row_fastest['estrutura']} "
            f"({row_fastest['caso']}, n={row_fastest['tamanho']}) "
            f"com {row_fastest['tempo_segundos']:.6f} s."
        ),
    }
