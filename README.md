# Modelo final de operación de la cuenca del Maule

Código computacional del modelo de operación de la cuenca del Maule y
evaluación de una nueva central en el nodo `B_Maule`.

Esta carpeta está preparada como entregable final del capstone. Contiene una
sola corrida, la del 25-11-2026 (ver *Verificación de la corrida*). El notebook
fuente y el notebook ejecutado no son dos corridas distintas:

Repositorio: https://github.com/Jerrazuriz/Capstone

- `Modelo_Final_Maule_C2_corregido.ipynb` es el código fuente, sin depender de sus
  salidas guardadas.
- `resultados_corrida\Modelo_Final_Maule_C2_corregido_ejecutado.ipynb` es una copia
  del mismo notebook después de ejecutar todas sus celdas; conserva las tablas,
  gráficos y mensajes de esa corrida como evidencia reproducible.

## Qué incluye la versión final

- **Modelo de operación** de la cuenca (48 semanas × 5 bloques, Convenio de 1947
  con la cuota C2 por año calendario) y verificación independiente de cada solución.
- **Caso base comparable** (sección 9): operación secuencial con objetivo
  semanal, con las mismas condiciones de borde que el modelo (`V_final ≥ V_inicial`
  y riego sin déficit). Reemplaza al miope puro de la entrega anterior, que no era
  comparable porque vaciaba la Laguna o dejaba riego sin cubrir.
- **Análisis de sensibilidad** (secciones 11a–11e): precios, gasto de riego,
  Convenio, condiciones de borde (condición terminal, valor del agua, volumen
  inicial, filtración, uso previo de la cuota) y políticas de operación, con un
  resumen por factor y gráfico tipo tornado.
- **Serie de 65 años** y **nueva central** en `B_Maule`, con sensibilidad de su
  ingreso a η, caudal de diseño, precios, hidrología y operación aguas arriba.
- **Ingreso potencial del caudal y período reciente** (sección 12d): KPI de
  ingreso = η · caudal promedio · CMg promedio · 8.760 h, por escenario, caso base,
  sin Convenio, sensibilidades y 65 años, con su validación bloque a bloque; y la
  comparación del registro completo con 1960-61 a 2009-10 y 2010-11 a 2024-25.

## Requisitos

- Windows 10/11.
- Python 3.11 (se usó Python 3.11.7).
- Las dependencias listadas en `requirements.txt`.
- Una licencia activa de Gurobi. La corrida registrada se realizó con
  Gurobi 13.0.3 y licencia académica. **Sin licencia** el notebook igual corre:
  la celda *Solver* (sección 0) detecta la licencia restringida de `pip`, exporta
  el mismo modelo a MPS y lo resuelve con HiGHS (`highspy`, incluido en
  `requirements.txt`), con los mismos caudales y volúmenes.

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
├── Modelo_Final_Maule_C2_corregido.ipynb
├── requirements.txt
├── data
│   ├── CaudalesHistoricos.xlsx
│   ├── Conectividad_Maule.xlsx
│   ├── plpbar.dat
│   ├── plpcnfce.dat
│   └── po12meses_jul26.xlsx
└── resultados_corrida
    ├── Modelo_Final_Maule_C2_corregido_ejecutado.ipynb
    ├── resultados_modelo_final_maule.xlsx
    ├── resultados_65_anios.xlsx
    ├── sensibilidades_borde.xlsx
    ├── ingreso_potencial_y_periodos.xlsx
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
  .\Modelo_Final_Maule_C2_corregido.ipynb `
  --output .\resultados_corrida\Modelo_Final_Maule_C2_corregido_ejecutado.ipynb `
  --ExecutePreprocessor.timeout=1800 `
  --ExecutePreprocessor.kernel_name=python3
```

El comando ejecuta todas las celdas y conserva sus salidas en una copia
ejecutada. El notebook fuente no se reemplaza. La corrida genera o actualiza:

- `resultados_corrida\resultados_modelo_final_maule.xlsx`: resultados de los
  escenarios, sensibilidades y comparaciones.
- `resultados_corrida\resultados_65_anios.xlsx`: resultados de la serie
  histórica de 65 años.
- `resultados_corrida\sensibilidades_borde.xlsx`: sensibilidades de la sección 11d
  (políticas de operación, condición terminal, valor del agua, volumen inicial de
  la Laguna, filtración, uso previo de la cuota 2026, precios, gasto de riego y
  Convenio) y el resumen por factor de la 11e (hojas `tornado_rangos` y
  `deltas_vs_modelo`).
- `resultados_corrida\ingreso_potencial_y_periodos.xlsx`: ingreso potencial del
  caudal y comparación por período (sección 12d).
- `resultados_corrida\figures_informe\*.pdf`: todas las figuras del informe final,
  con el mismo nombre que usa el `.tex`:

  | Archivo | Figura del informe | Sección del notebook |
  |---|---|---|
  | `e2_anios_pe.pdf` | Años por probabilidad de excedencia (`fig:anios_pe`) | 5 |
  | `e3_caudal_natural.pdf` | Caudal natural en B_Maule por origen y variabilidad (`fig:caudal_natural`) | 5 |
  | `e2_operacion.pdf` | Caudal en B_Maule y volumen de la Laguna (`fig:operacion`) | 9 |
  | `e3_miope_terminal.pdf` | Año seco: modelo, miope y miope con V_final ≥ V_inicial (`fig:miope`) | 9 y 11d |
  | `e2_q_con_sin.pdf` | Caudal sin y con Convenio (`fig:con_sin`) | 11c |
  | `e2_duracion.pdf` | Curva de duración (`fig:duracion`) | 12 |
  | `e3_sensibilidades.pdf` | Sensibilidad a las condiciones de borde (`fig:sensibilidades`) | 11d |
  | `e2_nueva_central.pdf` | Nueva central | 12b |
  | `e3_tornado.pdf` | Rango del cambio en Q medio y Q90 por factor (`fig:tornado`) | 11e |
  | `e3_tornado_central.pdf` | Sensibilidad del ingreso de la nueva central (`fig:tornado_central`) | 12b |
  | `e3_periodo_reciente.pdf` | Caudal medio anual y curva de duración por período (`fig:reciente`) | 12d |

  Todas se generan en la sección 12c; basta copiarlas a `figures/` en Overleaf.
