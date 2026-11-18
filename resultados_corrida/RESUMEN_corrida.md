# Corrida final del modelo del Maule (Modelo_Final_Maule_C2_corregido.ipynb)
Fecha: 18-11-2026 · Gurobi 13.0.3 (licencia académica, `SOLVER=gurobi`) · todas las celdas sin errores.
Verificación independiente OK en los 3 escenarios, en el caso base y en los 45 casos de sensibilidad.
Todos los resultados (modelo, sensibilidades y 65 años) coinciden con la corrida del 17-11-2026; solo cambian los tiempos de cómputo.

## Qué cambió respecto de la corrida del 18-10-2026
1. **Caso base comparable** (aporte del código de un compañero, integrado al notebook del repositorio).
   Antes el caso base era un miope puro: sin condición terminal y con el déficit de riego penalizado
   solo en la semana en curso. No era comparable con el modelo: en el año seco "ganaba" 13,6 m³/s de
   caudal medio vaciando la Laguna (665 → 243 hm³), y al agregarle solo la condición terminal dejaba
   294,7 hm³ de riego sin cubrir. Ahora el caso base es una **operación secuencial con objetivo semanal**
   con las mismas condiciones de borde que el modelo (`V_final ≥ V_inicial` y riego sin déficit).
   El miope puro y la variante con riego penalizado se mantienen como sensibilidades (1b y 1c).
2. **Más escenarios en la sección 11d:** se agregan CMg de la propia hidrología, gasto de riego de
   200 m³/s y sin Convenio, para tener todas las sensibilidades en una sola tabla.
3. **Nueva sección 11e:** resumen de sensibilidad por factor (rango de Δ respecto del modelo) y tornado
   `e3_tornado.pdf`.
4. **Sección 12b:** sensibilidad del ingreso de la nueva central y tornado `e3_tornado_central.pdf`.
5. Textos con cifras antiguas corregidos (secciones 9 y 12), instalación compatible con VS Code y Colab,
   `highspy` en `requirements.txt`.

## 3 escenarios (CMg MEDIA, gasto riego 160 m³/s): sin cambios
| | Húmedo 1992-93 | Medio 1973-74 | Seco 2010-11 |
|---|---|---|---|
| Q medio en B_Maule [m³/s] | 135,9 | 98,1 | 68,2 |
| Q50 / Q90 [m³/s] | 118,7 / 79,0 | 100,2 / 52,2 | 74,0 / 28,5 |
| Q mínimo semanal [m³/s] | 70,9 | 68,8 | 42,3 |
| Ingreso [MUSD] | 421,1 | 391,3 | 280,0 |
| Déficit de riego [hm³] | 0 | 0 | 0 |
| V final LMAULE [hm³] | 754,9 | 664,7 | 664,7 |

## Caso base secuencial vs. modelo
| | Q medio | Q90 | Q mín. semanal | Ingreso [MUSD] | Déficit riego | V final LMAULE |
|---|---|---|---|---|---|---|
| Húmedo | 135,9 → 135,9 | 74,8 → 79,0 | 58,6 → 70,9 | 402,4 → 421,1 (+18,7) | 0 → 0 | 754,9 → 754,9 |
| Medio | 98,1 → 98,1 | 50,0 → 52,2 | 31,0 → 68,8 | 343,7 → 391,3 (+47,7) | 0 → 0 | 664,7 → 664,7 |
| Seco | 68,2 → 68,2 | 26,7 → 28,5 | 28,5 → 42,3 | 232,7 → 280,0 (+47,3) | 0 → 0 | 664,7 → 664,7 |

**Lectura:** con las mismas condiciones de borde, planificar el año no cambia cuánta agua llega a
B_Maule, sino **cuándo** llega: sube el Q90 y sobre todo el mínimo semanal, y el ingreso. La ganancia
por planificar es +18,7 / +47,7 / +47,3 MUSD (antes +19 / +44 / +11). En el año seco es mucho mayor,
porque el caso base ya no puede vaciar la Laguna.

