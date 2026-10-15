"""
Simulador de eventos discretos para UCI: M/M/c (con espera) y M/M/c/c (sin espera).
"""
import heapq
import random
import math
import statistics


def simular(lam, mu, c, horizonte, calentamiento=0.0, semilla=None, con_espera=True):
    rng = random.Random(semilla)
    # lista de eventos: (tiempo, tipo)  tipo 0 = llegada, 1 = salida
    eventos = []
    heapq.heappush(eventos, (rng.expovariate(lam), 0))

    ocupadas = 0
    fila = []            # tiempos de llegada de los que esperan
    t = 0.0

    llegadas = 0
    bloqueados = 0
    esperaron = 0
    atendidos = 0
    esperas = []

    # acumuladores para L y Lq
    muestras_L = []
    muestras_Lq = []
    tiempo_ocupado = 0.0
    t_prev = 0.0

    while eventos:
        t, tipo = heapq.heappop(eventos)
        if t > horizonte:
            break

        # estadísticas de utilización (tiempo ocupado) después del calentamiento
        if t > calentamiento:
            tiempo_ocupado += ocupadas * (t - max(t_prev, calentamiento))
        t_prev = t

        if tipo == 0:
            # llegada
            heapq.heappush(eventos, (t + rng.expovariate(lam), 0))
            if t > calentamiento:
                llegadas += 1
            if ocupadas < c:
                ocupadas += 1
                heapq.heappush(eventos, (t + rng.expovariate(mu), 1))
                if t > calentamiento:
                    atendidos += 1
                    esperas.append(0.0)
            else:
                if con_espera:
                    fila.append(t)
                else:
                    if t > calentamiento:
                        bloqueados += 1
        else:
            # salida
            if fila:
                t_llegada = fila.pop(0)
                heapq.heappush(eventos, (t + rng.expovariate(mu), 1))
                if t > calentamiento:
                    atendidos += 1
                    esperaron += 1
                    esperas.append(t - t_llegada)
            else:
                ocupadas -= 1

        if t > calentamiento:
            muestras_L.append(ocupadas + len(fila))
            muestras_Lq.append(len(fila))

    T = horizonte - calentamiento
    L = sum(muestras_L) / len(muestras_L)
    Lq = sum(muestras_Lq) / len(muestras_Lq)
    Wq = sum(esperas) / len(esperas) if esperas else 0.0
    util = tiempo_ocupado / (T * c)
    p_esperar = esperaron / llegadas if llegadas else 0.0
    p_bloqueo = bloqueados / llegadas if llegadas else 0.0

    return {
        "L": L,
        "Lq": Lq,
        "Wq": Wq,
        "utilizacion": util,
        "P_esperar": p_esperar,
        "P_bloqueo": p_bloqueo,
        "llegadas": llegadas,
    }


def replicas(lam, mu, c, horizonte, calentamiento, n_rep=30, con_espera=True):
    resultados = []
    for i in range(n_rep):
        resultados.append(simular(lam, mu, c, horizonte, calentamiento, semilla=42, con_espera=con_espera))
    resumen = {}
    for k in resultados[0]:
        vals = [r[k] for r in resultados]
        m = statistics.mean(vals)
        s = statistics.stdev(vals)
        h = 1.96 * s / math.sqrt(len(vals))
        resumen[k] = (m, m - h, m + h)
    return resumen


if __name__ == "__main__":
    lam, mu, c = 3.0, 0.25, 18
    print("Con espera:", replicas(lam, mu, c, 1000, 100, 30, True))
    print("Sin espera:", replicas(lam, mu, c, 1000, 100, 30, False))