- `resultados_corrida\log_corrida.txt`: salida textual completa de la corrida.
- `resultados_corrida\Modelo_Final_Maule_C2_corregido_ejecutado.ipynb`: notebook
  con las celdas ejecutadas y sus resultados.

## Resultados principales

La corrida usa CMg medio y gasto de riego de `160 m³/s` en tres escenarios:

| Indicador | Húmedo 1992-93 | Medio 1973-74 | Seco 2010-11 |
|---|---:|---:|---:|
| Percentil de excedencia (`Pe`) | 19,7 % | 50,0 % | 89,4 % |
| Caudal medio en `B_Maule` | 135,9 m³/s | 98,1 m³/s | 68,2 m³/s |
| Caudal mínimo semanal | 70,9 m³/s | 68,8 m³/s | 42,3 m³/s |
| Energía | 11.725 GWh | 9.890 GWh | 6.643 GWh |
| Ingreso | 421,1 MUSD | 391,3 MUSD | 280,0 MUSD |
| Déficit de riego | 0 hm³ | 0 hm³ | 0 hm³ |
| Volumen final en `LMAULE` | 754,9 hm³ | 664,7 hm³ | 664,7 hm³ |

Contra el caso base secuencial (mismas condiciones de borde), el modelo entrega
el mismo caudal medio, pero más estable y con más ingreso:

| Indicador (caso base → modelo) | Húmedo | Medio | Seco |
|---|---:|---:|---:|
| Caudal medio en `B_Maule` | 135,9 → 135,9 | 98,1 → 98,1 | 68,2 → 68,2 |
| `Q90` | 74,8 → 79,0 | 50,0 → 52,2 | 26,7 → 28,5 |
| Caudal mínimo semanal | 58,6 → 70,9 | 31,0 → 68,8 | 28,5 → 42,3 |
| Ingreso [MUSD] | 402,4 → 421,1 | 343,7 → 391,3 | 232,7 → 280,0 |

En el análisis de sensibilidad, el caudal medio en `B_Maule` cambia a lo más
~4 m³/s en los años húmedo y medio. En el año seco solo lo suben los casos que
dejan terminar la Laguna bajo su volumen inicial: sin condición terminal
(+5,5 a +7,1 m³/s, Laguna en 447–500 hm³) y el miope puro (+13,6 m³/s, Laguna
en 243 hm³). Es agua prestada del año siguiente, no agua que produce la cuenca. El
detalle está en `resultados_corrida\RESUMEN_corrida.md`.

Para la serie completa de 65 años (1960-61 a 2024-25), el caudal medio en
`B_Maule` es `107,9 m³/s`, el ingreso medio es `363,4 MUSD` y el déficit de
riego es `0 hm³` en todos los años. El año mínimo es 1998-99
(`40,5 m³/s`) y el máximo es 1982-83 (`181,6 m³/s`).

Para la nueva central, usando `Qd = Q50 = 99,4 m³/s` y rendimiento supuesto
`η = 0,45`, el resultado para 65 años es:

- Potencia: `44,7 MW`.
- Generación: `331,3 GWh/año`.
- Ingreso: `11,2 MUSD/año`.
- Factor de planta: `0,85`.
- Sensibilidad del ingreso (un supuesto a la vez): CMg ±20 % → 9,0–13,4;
  hidrología p10–p90 → 9,3–12,5; η 0,40–0,50 → 10,0–12,4; `Qd` entre `Q70` y
  `Q30` → 9,8–12,2 MUSD/año.

## Verificación de la corrida

La corrida oficial registrada en `resultados_corrida\` se ejecutó el 25-11-2026
con Python 3.11.7 y **Gurobi 13.0.3** (licencia académica), forzando el solver
con la variable de entorno `SOLVER=gurobi` para que no se use el respaldo de
HiGHS. Todas las celdas corren sin errores y todas las soluciones pasan la
verificación independiente. Todos los resultados del modelo, las sensibilidades
y los 65 años coinciden con la corrida del 18-11-2026; solo cambian los tiempos
de cómputo. Es la primera corrida oficial que incluye la sección 12d (ingreso
potencial del caudal y período reciente).

Para repetir la corrida con Gurobi, se ejecuta el comando de la sección
*Ejecución reproducible* después de definir `$env:SOLVER = "gurobi"`. El
respaldo con HiGHS sirve solo para ejecutar el notebook sin licencia. En ese
caso, el ingreso de los casos secuenciales (caso base y miope) puede diferir en
algunos MUSD, porque cada semana puede tener soluciones alternativas.

Los archivos de `resultados_corrida\` son exclusivamente productos de la
última ejecución y sirven para revisar tablas y figuras sin volver a resolver
el modelo. No se incluyen credenciales, archivos de licencia, entornos
virtuales, cachés ni copias de corridas anteriores.
