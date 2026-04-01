from __future__ import annotations

import argparse
from pathlib import Path

from benchmark import benchmark_all_for_size, build_average_case_plot, build_summary, format_results_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analise de desempenho de algoritmos de ordenacao em arrays e listas ligadas."
    )
    parser.add_argument(
        "--benchmark-size",
        type=int,
        default=10000,
        help="Tamanho usado para a tabela principal (padrao: 10000).",
    )
    parser.add_argument(
        "--plot-sizes",
        type=int,
        nargs="+",
        default=[5000, 10000, 50000],
        help="Tamanhos usados no grafico do caso medio.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("saida"),
        help="Diretorio de saida para tabela CSV e grafico.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.benchmark_size >= 10000 or any(size >= 50000 for size in args.plot_sizes):
        print(
            "Aviso: os algoritmos implementados sao O(n^2). "
            "Executar os tamanhos exigidos pode levar bastante tempo."
        )

    results_df = benchmark_all_for_size(args.benchmark_size)
    formatted_df = format_results_table(results_df)
    plot_df = build_average_case_plot(args.plot_sizes, args.output_dir / "grafico_caso_medio.png")
    summary = build_summary(results_df)

    results_csv_path = args.output_dir / "resultados_tabela_principal.csv"
    plot_csv_path = args.output_dir / "resultados_grafico_caso_medio.csv"

    results_df.to_csv(results_csv_path, index=False)
    plot_df.to_csv(plot_csv_path, index=False)

    print("\nTABELA DE RESULTADOS")
    print(formatted_df.to_string(index=False))

    print("\nRESUMO AUTOMATICO")
    print(f"- Mais comparacoes: {summary['mais_comparacoes']}")
    print(f"- Mais trocas: {summary['mais_trocas']}")
    print(f"- Mais rapido: {summary['mais_rapido']}")

    print("\nARQUIVOS GERADOS")
    print(f"- Tabela principal CSV: {results_csv_path.resolve()}")
    print(f"- Dados do grafico CSV: {plot_csv_path.resolve()}")
    print(f"- Grafico PNG: {(args.output_dir / 'grafico_caso_medio.png').resolve()}")


if __name__ == "__main__":
    main()
