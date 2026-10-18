# Corrida del modelo final del Maule (Modelo_Final_Maule_C2_corregido.ipynb)
Fecha: 18-10-2026 · Gurobi 13.0.3 (licencia académica) · corrida local, todas las celdas sin errores.
Verificación independiente OK en los 3 escenarios y en los 3 casos miope.

## Qué cambió respecto de la corrida anterior (Modelo_Final_Maule_revisado.ipynb)
Un solo cambio de modelo: **C2 (cuota de generación del Art. 4) se impone por año calendario**
y no sobre las 48 semanas del horizonte.

- Antes: κ·Σ_{t,b} h·g ≤ 250 hm³ en todo el horizonte jul-2026 / jun-2027.
- Ahora: κ·Σ_{t∈T_c,b} h·g ≤ C_c para c = 2026 (semanas 1-24, jul-dic) y c = 2027 (semanas 25-48, ene-jun),
  con C_2026 = 250 − 125 = 125 hm³ y C_2027 = 250 hm³.
- Supuesto nuevo: se desconoce cuánto de la cuota 2026 se usó en ene-jun 2026; se supone un uso
  **a prorrata de 125 hm³** (medio año). Debe declararse como supuesto y sensibilizarse.
- Efecto: la cuota disponible en el horizonte sube de 250 a 375 hm³. El Convenio pasa a restringir
  menos: más agua de la Laguna se turbina dentro del año y llega más caudal a B_Maule en los años
  húmedo y medio. El año seco no cambia (allí la cuota no era la restricción activa).
- Es coherente con C6, que ya se imponía por año calendario.

## 3 escenarios (CMg MEDIA, gasto riego 160 m³/s)
| | Húmedo 1992-93 | Medio 1973-74 | Seco 2010-11 |
|---|---|---|---|
| Pe [%] | 19,7 | 50,0 | 89,4 |
| Q medio en B_Maule [m³/s] | 135,9 (antes 132,0) | 98,1 (antes 95,1) | 68,2 (igual) |
| Q natural en B_Maule [m³/s] | 138,8 | 98,1 | 68,2 |
| Q mínimo semanal [m³/s] | 70,9 (igual) | 68,8 (antes 58,5) | 42,3 (igual) |
| Q50 / Q90 [m³/s] | 118,7 / 79,0 (antes 112,0 / 76,2) | 100,2 / 52,2 (antes 98,3 / 48,9) | 74,0 / 28,5 (igual) |
| Energía [GWh] | 11.725 (antes 11.378) | 9.890 (antes 9.590) | 6.643 (antes 6.657) |
| Ingreso [MUSD] | 421,1 (antes 410,0) | 391,3 (antes 380,3) | 280,0 (igual) |
| CMg obtenido [USD/MWh] | 35,9 | 39,6 | 42,1 |
| Déficit de riego [hm³] | 0 | 0 | 0 |
| Generación desde la Laguna [hm³] | 375,0 (antes 250,0) | 343,9 (antes 250,0) | 230,2 (igual) |
| Riego desde la Laguna [hm³] | 0,0 | 3,1 (antes 5,1) | 66,2 |
| V final LMAULE [hm³] | 754,9 (antes 879,9) | 664,7 (antes 756,7) | 664,7 (igual) |
| Semanas en reserva ordinaria | 0 | 0 | 0 |

V inicial LMAULE = 664,7 hm³. Tiempo de resolución < 1 s por escenario; gap ≤ 0,01 %.

## Caso base miope vs. modelo
| | Q medio (miope → modelo) | Q90 | Q mín. semanal | Ingreso [MUSD] | Déficit riego [hm³] | V final LMAULE [hm³] |
|---|---|---|---|---|---|---|
| Húmedo | 136,2 → 135,9 | 74,8 → 79,0 | 58,6 → 70,9 | 402,3 → 421,1 (+18,8) | 0 → 0 | 754,9 → 754,9 |
| Medio | 99,3 → 98,1 | 52,2 → 52,2 | 31,0 → 68,8 | 347,1 → 391,3 (+44,2) | 0 → 0 | 631,7 → 664,7 |
| Seco | 81,8 → 68,2 | 30,0 → 28,5 | 29,8 → 42,3 | 268,9 → 280,0 (+11,1) | 0 → 0 | 243,1 → 664,7 |

**Cambio importante de interpretación:** en la corrida anterior el miope dejaba 35,3 hm³ de riego sin
cubrir en el año seco; **ahora el miope cumple todo el riego** en los tres escenarios. El argumento
contra el miope en el seco queda en que vacía la Laguna (664,7 → 243,1 hm³) para dar más caudal medio,
y en que entrega un mínimo semanal menor (29,8 vs. 42,3 m³/s). La ganancia por planificar baja a
+18,8 / +44,2 / +11,1 MUSD (antes +28,2 / +53,4 / +15,9).

## Sensibilidades
- **Precios de su propia hidrología:** Húmedo 381,2 MUSD (vs. 421,1 con CMg MEDIA), Medio 391,3, Seco 308,0
  (vs. 280,0). El Q en B_Maule no cambia. El húmedo sigue dando menos ingreso que el medio (381 vs. 391).
- **Gasto de riego 200 vs. 160 m³/s:** Medio Q 98,1 en ambos, Q90 52,2 en ambos, ingreso 388,8 vs. 391,3,
  con 20 semanas en reserva ordinaria (antes 13). Seco Q 68,2 en ambos, ingreso 272,7 vs. 280,0, 16 semanas
  en reserva ordinaria. Sin déficit en ningún caso.
  (Antes, en el medio, el gasto de 200 subía el Q a 97,3 y el Q90 a 58,7; ese efecto desaparece.)
- **Sin vs. con Convenio:**

