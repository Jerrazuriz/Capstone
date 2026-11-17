# Sensibilidades del informe final

Corridas pendientes de la entrega final, hechas con el **mismo modelo** del notebook
`Modelo_Final_Maule_C2_corregido.ipynb`. El script no copia el modelo: lee las celdas de
código del notebook (datos, red, restricciones, verificación e indicadores) y las ejecuta,
así que cualquier cambio en el notebook se refleja aquí.

## Cómo correr

Desde la carpeta raíz del repositorio (la que tiene `data\`):

```powershell
python -m pip install -r requirements.txt highspy tabulate
python sensibilidades_final\correr_sensibilidades.py
```

Tarda unos 2 a 3 minutos. Usa Gurobi si hay licencia completa (`gurobi.lic` o
`GRB_LICENSE_FILE`). Si solo está la licencia restringida de `pip install gurobipy`, arma el
mismo modelo con gurobipy, lo exporta a MPS y lo resuelve con HiGHS. Se puede forzar con
`$env:SOLVER="gurobi"` o `$env:SOLVER="highs"`.

**Control de calidad:** la primera sección del script vuelve a resolver los 3 escenarios
base. Con HiGHS reproduce exactamente la corrida de Gurobi del 18-10-2026 (135,9 / 98,1 /
68,2 m³/s; Q90 79,0 / 52,2 / 28,5; V final Laguna 754,9 / 664,7 / 664,7), y el miope del
notebook también (136,2 / 99,3 / 81,8). Las 33 soluciones pasan la verificación
independiente del notebook.

Una diferencia menor: el **ingreso** del miope sale 405,3 / 350,0 / 269,1 MUSD con HiGHS frente
a 402,3 / 347,1 / 268,9 con Gurobi. Cada semana del miope tiene soluciones alternativas con
el mismo ingreso semanal, y cada solver elige una distinta, lo que cambia levemente las
semanas siguientes. Los caudales (promedio, Q90, mínimo) y los volúmenes finales coinciden.

## Qué corre

| Grupo | Caso | Cómo se implementa |
|---|---|---|
| 1 | Miope con $V_{final} \ge V_{inicial}$ | El mismo miope del notebook (semana a semana, solo el ingreso de la semana), pero sin relajar la cota del volumen final |
| 2a | Sin condición terminal | Modelo optimizado con la cota de volumen final relajada (Laguna ≥ 170, resto ≥ Vmin) |
| 2b | Sin condición terminal, con valor del agua | 2a + el volumen final valorizado en el objetivo: Σ rendimientos aguas abajo × CMg medio (Laguna 94.098 USD/hm³) |
| 3 | V inicial de la Laguna 400, 510 y 900 hm³ | Cambia `V0` de LMAULE (base 664,7); la condición terminal pasa a ser $V_{final} \ge$ ese nuevo $V_0$ |
| 4 | Sin filtración | `FILT = 0` (base 11,84 m³/s) |
| 5 | Uso previo de la cuota 2026 de 0 y 250 hm³ | `CUOTA_DISPONIBLE[2026] = 250 − uso` (base 125 hm³ usados) |

## Archivos de salida (`resultados/`)

| Archivo | Contenido |
|---|---|
| `sensibilidades.xlsx` | Hoja `todas` (una fila por caso y escenario, con todos los indicadores y la diferencia con la base), hoja `tabla_informe` (Q medio, Q50, Q90, Q mín. semanal y V final de la Laguna) y hoja `semanal` (caudal en B_Maule y volumen de la Laguna por semana) |
| `sensibilidades.csv` | Lo mismo que la hoja `todas` |
| `tabla_informe.md` | La tabla del informe en texto |
| `log_sensibilidades.txt` | Salida de la corrida |

## Figuras para el informe (de dónde sale cada una)

| Figura (subir a Overleaf, carpeta `figures/`) | Sale de | Qué muestra | Dónde va en `main_final.tex` |
|---|---|---|---|
| `resultados/figuras/e3_sensibilidades.pdf` | `exportar()`, "Figura A" | Q medio y Q90 en B_Maule de cada sensibilidad y escenario frente al modelo base (líneas punteadas) | `\label{fig:sensibilidades}`, sección de sensibilidad a las condiciones de borde |
| `resultados/figuras/e3_miope_terminal.pdf` | `exportar()`, "Figura B" | Año seco: caudal semanal en B_Maule y volumen de la Laguna para el modelo, el miope y el miope con $V_f \ge V_0$ | `\label{fig:miope_terminal}`, sección del caso base |

Los `.png` son las mismas figuras, para verlas rápido. Si cambian algo del gráfico, editen
`exportar()` y vuelvan a correr el script.
