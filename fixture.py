from itertools import combinations
from models import Partido, Pareja, Enfrentamiento, db
from datetime import datetime, timedelta

def generar_round_robin_sin_historial(parejas, temporada=None, fecha_inicio=None):
    ids = [p.id for p in parejas]
    cruces = []
    for a, b in combinations(ids, 2):
        # chequear historial
        exists = Enfrentamiento.query.filter(
            ((Enfrentamiento.parejaA_id==a) & (Enfrentamiento.parejaB_id==b)) |
            ((Enfrentamiento.parejaA_id==b) & (Enfrentamiento.parejaB_id==a))
        ).first()
        if exists:
            continue
        cruces.append((a, b))
    # crear partidos
    fecha = fecha_inicio or datetime.utcnow()
    partidos = []
    for i, (a, b) in enumerate(cruces):
        p = Partido(fecha=fecha + timedelta(days=i), categoria=parejas[0].categoria, parejaA_id=a, parejaB_id=b)
        db.session.add(p)
        partidos.append(p)
    db.session.commit()
    return partidos
# fixture.py
def generate_round_robin(teams):
    teams = list(teams)
    # si menos de 2 equipos: nada
    if len(teams) < 2:
        return []
    if len(teams) % 2 == 1:
        teams.append("BYE")
    n = len(teams)
    half = n // 2
    rounds = []
    for r in range(n - 1):
        pairs = []
        for i in range(half):
            a = teams[i]
            b = teams[n - 1 - i]
            if a != "BYE" and b != "BYE":
                pairs.append((a,b))
        rounds.append(pairs)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    return rounds
