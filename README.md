# Plantilla TFM CEU en LaTeX

Plantilla modular en LaTeX para redactar un **Trabajo Fin de Máster (TFM)**, con soporte para:

- portada personalizada
- resumen y abstract
- índice de contenidos, figuras y tablas
- capítulos y anexos modulares
- bibliografía con `biblatex` + `biber`
- glosario y siglas
- bloques de código con `listings`
- generación automática de capítulos y anexos a partir de un índice estructurado

El proyecto está organizado para que la mayor parte del contenido se escriba en ficheros independientes dentro de `Cuerpo/`, mientras que `main.tex` actúa como documento orquestador.

---

## Estructura del proyecto

```text
C:.
│   .gitignore
│   generar_capitulos_latex.py
│   indice.json
│   main.pdf
│   main.tex
│   main2.tex.bak
│   README.md
│
├───Bibliografia
│       bibliografia.bib
│       IEEEtraN.bst
│
├───Cuerpo
│       00_Resumen_Abstract.aux.bak
│       00_Resumen_Abstract.tex.bak
│       01_introduccion.aux.bak
│       01_introduccion.tex.bak
│       02_gestion_del_proyecto.aux.bak
│       02_gestion_del_proyecto.tex.bak
│       03_analisis.aux.bak
│       03_analisis.tex.bak
│       04_diseno_e_implementacion.aux.bak
│       04_diseno_e_implementacion.tex.bak
│       05_validacion_del_sistema.aux.bak
│       05_validacion_del_sistema.tex.bak
│       06_implementacion.aux.bak
│       06_implementacion.tex.bak
│       07_aaaaaaaaaaaaa.aux.bak
│       anexo_ii_titulo_anexo_ii.aux.bak
│       anexo_ii_titulo_anexo_ii.tex.bak
│       anexo_i_manuales.tex.bak
│       anexo_i_manueales.aux.bak
│
├───Formatos
│       comandos.tex
│       Contenido.tex
│       Contenido_roman.tex
│       Cuerpo.tex
│       listings.tex
│
├───Glosario
│       glosario.tex
│
├───Imagenes
│       Imagen-ejemplo.png
│
├───Logo
│       CEU-Logo.png
│       CEU-Logo2.png
│
└───Portada
        Portada.tex
```

---

## Qué hace cada directorio

### `Bibliografia/`
Contiene los recursos bibliográficos del proyecto.

- `bibliografia.bib`: base de datos BibTeX/BibLaTeX con las referencias bibliográficas.
- `IEEEtraN.bst`: estilo bibliográfico heredado o auxiliar. En esta plantilla la bibliografía se gestiona principalmente con `biblatex`, pero este fichero puede mantenerse por compatibilidad o reutilización previa.

### `Cuerpo/`
Contiene los ficheros de contenido principal de la memoria.

Aquí se almacenan:
- el resumen
- los capítulos
- los anexos

En el árbol mostrado aparecen sobre todo copias `.bak`, lo que indica que se han conservado respaldos de versiones anteriores. El script `generar_capitulos_latex.py` genera los `.tex` nuevos en esta carpeta y **no elimina** los `.bak`.

Ejemplos de uso esperado:
- `00_Resumen_Abstract.tex`
- `01_introduccion.tex`
- `02_gestion_del_proyecto.tex`
- `anexo_i_manuales.tex`

### `Formatos/`
Agrupa la configuración visual y funcional reutilizable del documento.

- `comandos.tex`: macros personalizadas del proyecto.
- `Contenido.tex`: configuración del índice principal en numeración arábiga.
- `Contenido_roman.tex`: configuración para índices o preliminares en numeración romana.
- `Cuerpo.tex`: estilo del cuerpo principal del documento.
- `listings.tex`: configuración de bloques de código y lenguajes personalizados.

### `Glosario/`
Incluye la definición del glosario de términos y del glosario de siglas.

- `glosario.tex`: define entradas de glosario y acrónimos, y además imprime ambas secciones.

### `Imagenes/`
Directorio para imágenes generales del contenido.

- `Imagen-ejemplo.png`: imagen de ejemplo o placeholder.

### `Logo/`
Recursos gráficos institucionales.

- `CEU-Logo.png`
- `CEU-Logo2.png`

Se suelen usar en portada o cabeceras, según la configuración del documento.

### `Portada/`
Contiene la lógica de la portada.

- `Portada.tex`: define el comando `\printportada{...}` y la maquetación de la cubierta.

---

## Qué hace cada fichero principal en la raíz

### `.gitignore`
Define qué ficheros no se suben al repositorio. Es útil para ignorar:
- ficheros auxiliares de compilación de LaTeX (`.aux`, `.log`, `.out`, etc.)
- PDFs generados
- ficheros temporales

### `main.tex`
Es el fichero principal del proyecto. Carga paquetes, configura el documento e incluye los distintos bloques del TFM.

