# Participación Ciudadana INE · Dashboard

## Descripción

Dashboard interactivo en **Streamlit** para explorar la participación ciudadana en México:

- **Elección judicial 2024‑2025:** mapa de México coloreado según la participación de cada estado, con un panel de datos al seleccionar uno.
- **Elecciones federales 2009‑2024:** evolución de la participación por estado y por municipio, con desglose por **sexo**, **edad** y **tipo de sección** (urbana, mixta, rural), comparada contra el promedio nacional o estatal.
- **Reportes PDF:** infografía descargable a nivel nacional, estatal o municipal.

**Cálculo de participación:**

```
Participación = Votaron / (Votaron + No votaron) × 100
```

Los *no especificados* (cuadernillo no disponible) no entran en el cálculo. Los totales nacionales y estatales se obtienen sumando conteos, no promediando porcentajes. No incluye casillas especiales ni voto desde el extranjero.

**Fuente:** Instituto Nacional Electoral (INE): Conteos Censales de Participación Ciudadana y Participación en la Elección del Poder Judicial 2024‑2025.

## Versión

`1.0.0`

## Important changes

### Initial version (1.0.0)

- Mapa de participación de la elección judicial por estado (GeoJSON + Plotly).
- Panel lateral con datos generales del estado y sparkline de su evolución federal.
- Vista de evolución 2009‑2024 con gráfica interactiva: clic en un año para ver su detalle.
- Desglose por sexo, edad y tipo de sección, con íconos ⓘ explicativos.
- Selector de municipio con buscador.
- Reporte PDF tipo infografía (nacional, estatal y municipal).
- Script `summarize_counts` que reduce ~3,5 GB de Conteos Censales a dos CSV de resumen.
- Diseño responsive (escritorio y celular).

## Last modification

28/10/2026

## To do

### End points

La app no expone una API; sus "puntos de entrada" son las vistas de Streamlit, controladas con `st.session_state["vista"]`:

| Vista | Estado | Descripción |
|---|---|---|
| `mapa` | ✅ Listo | Mapa judicial + panel del estado seleccionado |
| `evolucion` | ✅ Listo | Detalle 2009‑2024 por estado o municipio |
| Descarga PDF | ✅ Listo | Reporte nacional, estatal o municipal |
| Mapa municipal | ⬜ Pendiente | Mapa coloreado por municipio (GeoJSON de municipios) |

### Pendientes

- [ ] Pruebas unitarias en `tests/` (por ejemplo, que los municipios sumen el total de su estado).
- [ ] Centralizar la fórmula de participación en un solo módulo.

## Guía de configuración

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/MrRobot437/ws-ine-hackathon-prueba.git
cd ws-ine-hackathon-prueba
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

### 2. Configuración central

Toda la configuración está en `src/constants.py`:

| Constante | Para qué sirve |
|---|---|
| `ORIGIN_DATA`, `DESTINO`, `DESTINO_MUNICIPIOS`, `CSV_*`, `GEOJSON` | Rutas de los archivos de datos |
| `COLORS_MAP`, `LINE_COLOR` | Paleta de colores (mapa, gráficas y PDF) |
| `LOW`, `CENTER`, `HIGH` | Referencias de la escala de color del mapa |
| `YEARS`, `PRESIDENTIAL_YEARS` | Años de elección federal que se procesan |
| `GENDER_CATEGORIES`, `TYPES`, `AGES`, `NAME_AGE` | Códigos del INE y su traducción a etiquetas |
| `ORDEN_SEXO`, `ORDEN_EDAD`, `ORDEN_SECCION` | Orden en que se muestran las categorías |

### 3. (Opcional) Regenerar los resúmenes de Conteos Censales

El repositorio ya incluye `data/resumen/conteos_estado.csv` y `data/resumen/conteos_municipio.csv`. Solo hace falta si actualizas los datos originales:

1. Descarga los Conteos Censales del portal de Datos Abiertos del INE (2009, 2012, 2015, 2018, 2021, 2024).
2. Colócalos en `data/DatosAbiertos_DECEyEC_ConteosCensales{AÑO}/`.
3. Desde la raíz del proyecto ejecuta:

```bash
python -m src.summarize_counts
```

> Usa `python -m`: con `python src/summarize_counts.py` aparece `ModuleNotFoundError: No module named 'src'`.

## Cómo leer la nueva estructura (paquetes y nomenclatura)

```
ws_ine_hackathon/
├── app.py                      # Punto de entrada: alterna entre la vista "mapa" y "evolucion"
├── requirements.txt
├── data/
│   ├── explorar_mapa/          # Elección judicial por estado + GeoJSON de México
│   ├── datos_generales/        # Indicadores generales por estado
│   └── resumen/                # CSV generados por summarize_counts
├── src/                        # Paquete principal
│   ├── constants.py            # Configuración
│   ├── utils.py                # Utilidades compartidas (lectura de CSV, formato)
│   ├── map_participation.py    # Datos + figura del mapa
│   ├── general_data.py         # Datos generales por estado
│   ├── panel_general_info.py   # Vista: panel lateral
│   ├── summarize_counts.py     # Script de preprocesamiento (no corre en Streamlit)
│   ├── evolution_data.py       # Datos: series y años por estado/municipio
│   ├── evolution_view.py       # Vista: detalle de evolución
│   ├── report_data.py          # Datos: prepara el reporte
│   └── report_pdf.py           # Vista: dibuja el PDF
└── tests/
```

**Capas:**

```
constants / utils  →  *_data.py (calcula)  →  *_view.py / panel / report_pdf (dibuja)  →  app.py
```

- Los archivos `*_data.py` **solo calculan**: devuelven DataFrames, series o diccionarios, sin llamar a Streamlit.
- Los archivos de vista **solo dibujan**: reciben los datos ya calculados.

**Nomenclatura:**

- **Paquete:** `src/` tiene `__init__.py`; se importa como `from src.utils import read_csv`.
- **Archivos y funciones:** `snake_case`, mayormente en inglés (`state_series`, `build_report_data`).
- **Constantes:** `MAYÚSCULAS` en `constants.py`.
- **Prefijo `_`:** funciones de uso interno de su archivo (`_grafica`, `_info_anio`).
- **Keys de Streamlit:** con el contexto en el nombre para que no se repitan (`municipio_{estado}`, `spark_{estado}`, `info_sexo`).
- **Columnas de datos:** se conservan los nombres del INE (`EDOCVE`, `MPIOCVE`, `LN`, `SV`, `NV`, `NS`).
- **Textos visibles para el usuario:** en español.

## Built with

| Librería | Versión | Uso |
|---|---|---|
| [Streamlit](https://streamlit.io/) | 1.66.0 | Interfaz web |
| [pandas](https://pandas.pydata.org/) | 3.0.6 | Lectura y resumen de datos |
| [Plotly](https://plotly.com/python/) | 7.1.0 | Mapa y gráficas interactivas |
| [fpdf2](https://py-pdf.github.io/fpdf2/) | 2.8.9 | Reporte PDF |

## Prerequisites

- Python **3.12 o superior**
- pip
- Git

## Deployment (Cómo correrlo)

### Local

```bash
streamlit run app.py
```

Se abre en `http://localhost:8501`.

### Streamlit Community Cloud

1. Sube el repositorio a GitHub (debe ser público, o dar acceso a repositorios privados).
2. En [share.streamlit.io](https://share.streamlit.io): **Create app** → repositorio → rama `main` → archivo `app.py`.
3. En **Advanced settings**, elige Python 3.12 o 3.13.
4. Pulsa **Deploy**.

**Demo:** _(URL de la app desplegada)_