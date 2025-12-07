import pandas as pd

def parse_excel(file_storage):
    # file_storage: objeto werkzeug FileStorage (desde request.files)
    # Asumimos que el excel tiene columnas: Nombre (o Jugador1,Jugador2) y Categoria
    df = pd.read_excel(file_storage)
    # adaptar a tu hoja: busco columnas comunes
    if "Nombre" in df.columns:
        df["nombre"] = df["Nombre"]
    elif "Pareja" in df.columns:
        df["nombre"] = df["Pareja"]
    else:
        # si vienen separados jugadores:
        if "Jugador1" in df.columns and "Jugador2" in df.columns:
            df["nombre"] = df["Jugador1"].astype(str) + " / " + df["Jugador2"].astype(str)
        else:
            raise ValueError("Columnas esperadas: 'Nombre' o 'Pareja' o ('Jugador1' y 'Jugador2')")

    if "Categoria" not in df.columns:
        raise ValueError("La hoja debe tener columna 'Categoria'")

    pairs = []
    for _, row in df.iterrows():
        pairs.append({"nombre": str(row["nombre"]).strip(), "categoria": str(row["Categoria"]).strip()})
    return pairs