### `main.pdf`
PDF compilado final o una versión de salida actual del documento.

### `main2.tex.bak`
Copia de seguridad de una versión anterior del documento principal.

### `indice.json`
Índice estructurado de ejemplo para alimentar el script de generación automática de capítulos y anexos.

### `generar_capitulos_latex.py`
Script en Python que genera automáticamente los capítulos y anexos en `Cuerpo/` y actualiza `main.tex`.

### `README.md`
Documentación del proyecto.

---

## Ficheros más importantes

## `main.tex`

`main.tex` es el núcleo del proyecto. Su función es coordinar todas las partes del documento.

### Qué hace

- define la clase del documento
- carga paquetes de idioma, tipografía, geometría y estilo
- configura colores, captions e hipervínculos
- carga los ficheros modulares de configuración:
  - `Formatos/listings`
  - `Formatos/comandos`
  - `Portada/Portada`
  - `Formatos/Cuerpo`
- genera la portada
- incluye el resumen
- construye índices
- incluye los capítulos
- imprime la bibliografía
- incluye los anexos
- genera el glosario

### Flujo general del documento

1. **Preámbulo**
   - paquetes
   - colores
   - bibliografía
   - comandos personalizados

2. **Portada**
   - `\printportada{...}`

3. **Preliminares**
   - numeración romana
   - resumen
   - índice, lista de figuras, lista de tablas

4. **Cuerpo principal**
   - numeración arábiga
   - capítulos incluidos desde `Cuerpo/`

5. **Bibliografía**

6. **Anexos**

7. **Glosario**

### Observaciones sobre el `main.tex` actual

Actualmente el fichero incluye alguna redundancia heredada, por ejemplo:

- `\usepackage{xcolor}` aparece dos veces
- `\usepackage{listings}` aparece dos veces

No impide necesariamente compilar, pero conviene limpiarlo para mantener el preámbulo más claro.

---

## `generar_capitulos_latex.py`

Este script automatiza la creación de capítulos y anexos.

### Qué hace

- lee un índice en formato:
  - `txt`
  - `yaml`
  - `json`
  - `toml`
- normaliza la estructura interna
- genera los ficheros `.tex` de los capítulos
- genera los ficheros `.tex` de los anexos
- actualiza automáticamente `main.tex` en dos bloques:
  - bloque de capítulos
  - bloque de anexos
- elimina los `.tex` previos de `Cuerpo/`, excepto:
  - `00_Resumen_Abstract.tex`
- no elimina ficheros `.bak`

### Formatos generados

#### Capítulos
```text
01_introduccion.tex
02_gestion_del_proyecto.tex
03_analisis.tex
```

#### Anexos
```text
anexo_i_codigo_fuente_si_procede.tex
anexo_ii_documentacion_de_usuario_si_procede.tex
anexo_iii_documentacion_tecnica_si_procede.tex
```

### Qué actualiza en `main.tex`

#### Bloque del cuerpo
Entre:

```latex
% =========================================================
% CUERPO DEL TRABAJO (estructura solicitada)
% =========================================================
```

y:

```latex
% BIBLIOGRAFÍA
```

#### Bloque de anexos
Entre:

```latex
% =========================================================
% ANEXOS
% =========================================================
```

y:

```latex
% GLOSARIO
```

---

## `glosario.tex`

Este fichero define y muestra el glosario del documento.

### Qué contiene

- entradas de términos:
  - `backend`
  - `framework`
  - `resultset`
  - `jdbc`

- acrónimos:
  - `WMS`
  - `API`
  - `REST`
  - `ERP`

### Qué imprime

- una sección de **Glosario de siglas**
- una sección de **Definiciones**

### Ventaja
Permite centralizar todas las definiciones terminológicas del proyecto en un único punto.

---

## Cómo se usa el proyecto

## Requisitos

### LaTeX
Se recomienda compilar con **XeLaTeX** o **LuaLaTeX**, porque el proyecto usa `fontspec`.

### Bibliografía
La bibliografía se genera con **biber**.

### Python
Para usar el script generador necesitas Python 3.

### Dependencias Python opcionales
- YAML:
  ```bash
  pip install pyyaml
  ```
- TOML en Python < 3.11:
  ```bash
  pip install tomli
  ```

---

## Flujo de trabajo recomendado

### 1. Editar la portada
En `main.tex`, ajusta esta línea:

```latex
\printportada{Titulo en español}{Nombre del autor}{Nombre del tutor}{Julio, 2026}{TÍTULO en inglés}
```

### 2. Editar el resumen
Crea o modifica:

```text
Cuerpo/00_Resumen_Abstract.tex
```

### 3. Definir el índice estructurado
Por ejemplo en `indice.json`:

```json
{
  "capitulos": [
    {
      "titulo": "Introducción",
      "secciones": [
        "Contexto del TFM",
        "Objetivos",
        "Organización del trabajo"
      ]
    }
  ],
  "Anexos": [
    "Anexo i: Código fuente (si procede)"
  ]
}
```

