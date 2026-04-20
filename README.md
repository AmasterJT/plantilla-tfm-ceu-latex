# plantilla-tfm-ceu-latex
Plantilla hecha en latex para la realización del TFM del Master en Ciberseguridad


```txt
Capítulo 1: Introducción
  1.1 Contexto del TFM
  1.2 Objetivos
  1.3 Organización del trabajo

Capítulo 2: Gestión del proyecto
  2.1 Modelo de ciclo de vida
  2.2 Planificación
  2.3 Presupuesto (si procede)

Capítulo 3: Análisis
  3.1 Especificación de requisitos
  3.2 Análisis de los Casos de Uso
  3.3 Análisis de seguridad
  3.4 Análisis desde la perspectiva del RGPD (si procede)

Capítulo 4: Diseño e implementación
  4.1 Arquitectura del sistema
    4.1.1 Arquitectura física
    4.1.2 Arquitectura lógica
    4.1.3 Diagrama de infraestructuras de nivel 2 (si procede)
    4.1.4 Diagrama de infraestructuras de nivel 3 (si procede)
  4.2 Diseño de datos
    4.2.1 Migración y carga inicial de datos (si procede)
  4.3 Diseño de la interfaz de usuario
  4.4 Diagrama de clases
  4.5 Entorno de construcción
  4.6 Referencia al repositorio de software

Capítulo 5: Validación del sistema
  5.1 Plan de pruebas
  5.2 Evaluación del sistema (si procede)

Capítulo 6: Implementación
  6.1 Conclusiones
  6.2 Líneas futuras

```

```yaml
capitulos:
  - titulo: "Introducción"
    secciones:
      - "Contexto del TFM"
      - "Objetivos"
      - "Organización del trabajo"

  - titulo: "Gestión del proyecto"
    secciones:
      - "Modelo de ciclo de vida"
      - "Planificación"
      - "Presupuesto (si procede)"

  - titulo: "Análisis"
    secciones:
      - "Especificación de requisitos"
      - "Análisis de los Casos de Uso"
      - "Análisis de seguridad"
      - "Análisis desde la perspectiva del RGPD (si procede)"

  - titulo: "Diseño e implementación"
    secciones:
      - titulo: "Arquitectura del sistema"
        subsecciones:
          - "Arquitectura física"
          - "Arquitectura lógica"
          - "Diagrama de infraestructuras de nivel 2 (si procede)"
          - "Diagrama de infraestructuras de nivel 3 (si procede)"
      - titulo: "Diseño de datos"
        subsecciones:
          - "Migración y carga inicial de datos (si procede)"
      - "Diseño de la interfaz de usuario"
      - "Diagrama de clases"
      - "Entorno de construcción"
      - "Referencia al repositorio de software"

  - titulo: "Validación del sistema"
    secciones:
      - "Plan de pruebas"
      - "Evaluación del sistema (si procede)"

  - titulo: "Implementación"
    secciones:
      - "Conclusiones"
      - "Líneas futuras"
```


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
    },
    {
      "titulo": "Gestión del proyecto",
      "secciones": [
        "Modelo de ciclo de vida",
        "Planificación",
        "Presupuesto (si procede)"
      ]
    },
    {
      "titulo": "Análisis",
      "secciones": [
        "Especificación de requisitos",
        "Análisis de los Casos de Uso",
        "Análisis de seguridad",
        "Análisis desde la perspectiva del RGPD (si procede)"
      ]
    },
    {
      "titulo": "Diseño e implementación",
      "secciones": [
        {
          "titulo": "Arquitectura del sistema",
          "subsecciones": [
            "Arquitectura física",
            "Arquitectura lógica",
            "Diagrama de infraestructuras de nivel 2 (si procede)",
            "Diagrama de infraestructuras de nivel 3 (si procede)"
          ]
        },
        {
          "titulo": "Diseño de datos",
          "subsecciones": [
            "Migración y carga inicial de datos (si procede)"
          ]
        },
        "Diseño de la interfaz de usuario",
        "Diagrama de clases",
        "Entorno de construcción",
        "Referencia al repositorio de software"
      ]
    },
    {
      "titulo": "Validación del sistema",
      "secciones": [
        "Plan de pruebas",
        "Evaluación del sistema (si procede)"
      ]
    },
    {
      "titulo": "Implementación",
      "secciones": [
        "Conclusiones",
        "Líneas futuras"
      ]
    }
  ]
}
```


```toml
[[capitulos]]
titulo = "Introducción"
secciones = [
  "Contexto del TFM",
  "Objetivos",
  "Organización del trabajo"
]

[[capitulos]]
titulo = "Gestión del proyecto"
secciones = [
  "Modelo de ciclo de vida",
  "Planificación",
  "Presupuesto (si procede)"
]

[[capitulos]]
titulo = "Análisis"
secciones = [
  "Especificación de requisitos",
  "Análisis de los Casos de Uso",
  "Análisis de seguridad",
  "Análisis desde la perspectiva del RGPD (si procede)"
]

[[capitulos]]
titulo = "Diseño e implementación"

[[capitulos.secciones]]
titulo = "Arquitectura del sistema"
subsecciones = [
  "Arquitectura física",
  "Arquitectura lógica",
  "Diagrama de infraestructuras de nivel 2 (si procede)",
  "Diagrama de infraestructuras de nivel 3 (si procede)"
]

[[capitulos.secciones]]
titulo = "Diseño de datos"
subsecciones = [
  "Migración y carga inicial de datos (si procede)"
]

[[capitulos.secciones]]
titulo = "Otros"
items = [
  "Diseño de la interfaz de usuario",
  "Diagrama de clases",
  "Entorno de construcción",
  "Referencia al repositorio de software"
]

[[capitulos]]
titulo = "Validación del sistema"
secciones = [
  "Plan de pruebas",
  "Evaluación del sistema (si procede)"
]

[[capitulos]]
titulo = "Implementación"
secciones = [
  "Conclusiones",
  "Líneas futuras"
]
```