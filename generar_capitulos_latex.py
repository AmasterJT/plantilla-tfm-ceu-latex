#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Genera los ficheros LaTeX de la carpeta Cuerpo a partir de un índice en TXT, YAML, JSON o TOML.

Uso:
    python generar_capitulos_latex.py indice.yaml
    python generar_capitulos_latex.py indice.json
    python generar_capitulos_latex.py indice.toml
    python generar_capitulos_latex.py indice.txt

Opciones:
    --project-root RUTA   Ruta raíz del proyecto LaTeX. Por defecto: carpeta actual
    --body-dir NOMBRE     Carpeta donde se crean los capítulos. Por defecto: Cuerpo
    --encoding ENC        Codificación del índice. Por defecto: utf-8

Requisitos:
    - YAML: pip install pyyaml
    - TOML en Python < 3.11: pip install tomli

Estructura esperada para YAML/JSON/TOML:
{
  "capitulos": [
    {
      "titulo": "Introducción",
      "secciones": [
        "Contexto del TFM",
        "Objetivos",
        {
          "titulo": "Arquitectura del sistema",
          "subsecciones": [
            "Arquitectura física",
            "Arquitectura lógica"
          ]
        }
      ]
    }
  ]
}

Formato TXT soportado:
Capítulo 1: Introducción
  1.1 Contexto del TFM
  1.2 Objetivos
Capítulo 2: Diseño e implementación
  2.1 Arquitectura del sistema
    2.1.1 Arquitectura física
    2.1.2 Arquitectura lógica

Notas:
- El fichero 00_Resumen_Abstract.tex no se toca.
- Cada capítulo se genera como:
    <NN>_<titulo_en_snake_case>.tex
- Las secciones simples se escriben como \\subsection{...}
- Las secciones con subsecciones se escriben como:
    \\subsection{...}
    \\subsubsection{...}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Para leer YAML necesitas instalar PyYAML: pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("El YAML debe tener un objeto raíz con la clave 'capitulos'.")
    return data


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("El JSON debe tener un objeto raíz con la clave 'capitulos'.")
    return data


def load_toml(path: Path) -> Dict[str, Any]:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        try:
            import tomli as tomllib  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Para leer TOML con Python < 3.11 necesitas instalar tomli: pip install tomli"
            ) from exc

    with path.open("rb") as f:
        data = tomllib.load(f)

    if not isinstance(data, dict):
        raise ValueError("El TOML debe tener un objeto raíz con la clave 'capitulos'.")
    return data


