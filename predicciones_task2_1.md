# Predicciones Task 2.1 (grupo 11: λ=3.0, c=18, a=12, ρ=2/3, k_off=9, T_b=7 d)

Escritas ANTES de ejecutar cualquier simulación del Task 2 (solo se había calculado la teoría exponencial del Task 1.1 y validado el simulador del Task 1). No se modifican después.

## 2.1a  Allen–Cunneen
Base M/M/18: Wq = 0.0504 d = 1.21 h (Erlang C = 0.0756).
- C_S = 0 → Wq ≈ 1.21 h · (1+0)/2 = **0.60 h**.
- C_S = 1 → Wq ≈ 1.21 h · (1+1)/2 = **1.21 h** (es la teoría exacta).
- C_S = 2 → Wq ≈ 1.21 h · (1+4)/2 = **3.02 h**.
Razonamiento: la fórmula escala la espera de M/M/c por (1+C_S²)/2; se supone que solo importan los dos primeros momentos de la estancia. Espero que sea menos precisa en C_S = 2: con ρ=0.67 y c=18 la espera es un evento raro (6 %) y depende de ráfagas de llegadas coincidiendo con estancias largas; la cola pesada de la lognormal hace que los momentos de orden superior (que la fórmula ignora) pesen más. En C_S = 0 espero un error menor (la aproximación es conocida por ser razonable para M/D/c).

## 2.1b  Tiempo de vaciado T_d
Modelo de acumulación (fluido): con la fila en su valor estacionario L_q0, durante el cierre la fila crece a tasa r_b = λ − (c−k_off)μ y tras reabrir baja a tasa d = cμ − λ:
  Q(T_b) = L_q0 + r_b·T_b,   T_d = (Q(T_b) − 1.1·L_q0)/d = (r_b·T_b − 0.1·L_q0)/(cμ − λ)  ≈ r_b·T_b/(cμ−λ).
Con mis parámetros: r_b = 3 − 9·0.25 = 0.75 pac/día, d = 18·0.25 − 3 = 1.5 pac/día, L_q0 = 0.151:
  Q(T_b) = 0.151 + 0.75·7 = 5.40;  **T_d = (5.25 − 0.015)/1.5 = 3.49 días ≈ 3.5 días** (≈ 84 h).
Predicción de la simulación: **MENOR**, del orden de **1 día** o menos. Razonamiento: la fórmula supone que tras reabrir hay que vaciar la fila a tasa cμ−λ, pero en realidad al reabrir solo hay ≈9 camas ocupadas y 9 libres, así que una fila de ≈5–8 pacientes se absorbe casi de inmediato; el modelo fluido confunde "servidores todos ocupados" con la situación real. Efectos en sentido contrario (pacientes que ya estaban en cama durante el cierre, variabilidad de la fila) la alargan, pero espero que domine el primero.

## 2.1c  Estancia +25 %
Nueva media 5 días → μ' = 0.20, a' = λ/μ' = 15, c = 18. Erlang B: B(18,15) = **0.0862** (8.6 %), frente a B(18,12) = 0.0265 → **3.25 veces mayor**.
Razonamiento: la recurrencia B(k)=aB(k−1)/(k+aB(k−1)); subir la carga ofrecida de 12 a 15 (ρ de 0.67 a 0.83) hace crecer el bloqueo de forma no lineal, mucho más que el 25 % de la estancia.
