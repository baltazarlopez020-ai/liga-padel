from models import Partido, Pareja
from config import PUNTOS_VICTORIA, PUNTOS_EMPATE, PUNTOS_DERROTA

def calcular_posiciones_por_categoria(categoria):
    posiciones = {}
    parejas = Pareja.query.filter_by(categoria=categoria).all()
    for p in parejas:
        posiciones[p.id] = {'pareja': p, 'PJ':0, 'PG':0, 'PE':0, 'PP':0, 'GF':0, 'GC':0, 'Puntos':0}
    partidos = Partido.query.filter_by(categoria=categoria).filter(Partido.played==True).all()
    for partido in partidos:
        a = partido.parejaA_id
        b = partido.parejaB_id
        if not partido.sets:
            continue
        s = partido.sets.strip()
        try:
            totalA = 0
            totalB = 0
            for seg in s.split(','):
                seg = seg.strip()
                if '-' in seg:
                    ga, gb = seg.split('-')
                elif ':' in seg:
                    ga, gb = seg.split(':')
                else:
                    continue
                totalA += int(ga)
                totalB += int(gb)
        except Exception:
            continue

        posiciones[a]['PJ'] += 1
        posiciones[b]['PJ'] += 1
        posiciones[a]['GF'] += totalA
        posiciones[a]['GC'] += totalB
        posiciones[b]['GF'] += totalB
        posiciones[b]['GC'] += totalA

        if totalA > totalB:
            posiciones[a]['PG'] += 1
            posiciones[b]['PP'] += 1
            posiciones[a]['Puntos'] += PUNTOS_VICTORIA
        elif totalA < totalB:
            posiciones[b]['PG'] += 1
            posiciones[a]['PP'] += 1
            posiciones[b]['Puntos'] += PUNTOS_VICTORIA
        else:
            posiciones[a]['PE'] += 1
            posiciones[b]['PE'] += 1
            posiciones[a]['Puntos'] += PUNTOS_EMPATE
            posiciones[b]['Puntos'] += PUNTOS_EMPATE

    tabla = []
    for pid, v in posiciones.items():
        v['DIF'] = v['GF'] - v['GC']
        tabla.append(v)
    tabla_sorted = sorted(tabla, key=lambda x: (x['Puntos'], x['DIF'], x['GF']), reverse=True)
    return tabla_sorted