def strip_numeric_prefix(text: str) -> str:
    """
    Elimina prefijos como:
      - 'Capítulo 1: '
      - 'Capítulo 2 '
      - '1.1 '
      - '4.1.3 '
    """
    text = text.strip()

    m = re.match(r"^Cap[ií]tulo\s+\d+\s*[:.-]?\s*(.+)$", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    m = re.match(r"^\d+(?:\.\d+)*\.?\s+(.+)$", text)
    if m:
        return m.group(1).strip()

    return text


def load_txt(path: Path) -> Dict[str, Any]:
    """
    Parser sencillo basado en indentación.

    Reglas:
    - Sin indentación: nuevo capítulo
    - 2 espacios o 1 tab: sección
    - 4 espacios o 2 tabs: subsección

    También elimina prefijos numéricos tipo '1.1', '4.1.2' y 'Capítulo 3:'.
    """
    with path.open("r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    lines = [line.rstrip("\n\r") for line in raw_lines if line.strip()]

    capitulos: List[Dict[str, Any]] = []
    current_chapter: Dict[str, Any] | None = None
    current_section_obj: Dict[str, Any] | None = None

    for raw in lines:
        expanded = raw.replace("\t", "    ")
        indent = len(expanded) - len(expanded.lstrip(" "))
        content = expanded.strip()

        # Ignorar líneas claramente ajenas al índice
        lowered = content.lower()
        if lowered.startswith("listado de rutas") or lowered.startswith("el n"):
            continue

        text = strip_numeric_prefix(content)

        if indent == 0:
            current_chapter = {"titulo": text, "secciones": []}
            capitulos.append(current_chapter)
            current_section_obj = None

        elif indent in (2, 4):
            if current_chapter is None:
                raise ValueError(
                    f"Se encontró una sección fuera de un capítulo: '{content}'"
                )

            # sección simple, todavía sin saber si tendrá subsubsecciones
            current_section_obj = {"titulo": text, "subsecciones": []}
            current_chapter["secciones"].append(current_section_obj)

        elif indent >= 6:
            if current_section_obj is None:
                raise ValueError(
                    f"Se encontró una subsección fuera de una sección: '{content}'"
                )
            current_section_obj["subsecciones"].append(text)

        else:
            # fallback conservador por si la indentación es irregular
            if current_chapter is None:
                current_chapter = {"titulo": text, "secciones": []}
                capitulos.append(current_chapter)
                current_section_obj = None
            else:
                current_section_obj = {"titulo": text, "subsecciones": []}
                current_chapter["secciones"].append(current_section_obj)

    return {"capitulos": capitulos}


def normalize_structure(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "capitulos" not in data:
        raise ValueError("Falta la clave raíz 'capitulos'.")

    capitulos = data["capitulos"]
    if not isinstance(capitulos, list):
        raise ValueError("'capitulos' debe ser una lista.")

    normalized: List[Dict[str, Any]] = []

    for i, cap in enumerate(capitulos, start=1):
        if not isinstance(cap, dict):
            raise ValueError(f"El capítulo {i} debe ser un objeto.")

        titulo = cap.get("titulo")
        secciones = cap.get("secciones", [])

        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError(f"El capítulo {i} debe tener un 'titulo' no vacío.")

        if not isinstance(secciones, list):
            raise ValueError(f"Las 'secciones' del capítulo '{titulo}' deben ser una lista.")

        norm_sections: List[Dict[str, Any]] = []
        for j, sec in enumerate(secciones, start=1):
            if isinstance(sec, str):
                norm_sections.append({
                    "titulo": sec.strip(),
                    "subsecciones": []
                })
            elif isinstance(sec, dict):
                sec_titulo = sec.get("titulo")
                subsecciones = sec.get("subsecciones", [])

                if not isinstance(sec_titulo, str) or not sec_titulo.strip():
                    raise ValueError(
                        f"La sección {j} del capítulo '{titulo}' debe tener un 'titulo' no vacío."
                    )
                if not isinstance(subsecciones, list):
                    raise ValueError(
                        f"'subsecciones' de '{sec_titulo}' debe ser una lista."
                    )

                clean_subsections = []
                for sub in subsecciones:
                    if not isinstance(sub, str) or not sub.strip():
                        raise ValueError(
                            f"Las subsecciones de '{sec_titulo}' deben ser strings no vacíos."
                        )
                    clean_subsections.append(sub.strip())

                norm_sections.append({
                    "titulo": sec_titulo.strip(),
                    "subsecciones": clean_subsections
                })
            else:
                raise ValueError(
                    f"La sección {j} del capítulo '{titulo}' debe ser string u objeto."
                )

        normalized.append({
            "titulo": titulo.strip(),
            "secciones": norm_sections
        })

    return normalized


def slugify_snake_case(text: str) -> str:
    text = text.strip().lower()

    # quitar acentos
    text = "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )

    # ñ ya cae como n con NFKD, pero dejamos el flujo genérico
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[-\s]+", "_", text).strip("_")
    text = re.sub(r"_+", "_", text)

    if not text:
        return "capitulo"

    return text


def label_slug(text: str) -> str:
    """
    Para \\label{sec:...} uso snake_case ASCII para evitar problemas.
    """
    return slugify_snake_case(text)


def chapter_filename(index_1_based: int, title: str) -> str:
    return f"{index_1_based:02d}_{slugify_snake_case(title)}.tex"


def render_chapter_tex(title: str, sections: List[Dict[str, Any]]) -> str:
    parts: List[str] = []

    parts.append(r"\vspace*{-1cm}")
    parts.append("")
    parts.append(rf"\nombreCapituloCabecera{{RH}}{{{title}}} % Título de la sección en la cabecera")
    parts.append("")
    parts.append(rf"\section{{{title}}} % Título del capítulo")
    parts.append(rf"\label{{sec:{label_slug(title)}}}")
    parts.append("")
    parts.append("% ---------------------------------------------------")
    parts.append("")

    for idx, sec in enumerate(sections):
        parts.append(rf"\subsection{{{sec['titulo']}}}")
        if sec["subsecciones"]:
            for sub in sec["subsecciones"]:
                parts.append("")
                parts.append(rf"\subsubsection{{{sub}}}")
        if idx != len(sections) - 1:
            parts.append("")
    parts.append("")

    return "\n".join(parts)


def load_index(path: Path) -> Dict[str, Any]:
    suffix = path.suffix.lower()

    if suffix in {".yaml", ".yml"}:
        return load_yaml(path)
    if suffix == ".json":
        return load_json(path)
    if suffix == ".toml":
        return load_toml(path)
    if suffix == ".txt":
        return load_txt(path)

    raise ValueError(
        f"Formato no soportado: {suffix}. Usa TXT, YAML, JSON o TOML."
    )


def ensure_project_layout(project_root: Path, body_dir_name: str) -> Path:
    main_tex = project_root / "main.tex"
    body_dir = project_root / body_dir_name

    if not main_tex.exists():
        raise FileNotFoundError(
            f"No se ha encontrado '{main_tex}'. Ejecuta el script en la raíz del proyecto "
            "o usa --project-root."
        )

    if not body_dir.exists():
        raise FileNotFoundError(
            f"No se ha encontrado la carpeta '{body_dir}'."
        )

    if not body_dir.is_dir():
        raise NotADirectoryError(f"'{body_dir}' existe pero no es una carpeta.")

    resumen = body_dir / "00_Resumen_Abstract.tex"
    if not resumen.exists():
        print(
            "Aviso: no existe '00_Resumen_Abstract.tex' en la carpeta Cuerpo. "
            "No se creará ni se modificará automáticamente.",
            file=sys.stderr,
        )

    return body_dir


def generate_files(index_data: List[Dict[str, Any]], body_dir: Path) -> List[Path]:
    created: List[Path] = []

    for i, chapter in enumerate(index_data, start=1):
        filename = chapter_filename(i, chapter["titulo"])
        target = body_dir / filename
        content = render_chapter_tex(chapter["titulo"], chapter["secciones"])
        target.write_text(content, encoding="utf-8", newline="\n")
        created.append(target)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera capítulos LaTeX a partir de un índice estructurado."
    )
    parser.add_argument("index_file", help="Ruta al índice (.txt, .yaml, .json, .toml)")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Raíz del proyecto LaTeX (por defecto: carpeta actual)",
    )
    parser.add_argument(
        "--body-dir",
        default="Cuerpo",
        help="Nombre de la carpeta donde crear los capítulos (por defecto: Cuerpo)",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Codificación del fichero de índice (actualmente informativa; por defecto: utf-8)",
    )

    args = parser.parse_args()

    try:
        index_path = Path(args.index_file).resolve()
        project_root = Path(args.project_root).resolve()

        if not index_path.exists():
            raise FileNotFoundError(f"No existe el fichero de índice: {index_path}")

        body_dir = ensure_project_layout(project_root, args.body_dir)

        raw_data = load_index(index_path)
        normalized = normalize_structure(raw_data)
        created = generate_files(normalized, body_dir)

        print("Ficheros generados:")
        for p in created:
            print(f" - {p}")
        print("")
        print("Nota: 00_Resumen_Abstract.tex no se modifica.")

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