| | Q medio sin → con | Q50 | Q90 | Q mín. sem. | Ingreso [MUSD] | V final LMAULE |
|---|---|---|---|---|---|---|
| Húmedo | 138,8 → 135,9 (−2,9; antes −6,8) | 125,1 → 118,7 | 82,3 → 79,0 | 76,4 → 70,9 | 428,0 → 421,1 (−6,9; antes −18,0) | 664,7 → 754,9 |
| Medio | 98,1 → 98,1 (0,0; antes −2,9) | 99,1 → 100,2 | 52,2 → 52,2 | 68,4 → 68,8 | 391,5 → 391,3 (−0,1; antes −11,2) | 664,7 → 664,7 |
| Seco | 68,2 → 68,2 (0,0) | 76,4 → 74,0 | 28,5 → 28,5 | 38,8 → 42,3 | 281,4 → 280,0 (−1,4) | 664,7 → 664,7 |

  **Cambio de conclusión:** con la cuota por año calendario, el Convenio solo reduce el caudal en B_Maule
  en el año húmedo (−2,9 m³/s, 2 %). En los años medio y seco su efecto sobre el caudal medio es nulo.

## 65 años (1960-61 a 2024-25)
Q medio en B_Maule: media 107,9 (antes 106,0), p10 70,9, p50 101,4 (antes 100,2), p90 153,1 (antes 149,1),
mín. 40,5 (1998-99), máx. 181,6 (1982-83; antes 177,6) m³/s. Q natural medio 109,2.
Q90 medio 58,3 (antes 56,7). Ingreso medio 363,4 MUSD (antes 356,8), p10 282,6, p50 379,6, p90 422,8.
Déficit de riego 0 en los 65 años.

## Nueva central en B_Maule (η = 0,45 supuesto, barra Pehuenche220)
Con Qd = Q50 = 99,4 m³/s (antes 97,8): 44,7 MW (antes 44,0), 331,3 GWh/año (antes 325,8) y
11,2 MUSD/año (antes 11,0) en promedio de los 65 años, factor de planta 0,85, precio capturado 34,0 USD/MWh.

| Qd | Q90 (42,4) | Q70 (83,5) | Q50 (99,4) | Q medio (107,9) | Q30 (119,7) |
|---|---|---|---|---|---|
| Potencia [MW] | 19,1 | 37,6 | 44,7 | 48,6 | 53,9 |
| Generación [GWh] | 163,1 | 293,1 | 331,3 | 346,2 | 361,9 |
| Ingreso [MUSD] (p10–p90) | 5,3 (5,1–5,4) | 9,8 (8,9–10,6) | 11,2 (9,3–12,5) | 11,7 (9,4–13,4) | 12,2 (9,5–14,4) |
| Factor de planta | 0,98 | 0,89 | 0,85 | 0,81 | 0,77 |
| Precio capturado [USD/MWh] | 32,5 | 33,8 | 34,0 | 34,1 | 34,0 |
| Tiempo a plena carga [%] | 90,0 | 70,0 | 50,0 | 39,1 | 30,0 |

Por escenario (Qd = Q50 = 99,4):
| | Húmedo | Medio | Seco |
|---|---|---|---|
| Modelo: GWh / MUSD / FP | 374,0 / 12,35 / 0,95 | 343,9 / 11,94 / 0,88 | 263,3 / 9,25 / 0,67 |
| Miope: GWh / MUSD / FP | 365,1 / 11,86 / 0,93 | 331,7 / 10,91 / 0,85 | 280,6 / 8,72 / 0,72 |
| Sin Convenio: GWh / MUSD / FP | 377,0 / 12,41 / 0,96 | 343,1 / 11,93 / 0,88 | 264,1 / 9,35 / 0,67 |
| Precio capturado modelo [USD/MWh] | 33,0 | 34,7 | 35,1 |
| Tiempo a plena carga modelo [%] | 79,6 | 51,8 | 9,2 |

## Qué hay que actualizar en el Informe 2 (.tex)
1. Ecuación C2 (`eq:c2`): pasar de una suma sobre todo el horizonte a una por año calendario
   (`\forall c`, sobre `t \in T_c`, con cota `C_c`), y definir `C_c` en Parámetros
   (C_2026 = 125, C_2027 = 250 hm³).
2. Supuestos (Tabla `tab:supuestos`): reemplazar "Cuota de 250 hm³ sin saldo de años anteriores" por
   "Cuota de 250 hm³ por año calendario; uso a prorrata de 125 hm³ en ene-jun 2026 (no observado)", con
   sensibilidad a ese uso previo (entrega final). Mantener que no se modela la acumulación hasta 350 hm³.
3. Todas las cifras de resultados de las tablas anteriores (escenarios, miope, sensibilidades, 65 años,
   nueva central), incluido el resumen.
4. Texto del caso miope: quitar que el miope deja 35 hm³ de riego sin cubrir en el seco.
5. Texto de con/sin Convenio: el efecto ahora es pequeño (solo húmedo, −2,9 m³/s).
6. Caudal de diseño de referencia: Q50 = 99,4 m³/s (antes se citaba 98 / 97,8).
7. Reemplazar las 6 figuras por las nuevas de `figures_informe/` (mismos nombres).

Datos que **no** cambian: selección de años y Pe, afluentes, CMg por barra, demanda de riego
(2.244 hm³), filtración (11,84 m³/s), tamaño del modelo (~16.700 variables, 288 binarias).

## Archivos generados (en esta carpeta)
`Modelo_Final_Maule_C2_corregido_ejecutado.ipynb`, `resultados_modelo_final_maule.xlsx`,
`resultados_65_anios.xlsx`, `figures_informe/e2_*.pdf` (6 figuras del informe)
y `log_corrida.txt` (salida completa).
