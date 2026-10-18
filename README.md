# Modelo final de operación de la cuenca del Maule

Código computacional del modelo de operación de la cuenca del Maule y
evaluación de una nueva central en el nodo `B_Maule`.

Esta carpeta está preparada como entregable final. Contiene una sola corrida:
la realizada el 18-10-2026. El notebook fuente y el notebook ejecutado no son
dos corridas distintas:

Repositorio: https://github.com/Jerrazuriz/Capstone

- `Modelo_Final_Maule_revisado.ipynb` es el código fuente, sin depender de sus
  salidas guardadas.
- `resultados_corrida\Modelo_Final_Maule_revisado_ejecutado.ipynb` es una copia
  del mismo notebook después de ejecutar todas sus celdas; conserva las tablas,
  gráficos y mensajes de esa corrida como evidencia reproducible.

## Requisitos

- Windows 10/11.
- Python 3.11 (se usó Python 3.11.7).
- Las dependencias listadas en `requirements.txt`.
- Una licencia activa de Gurobi. La corrida registrada se realizó con
  Gurobi 13.0.3 y licencia académica.

El entorno que se utilizó ya tenía instalados los paquetes requeridos. En una
instalación nueva, se puede preparar un entorno virtual con:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La licencia de Gurobi debe estar configurada antes de ejecutar el notebook.
Por ejemplo, se puede instalar una licencia local con `grbgetkey` o definir
`GRB_LICENSE_FILE` apuntando a un archivo `gurobi.lic`. No se deben guardar
credenciales WLS dentro del notebook ni del repositorio.

## Estructura esperada

```text
.
├── Modelo_Final_Maule_revisado.ipynb
├── requirements.txt
├── data
│   ├── CaudalesHistoricos.xlsx
│   ├── Conectividad_Maule.xlsx
│   ├── plpbar.dat
│   ├── plpcnfce.dat
│   └── po12meses_jul26.xlsx
└── resultados_corrida
    ├── Modelo_Final_Maule_revisado_ejecutado.ipynb
    ├── resultados_modelo_final_maule.xlsx
    ├── resultados_65_anios.xlsx
    ├── RESUMEN_corrida.md
    ├── log_corrida.txt
    └── figures_informe
```

El notebook detecta automáticamente `data\` cuando se ejecuta desde la
carpeta raíz del proyecto. También mantiene compatibilidad con la ejecución en
Colab, donde los archivos pueden estar en la carpeta raíz.

## Ejecución reproducible

Abrir PowerShell en la carpeta que contiene este README y ejecutar:

```powershell
py -3.11 -m jupyter nbconvert --to notebook --execute `
  .\Modelo_Final_Maule_revisado.ipynb `
  --output .\resultados_corrida\Modelo_Final_Maule_revisado_ejecutado.ipynb `
  --ExecutePreprocessor.timeout=1800 `
  --ExecutePreprocessor.kernel_name=python3
```

El comando ejecuta todas las celdas y conserva sus salidas en una copia
ejecutada. El notebook fuente no se reemplaza. La corrida genera o actualiza:

- `resultados_corrida\resultados_modelo_final_maule.xlsx`: resultados de los
  escenarios, sensibilidades y comparaciones.
- `resultados_corrida\resultados_65_anios.xlsx`: resultados de la serie
  histórica de 65 años.
- `resultados_corrida\figures_informe\e2_*.pdf`: seis figuras para el informe.
- `resultados_corrida\log_corrida.txt`: salida textual completa de la corrida.
- `resultados_corrida\Modelo_Final_Maule_revisado_ejecutado.ipynb`: notebook
  con las celdas ejecutadas y sus resultados.

## Resultados principales

La corrida usa CMg medio y gasto de riego de `160 m³/s` en tres escenarios:

| Indicador | Húmedo 1992-93 | Medio 1973-74 | Seco 2010-11 |
|---|---:|---:|---:|
| Percentil de excedencia (`Pe`) | 19,7 % | 50,0 % | 89,4 % |
| Caudal medio en `B_Maule` | 132,0 m³/s | 95,1 m³/s | 68,2 m³/s |
| Caudal mínimo semanal | 70,9 m³/s | 58,5 m³/s | 42,3 m³/s |
| Energía | 11.378 GWh | 9.590 GWh | 6.657 GWh |
| Ingreso | 410,0 MUSD | 380,3 MUSD | 280,0 MUSD |
| Déficit de riego | 0 hm³ | 0 hm³ | 0 hm³ |
| Volumen final en `LMAULE` | 879,9 hm³ | 756,7 hm³ | 664,7 hm³ |

Para la serie completa de 65 años (1960-61 a 2024-25), el caudal medio en
`B_Maule` es `106,0 m³/s`, el ingreso medio es `356,8 MUSD` y el déficit de
riego es `0 hm³` en todos los años. El año mínimo es 1998-99
(`40,5 m³/s`) y el máximo es 1982-83 (`177,6 m³/s`).

Para la nueva central, usando `Qd = Q50 = 97,8 m³/s` y rendimiento supuesto
`η = 0,45`, el resultado para 65 años es:

- Potencia: `44,0 MW`.
- Generación: `325,8 GWh/año`.
- Ingreso: `11,0 MUSD/año`.
- Factor de planta: `0,85`.

## Verificación de la corrida

La ejecución local fue realizada el 18-10-2026 con Python 3.11.7,
`gurobipy 13.0.3` y licencia académica vigente. El notebook se ejecutó sin
errores después de corregir la detección de la carpeta local `data\`. La
salida completa y los tiempos por celda quedan registrados en
`resultados_corrida\log_corrida.txt`.

Los archivos de `resultados_corrida\` son exclusivamente productos de la
última ejecución y sirven para revisar tablas y figuras sin volver a resolver
el modelo. No se incluyen credenciales, archivos de licencia, entornos
virtuales, cachés ni copias de corridas anteriores.
