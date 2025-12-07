from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

EXCEL_PATH = BASE_DIR / 'MiLigaPadel.xlsx'
DB_PATH = DATA_DIR / 'liga.db'

# Puntajes configurables
PUNTOS_VICTORIA = 3
PUNTOS_EMPATE = 1
PUNTOS_DERROTA = 0
