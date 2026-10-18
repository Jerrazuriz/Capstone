# Corrida del modelo final del Maule (Modelo_Final_Maule_revisado.ipynb)
Fecha: 18-10-2026 · Gurobi 13.0.3 (licencia académica) · corrida local, todas las celdas sin errores.

## 3 escenarios (CMg MEDIA, gasto riego 160 m³/s) — verificación independiente OK en los 3
| | Húmedo 1992-93 | Medio 1973-74 | Seco 2010-11 |
|---|---|---|---|
| Pe [%] | 19,7 | 50,0 | 89,4 |
| Q medio en B_Maule [m³/s] | 132,0 | 95,1 | 68,2 |
| Q natural en B_Maule [m³/s] | 138,8 | 98,1 | 68,2 |
| Q mínimo semanal [m³/s] | 70,9 | 58,5 | 42,3 |
| Q50 / Q90 [m³/s] | 112,0 / 76,2 | 98,3 / 48,9 | 74,0 / 28,5 |
| Energía [GWh] | 11.378 | 9.590 | 6.657 |
| Ingreso [MUSD] | 410,0 | 380,3 | 280,0 |
| Déficit de riego [hm³] | 0 | 0 | 0 |
| Generación desde la Laguna [hm³] | 250,0 | 250,0 | 230,2 |
| V final LMAULE [hm³] | 879,9 | 756,7 | 664,7 |

## Caso base miope vs. modelo
| | Q medio (miope → modelo) | Q90 | Q mín. semanal | Ingreso [MUSD] | Déficit riego [hm³] |
|---|---|---|---|---|---|
| Húmedo | 132,2 → 132,0 | 59,9 → 76,2 | 49,1 → 70,9 | 381,8 → 410,0 (+28,2) | 0 → 0 |
| Medio | 95,4 → 95,1 | 36,4 → 48,9 | 31,0 → 58,5 | 326,9 → 380,3 (+53,4) | 0 → 0 |
| Seco | 79,8 → 68,2 | 28,5 → 28,5 | 28,5 → 42,3 | 264,1 → 280,0 (+15,9) | 35,3 → 0 |

En el seco el miope vacía la Laguna (V final 305,8 hm³ vs. 664,7) y deja 35,3 hm³ de riego sin cubrir.

## Sensibilidades
- **Precios de su propia hidrología:** Húmedo 372,3 MUSD (vs. 410,0), Medio 380,3, Seco 308,0 (vs. 280,0). El Q en B_Maule no cambia.
- **Gasto de riego 200 vs. 160 m³/s:** Medio Q 97,3 vs. 95,1, Q90 58,7 vs. 48,9, ingreso 383,4 vs. 380,3, con 13 semanas en reserva ordinaria. Seco Q 68,2 en ambos, ingreso 272,7 vs. 280,0, con 16 semanas en reserva ordinaria. Sin déficit en ningún caso.
- **Sin vs. con Convenio (Q medio B_Maule):** Húmedo 138,8 → 132,0; Medio 98,1 → 95,1; Seco 68,2 → 68,2. Ingreso −18,0 / −11,2 / −1,4 MUSD.

## 65 años (1960-61 a 2024-25)
Q medio en B_Maule: media 106,0, p10 70,9, p50 100,2, p90 149,1, mín. 40,5 (1998-99), máx. 177,6 (1982-83) m³/s. Q90 medio 56,7. Ingreso medio 356,8 MUSD. Déficit de riego 0 en los 65 años.

## Nueva central en B_Maule (η = 0,45 supuesto, barra Pehuenche220)
Con Qd = Q50 = 97,8 m³/s: 44 MW, 325,8 GWh/año y 11,0 MUSD/año (65 años), factor de planta 0,85.

| Qd | Q90 (42,3) | Q70 (80,7) | Q50 (97,8) | Q medio (106,0) | Q30 (116,5) |
|---|---|---|---|---|---|
| Potencia [MW] | 19,1 | 36,3 | 44,0 | 47,7 | 52,4 |
| Generación [GWh] | 162,9 | 284,2 | 325,8 | 340,0 | 354,0 |
| Ingreso [MUSD] (p10–p90) | 5,3 (5,1–5,4) | 9,5 (8,7–10,2) | 11,0 (9,3–12,2) | 11,5 (9,4–13,1) | 11,9 (9,5–14,0) |
| Factor de planta | 0,98 | 0,89 | 0,85 | 0,81 | 0,77 |

Por escenario (Qd = Q50): Húmedo 364,7 GWh / 12,0 MUSD; Medio 331,8 / 11,5; Seco 262,6 / 9,2.

## Archivos generados (en esta carpeta)
`Modelo_Final_Maule_revisado_ejecutado.ipynb`, `resultados_modelo_final_maule.xlsx`,
`resultados_65_anios.xlsx`, `figures_informe/e2_*.pdf` (6 figuras del informe)
y `log_corrida.txt` (salida completa).
