# Predicción de renuncias de empleados (IBM HR Analytics)

Trabajo final · **M71V/M72V 02 · Implementación de Modelos de Aprendizaje Automático** · UBA, Cohorte Septiembre 2025
Alumno: **Giovanni Raffo**

Un modelo que estima, para cada empleado, la probabilidad de que renuncie, y una API local que lo sirve. El dataset es el asignado por el profesor: *IBM HR Analytics Employee Attrition & Performance* (Kaggle), 1.470 empleados, 35 columnas, 16 % de renuncias.

## Entregas

| Entrega | Qué contiene | Abrir en Colab | Estado |
|---|---|---|---|
| 1. Preparación de los datos | `notebooks/01_datos.ipynb` | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gioaqp/attrition-uba/blob/main/notebooks/01_datos.ipynb) | lista |
| 2. Entrenamiento del modelo | `notebooks/02_modelo.ipynb` | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gioaqp/attrition-uba/blob/main/notebooks/02_modelo.ipynb) | lista |
| 3. Despliegue para consumo | `api/` y `notebooks/03_api_demo.ipynb` | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gioaqp/attrition-uba/blob/main/notebooks/03_api_demo.ipynb) | lista |

## Verlo sin instalar nada

- **Colab:** botón de la tabla y luego *Entorno de ejecución → Ejecutar todo*. La primera celda descarga este repositorio e instala lo necesario. Tarda alrededor de un minuto.
- **Solo leer:** `reports/01_datos.html`, `reports/02_modelo.html` y `reports/03_api_demo.html` son los cuadernos con todas sus salidas; `reports/eda_sweetviz.html` es el reporte automático de exploración.

## Correrlo en la computadora

Requiere [uv](https://docs.astral.sh/uv/). Desde la carpeta del proyecto:

```powershell
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Abrir los cuadernos con doble clic en `abrir_cuadernos.bat`, o ejecutarlos de punta a punta (el segundo vuelve a entrenar el modelo y regenera `models/`):

```powershell
.venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks\01_datos.ipynb
.venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks\02_modelo.ipynb
```

Quien use conda puede crear el entorno con `environment.yml`, que instala las mismas versiones.

## Estructura

```
attrition-uba/
├── data/                   dataset original y, en procesado/, el dataset final de la Entrega 1
├── notebooks/              un cuaderno por entrega
├── reports/                versiones HTML de los cuadernos y reporte Sweetviz
├── models/                 modelo_attrition.pkl (pipeline + modelo + punto de corte) y metricas.json
├── api/                    servicio de predicción (Entrega 3)
├── requirements.txt        versiones exactas del entorno
```

## Modelo

Regresión logística con pesos de clase (`class_weight="balanced"`), dentro del mismo pipeline de preparación de la Entrega 1. Ajustada por validación cruzada de 5 particiones sobre 12 configuraciones (mejor: C = 0,3, penalización L2, ROC-AUC 0,831). Punto de corte 0,40, elegido con predicciones de validación cruzada para detectar al menos 8 de cada 10 renuncias. El grupo de examen (294 empleados, 47 renuncias) se usó una sola vez.

## Métricas finales

Grupo de examen, comparado con el baseline que predice siempre "se queda":

| Métrica | Baseline | Modelo final |
|---|---|---|
| ROC-AUC | 0,50 | 0,81 |
| Recall (renuncias detectadas) | 0,00 | 0,79 (37 de 47) |
| Precisión | 0,00 | 0,34 |
| F1 | 0,00 | 0,47 |
| Exactitud | 0,84 | 0,72 |

Los valores exactos están en `models/metricas.json`.

## API

El servicio carga `models/modelo_attrition.pkl`, el mismo archivo que guardó la Entrega 2: trae adentro la receta de preparación, el modelo y el punto de corte, así que en producción los datos se transforman exactamente igual que en el entrenamiento. Se carga una sola vez al arrancar.

```powershell
.venv\Scripts\uvicorn api.app:app --reload
```

O, sin escribir nada: doble clic en `levantar_api.bat`, que levanta el servicio y abre la pantalla de demostración en el navegador. Se apaga cerrando la ventana negra.

| Ruta | Qué hace |
|---|---|
| `GET /health` | Dice si el servicio está vivo y si cargó el modelo. |
| `POST /predict` | Recibe los 29 datos de un empleado y devuelve `{"attrition": "Yes"/"No", "probabilidad": 0.99}`. |

Demo en el navegador: `http://127.0.0.1:8000/docs`. Los campos de texto solo aceptan los valores del dataset; cualquier otro devuelve error 422 antes de llegar al modelo.

Probar los tres empleados de ejemplo (`api/ejemplos.json`: riesgo alto, estable y de frontera) con el servicio levantado:

```powershell
.venv\Scripts\python api\probar_ejemplos.py
```

Una consulta suelta con `curl`, usando el empleado de `api/ejemplo.json`:

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @api/ejemplo.json
```

Respuesta: `{"attrition":"Yes","probabilidad":0.9877}`

`notebooks/03_api_demo.ipynb` hace todo lo anterior sin navegador: levanta el servicio, manda los tres ejemplos y lo apaga. Es la versión que corre en Colab.
