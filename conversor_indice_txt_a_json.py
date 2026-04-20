#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
from pathlib import Path


def clean_title(text: str) -> str:
    """Elimina prefijos de capítulo, numeración y anexo."""
    text = text.strip()

    m = re.match(r"^Cap[ií]tulo\s+\d+\s*[:.-]?\s*(.+)$", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    m = re.match(r"^\d+(?:\.\d+)*\.?\s+(.+)$", text)
    if m:
        return m.group(1).strip()

    m = re.match(r"^Anexo\s+[ivxlcdm]+\s*[:\-–]\s*(.+)$", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    return text


def detect_numbering_level(text: str) -> int | None:
    """
    Devuelve:
    - 1 para capítulos tipo 'Capítulo 1: ...'
    - 2 para secciones tipo '4.1 ...'
    - 3 para subsecciones tipo '4.1.1 ...'
    - None si no detecta nivel
    """
    text = text.strip()

    if re.match(r"^Cap[ií]tulo\s+\d+\s*[:.-]?\s+.+$", text, flags=re.IGNORECASE):
        return 1

    m = re.match(r"^(\d+(?:\.\d+)+)\.?\s+.+$", text)
    if not m:
        return None

    numeric = m.group(1)
    parts = numeric.split(".")
    return len(parts)


def parse_txt_to_structure(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n\r") for line in f if line.strip()]

    capitulos = []
    anexos = []

    current_chapter = None
    current_section = None
    in_anexos = False

    for raw in lines:
        content = raw.strip()
        lowered = content.lower()

        if lowered.startswith("anexos"):
            in_anexos = True
            current_chapter = None
            current_section = None
            continue

        if in_anexos:
            if lowered.startswith("anexo "):
                anexos.append(clean_title(content))
            continue

        level = detect_numbering_level(content)

        # Capítulo
        if level == 1:
            current_chapter = {
                "titulo": clean_title(content),
                "secciones": []
            }
            capitulos.append(current_chapter)
            current_section = None
            continue

        # Sección
        if level == 2:
            if current_chapter is None:
                raise ValueError(f"Se encontró una sección fuera de un capítulo: '{content}'")

            current_section = {
                "titulo": clean_title(content),
                "subsecciones": []
            }
            current_chapter["secciones"].append(current_section)
            continue

        # Subsección
        if level == 3:
            if current_section is None:
                raise ValueError(f"Se encontró una subsección fuera de una sección: '{content}'")

            current_section["subsecciones"].append(clean_title(content))
            continue

        # Si no tiene patrón conocido, lo ignoramos o lanzamos error.
        # Aquí prefiero ignorar silenciosamente líneas no estructurales.
        continue

    # Normalizar: secciones sin hijos pasan a string
    for cap in capitulos:
        normalized_sections = []
        for sec in cap["secciones"]:
            if sec["subsecciones"]:
                normalized_sections.append(sec)
            else:
                normalized_sections.append(sec["titulo"])
        cap["secciones"] = normalized_sections

    return {
        "capitulos": capitulos,
        "Anexos": anexos
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convierte un índice TXT estructurado a JSON."
    )
    parser.add_argument(
        "input_file",
        help="Ruta al fichero de entrada .txt"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Ruta del JSON de salida. Si no se indica, se crea junto al TXT con extensión .json"
    )

    args = parser.parse_args()

    input_path = Path(args.input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el fichero de entrada: {input_path}")

    if input_path.suffix.lower() != ".txt":
        raise ValueError("El fichero de entrada debe tener extensión .txt")

    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix(".json")

    data = parse_txt_to_structure(input_path)

    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"JSON generado correctamente en: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())