## Sensibilidades (Δ respecto del modelo; detalle en `sensibilidades_borde.xlsx`)
| Factor | Δ Q medio [m³/s] (H / M / S) | Δ Q90 [m³/s] (H / M / S) | Comentario |
|---|---|---|---|
| Miope puro | +0,2 / +1,3 / +13,6 | −4,2 / 0,0 / +1,5 | Sube el caudal del seco bajando la Laguna a 243 hm³ |
| Condición terminal (sin ella, con o sin valor del agua) | −3,2 a +0,2 / +0,6 a +1,3 / +5,5 a +7,1 | −8,1 a 0 / 0 a +8,7 / +7,5 a +10,3 | El efecto relevante está en el seco y se paga con la Laguna (447–500 hm³) |
| Uso previo de la cuota 2026 (0 y 250 hm³) | −4,0 a +2,9 / −2,9 a 0 / 0 | −6,2 a +3,1 / −0,4 a 0 / 0 a +3,3 | Solo húmedo y medio |
| Convenio (sin) | +2,9 / 0 / 0 | +3,2 / 0 / 0 | Solo restringe en el húmedo |
| Volumen inicial Laguna (400, 510, 900 hm³) | −0,3 a 0 / −2,2 a 0 / 0 | −2,8 a 0 / −0,4 a 0 / 0 a +0,7 | Solo importa si parte en la reserva ordinaria |
| Gasto de riego 200 m³/s | +0,3 / 0 / 0 | 0 / 0 / 0 | Solo baja el ingreso (−2,6 y −7,3 MUSD en medio y seco) |
| Caso base secuencial | 0 / 0 / 0 | −4,2 / −2,2 / −1,8 | Mismo caudal medio, peor distribución |
| Sin filtración | 0 / 0 / 0 | +3,1 / +0,3 / −8,5 | El agua vuelve al río antes de B_Maule; cambia el Q90 del seco |
| CMg de su hidrología | 0 / 0 / 0 | −2,5 / 0 / +1,0 | Mueve el ingreso (−39,9 / 0 / +28,0 MUSD), no el caudal |

## 65 años (1960-61 a 2024-25): sin cambios
Q medio en B_Maule: media 107,9, p10 70,9, p50 101,4, p90 153,1 m³/s; mín. 40,5 (1998-99), máx. 181,6 (1982-83).
Ingreso medio 363,4 MUSD. Déficit de riego 0 en los 65 años.

## Nueva central en B_Maule (Qd = Q50 = 99,4 m³/s, η = 0,45)
44,7 MW, 331,3 GWh/año, 11,2 MUSD/año, factor de planta 0,85 (promedio de 65 años).

| Supuesto (uno a la vez) | Ingreso [MUSD/año] |
|---|---|
| Nivel de CMg −20 % / +20 % | 9,0 – 13,4 |
| Hidrología, año p10 / p90 | 9,3 – 12,5 |
| Rendimiento η 0,40 / 0,50 | 10,0 – 12,4 |
| Caudal de diseño Q70 / Q30 | 9,8 – 12,2 |
| Operación aguas arriba, año medio (caso base / modelo) | 10,1 – 11,2 |
| Convenio, año medio (con / sin) | 11,2 – 11,2 |

## Qué hay que actualizar en el informe final (.tex)
1. Caso base: reemplazar la descripción del miope por la operación secuencial con las mismas condiciones
   de borde, la tabla caso base vs. modelo y su lectura (ganancia +18,7 / +47,7 / +47,3 MUSD; mismo caudal medio).
2. Figura `fig:miope` (`e3_miope_terminal.pdf`): ahora compara modelo, caso base secuencial y miope puro.
3. Agregar la tabla de sensibilidad por factor y las figuras `e3_tornado.pdf` y `e3_tornado_central.pdf`.
4. Reemplazar las figuras de `figures_informe/` (mismos nombres).