### 4. Ejecutar el generador
```bash
python generar_capitulos_latex.py indice.json
```

También admite:

```bash
python generar_capitulos_latex.py indice.yaml
python generar_capitulos_latex.py indice.toml
python generar_capitulos_latex.py indice.txt
```

### 5. Rellenar el contenido de cada capítulo y anexo
El script crea la estructura base, pero después hay que escribir el contenido real dentro de cada fichero generado.

### 6. Compilar el documento
Secuencia típica:

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

Si usas LuaLaTeX:

```bash
lualatex main.tex
biber main
lualatex main.tex
lualatex main.tex
```

---

## Ejemplos de índice soportados

## TXT
```txt
Capítulo 1: Introducción
  1.1 Contexto del TFM
  1.2 Objetivos

Capítulo 2: Análisis
  2.1 Requisitos

Anexos
  Anexo i: Código fuente (si procede)
  Anexo ii: Documentación de usuario (si procede)
```

## YAML
```yaml
capitulos:
  - titulo: "Introducción"
    secciones:
      - "Contexto del TFM"
      - "Objetivos"

Anexos:
  - "Anexo i: Código fuente (si procede)"
  - "Anexo ii: Documentación de usuario (si procede)"
```

## JSON
```json
{
  "capitulos": [
    {
      "titulo": "Introducción",
      "secciones": [
        "Contexto del TFM",
        "Objetivos"
      ]
    }
  ],
  "Anexos": [
    "Anexo i: Código fuente (si procede)",
    "Anexo ii: Documentación de usuario (si procede)"
  ]
}
```

## TOML
```toml
[[capitulos]]
titulo = "Introducción"
secciones = [
  "Contexto del TFM",
  "Objetivos"
]

Anexos = [
  "Anexo i: Código fuente (si procede)",
  "Anexo ii: Documentación de usuario (si procede)"
]
```

---

## Personalizaciones posibles

## 1. Portada
Se puede personalizar desde:
- `Portada/Portada.tex`
- la llamada a `\printportada{...}` en `main.tex`

## 2. Tipografías
En `main.tex`:

```latex
\setmainfont{Times New Roman}
\setmonofont{Arial}

ewfontfamily\calibribody{Calibri}
```

Puedes adaptar las fuentes a las exigencias de tu centro.

## 3. Márgenes y geometría
En `main.tex`:

```latex
\geometry{
  a4paper,
  inner=30mm,
  outer=30mm,
  top=35mm,
  bottom=30mm,
  headheight=45pt,
  headsep=8pt
}
```

## 4. Estilo del cuerpo
En `Formatos/Cuerpo.tex` puedes cambiar:
- estilo de capítulos
- estilo de subsecciones
- cabeceras y pies
- espacios antes y después de títulos

## 5. Comandos personalizados
En `Formatos/comandos.tex` puedes centralizar:
- comandos de citas
- comandos de enlaces
- macros reutilizables
- cabeceras personalizadas

## 6. Bloques de código
En `Formatos/listings.tex` puedes definir:
- lenguajes nuevos
- colores
- estilos
- numeración de líneas

## 7. Glosario y siglas
En `Glosario/glosario.tex` puedes añadir:
- términos
- siglas
- definiciones técnicas del proyecto

## 8. Estructura automática
Puedes cambiar la estructura completa del TFM modificando solo el fichero índice y relanzando:

```bash
python generar_capitulos_latex.py indice.json
```

---

## Qué hace `Cuerpo.tex`

`Formatos/Cuerpo.tex` define la apariencia del cuerpo principal de la memoria.

Normalmente ahí se controla:

- cabeceras y pies de página
- estilo de `\section`
- estilo de `\subsection`
- estilo de `\subsubsection`
- espaciado vertical
- aspecto de captions

Es el fichero indicado para personalizar cómo se ve la parte principal del TFM sin tocar el preámbulo global.

---

## Recomendaciones

- Mantén `main.tex` como fichero de orquestación y evita meter contenido largo directamente ahí.
- Escribe el contenido en `Cuerpo/`.
- Guarda una copia del índice estructurado para poder regenerar la plantilla rápidamente.
- No edites a mano los bloques de includes si vas a usar el script, porque se sobrescriben.
- Conserva los `.bak` si quieres histórico de cambios.

---

## Posibles mejoras futuras

- limpieza automática de duplicados en `main.tex`
- validación adicional de índices TOML mixtos
- generación opcional de anexos desde plantillas enriquecidas
- soporte para más formatos de entrada
- plantillas alternativas de portada o estilos de universidad

---

## Licencia / uso

Ajusta este apartado según cómo quieras distribuir la plantilla:
- uso personal
- uso académico interno
- licencia abierta
- repositorio privado

Si no tienes una licencia definida todavía, conviene añadirla antes de compartir el proyecto públicamente.
