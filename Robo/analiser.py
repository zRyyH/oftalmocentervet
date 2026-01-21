#!/usr/bin/env python3
"""
JSON Translator - Traduz estruturas JSON complexas para Markdown otimizado para LLMs
"""

import json
import sys
import re
from collections import defaultdict
from typing import Any
# from datetime import datetime


class JSONTranslator:
    def __init__(self, max_examples: int = 3):
        self.max_examples = max_examples
        self.fields = defaultdict(
            lambda: {
                "types": set(),
                "examples": [],
                "count": 0,
                "null_count": 0,
                "min_val": None,
                "max_val": None,
                "min_len": None,
                "max_len": None,
                "pattern": None,
            }
        )
        self.root_type = None
        self.total_records = 0

    def analyze(self, data: Any) -> dict:
        """Analisa o JSON e retorna estrutura detalhada."""
        if isinstance(data, list):
            self.root_type = "array"
            self.total_records = len(data)
            for item in data:
                self._process(item, "item")
        elif isinstance(data, dict):
            self.root_type = "object"
            self.total_records = 1
            self._process(data, "root")
        return self.fields

    def _process(self, value: Any, path: str):
        """Processa recursivamente cada valor."""
        node = self.fields[path]
        node["count"] += 1

        if value is None:
            node["types"].add("null")
            node["null_count"] += 1
        elif isinstance(value, bool):
            node["types"].add("boolean")
            self._add_example(node, value)
        elif isinstance(value, int):
            node["types"].add("integer")
            self._update_numeric_stats(node, value)
            self._add_example(node, value)
        elif isinstance(value, float):
            node["types"].add("number")
            self._update_numeric_stats(node, value)
            self._add_example(node, round(value, 4))
        elif isinstance(value, str):
            node["types"].add("string")
            self._update_string_stats(node, value)
            self._detect_pattern(node, value)
            self._add_example(node, self._truncate(value, 60))
        elif isinstance(value, list):
            node["types"].add("array")
            self._update_array_stats(node, value)
            for item in value:
                self._process(item, f"{path}[]")
        elif isinstance(value, dict):
            node["types"].add("object")
            for key, val in value.items():
                self._process(val, f"{path}.{key}")

    def _add_example(self, node: dict, value):
        if len(node["examples"]) < self.max_examples:
            if value not in node["examples"]:
                node["examples"].append(value)

    def _truncate(self, s: str, max_len: int) -> str:
        return f"{s[:max_len]}..." if len(s) > max_len else s

    def _update_numeric_stats(self, node: dict, value):
        if node["min_val"] is None or value < node["min_val"]:
            node["min_val"] = value
        if node["max_val"] is None or value > node["max_val"]:
            node["max_val"] = value

    def _update_string_stats(self, node: dict, value: str):
        length = len(value)
        if node["min_len"] is None or length < node["min_len"]:
            node["min_len"] = length
        if node["max_len"] is None or length > node["max_len"]:
            node["max_len"] = length

    def _update_array_stats(self, node: dict, value: list):
        length = len(value)
        if node["min_len"] is None or length < node["min_len"]:
            node["min_len"] = length
        if node["max_len"] is None or length > node["max_len"]:
            node["max_len"] = length

    def _detect_pattern(self, node: dict, value: str):
        """Detecta padrões semânticos em strings."""
        if node["pattern"]:
            return

        patterns = [
            (r"^\d{4}-\d{2}-\d{2}(T|\s)\d{2}:\d{2}:\d{2}", "datetime_iso"),
            (r"^\d{4}-\d{2}-\d{2}$", "date_iso"),
            (r"^\d{2}/\d{2}/\d{4}$", "date_br"),
            (r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", "uuid"),
            (r"^[a-f0-9]{24}$", "mongodb_id"),
            (r"^https?://", "url"),
            (r"^[^@]+@[^@]+\.[^@]+$", "email"),
            (r"^\+?\d{10,15}$", "phone"),
            (r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", "cpf"),
            (r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", "cnpj"),
            (r"^\d{5}-?\d{3}$", "cep"),
            (r"^#[0-9a-fA-F]{6}$", "hex_color"),
            (r"^(true|false)$", "boolean_string"),
            (r"^\d+$", "numeric_string"),
            (r"^-?\d+\.\d+$", "decimal_string"),
        ]

        for regex, pattern_name in patterns:
            if re.match(regex, value, re.IGNORECASE):
                node["pattern"] = pattern_name
                break

    def generate_report(self, json_path: str) -> str:
        """Gera relatório Markdown otimizado para LLMs."""
        lines = []

        # Cabeçalho
        lines.append(f"# JSON Schema: `{json_path}`\n")

        # Resumo
        lines.append("## Resumo\n")
        lines.append(f"- **Tipo raiz:** `{self.root_type}`")
        if self.root_type == "array":
            lines.append(f"- **Total de registros:** {self.total_records}")
        lines.append(f"- **Campos únicos:** {len(self.fields)}\n")

        # Estrutura hierárquica
        lines.append("## Estrutura\n")
        lines.append("```")
        lines.append(self._build_tree())
        lines.append("```\n")

        # Detalhamento dos campos
        lines.append("## Campos\n")

        for path in sorted(self.fields.keys()):
            info = self.fields[path]
            lines.append(self._format_field(path, info))

        # Campos opcionais vs obrigatórios
        if self.total_records > 1:
            lines.append("## Análise de Obrigatoriedade\n")
            required = []
            optional = []
            for path, info in self.fields.items():
                if "[]" in path:
                    continue
                ratio = info["count"] / self.total_records
                if ratio >= 0.99:
                    required.append(path)
                elif ratio < 0.99:
                    optional.append(f"{path} ({ratio*100:.0f}%)")

            if required:
                lines.append(f"**Obrigatórios:** `{'`, `'.join(sorted(required))}`\n")
            if optional:
                lines.append(f"**Opcionais:** `{'`, `'.join(sorted(optional))}`\n")

        return "\n".join(lines)

    def _build_tree(self) -> str:
        """Constrói representação em árvore da estrutura."""
        tree_lines = []
        paths = sorted(self.fields.keys())

        for path in paths:
            info = self.fields[path]
            types = "|".join(sorted(info["types"]))
            pattern = f" <{info['pattern']}>" if info["pattern"] else ""

            depth = path.count(".") + path.count("[]")
            indent = "  " * depth
            name = path.split(".")[-1].replace("[]", "[*]")

            tree_lines.append(f"{indent}{name}: {types}{pattern}")

        return "\n".join(tree_lines)

    def _format_field(self, path: str, info: dict) -> str:
        """Formata informações de um campo."""
        types = ", ".join(sorted(info["types"]))
        lines = [f"### `{path}`\n"]
        lines.append(f"- **Tipo:** {types}")

        if info["pattern"]:
            lines.append(f"- **Formato:** {info['pattern']}")

        lines.append(f"- **Ocorrências:** {info['count']}")

        if info["null_count"] > 0:
            lines.append(f"- **Nulos:** {info['null_count']}")

        if info["min_val"] is not None:
            lines.append(f"- **Range:** {info['min_val']} → {info['max_val']}")

        if info["min_len"] is not None and "string" in info["types"]:
            lines.append(
                f"- **Comprimento:** {info['min_len']} - {info['max_len']} chars"
            )

        if info["min_len"] is not None and "array" in info["types"]:
            lines.append(f"- **Tamanho:** {info['min_len']} - {info['max_len']} items")

        if info["examples"]:
            examples = [f"`{e}`" for e in info["examples"]]
            lines.append(f"- **Exemplos:** {', '.join(examples)}")

        lines.append("")
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Uso: python json_translator.py <arquivo.json> [saida.md]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = (
        sys.argv[2] if len(sys.argv) > 2 else json_path.rsplit(".", 1)[0] + "_schema.md"
    )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{json_path}' não encontrado")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido - {e}")
        sys.exit(1)

    translator = JSONTranslator(max_examples=3)
    translator.analyze(data)
    report = translator.generate_report(json_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Relatório gerado: {output_path}")


if __name__ == "__main__":
    main()
