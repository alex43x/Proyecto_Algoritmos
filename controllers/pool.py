import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "torneo.db")

def conectar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS torneo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreTorneo TEXT NOT NULL UNIQUE,
        sede TEXT NOT NULL UNIQUE,
        fechaDeInicio TEXT NOT NULL UNIQUE,
        fechaDeFin TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS grupos(
        idGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreGrupo TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS equipos (
        identificador TEXT PRIMARY KEY,
        pais TEXT NOT NULL ,
        abreviatura TEXT NOT NULL ,
        confederacion TEXT NOT NULL ,
        grupo INTEGER NOT NULL,
        FOREIGN KEY (grupo) REFERENCES grupos(idGrupo)
    );

    CREATE TABLE IF NOT EXISTS partido (
        idPartido INTEGER PRIMARY KEY,
        fecha TEXT,
        hora TEXT,
        identificadorEquipoUno INTEGER NOT NULL,
        identificadorEquipoDos INTEGER NOT NULL,
        golesEquipoUno INTEGER NOT NULL,
        golesEquipoDos INTEGER NOT NULL,
        tarjetasAmarillasEquipoUno INTEGER NOT NULL,
        tarjetasAmarillasEquipoDos INTEGER NOT NULL,
        tarjetasRojasEquipoUno INTEGER NOT NULL,
        tarjetasRojasEquipoDos INTEGER NOT NULL,
        puntosEquipoUno INTEGER NOT NULL,
        puntosEquipoDos INTEGER NOT NULL,
        jornada INTEGER NOT NULL,
        FOREIGN KEY (identificadorEquipoUno) REFERENCES equipos(identificador),
        FOREIGN KEY (identificadorEquipoDos) REFERENCES equipos(identificador)
    );
    """)
    conn.commit()
    conn.close()
def crear_partidos_fase_grupos():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.executescript("""
    INSERT INTO partido (fecha, hora, identificadorEquipoUno, identificadorEquipoDos, golesEquipoUno, golesEquipoDos, tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos, tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, puntosEquipoUno, puntosEquipoDos, jornada) VALUES
    -- Jornada 1
    ('', '', 'A1', 'A2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'A3', 'A4', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'B1', 'B2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'B3', 'B4', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'C1', 'C2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'C3', 'C4', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'D1', 'D2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'D3', 'D4', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'E1', 'E2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'E3', 'E4', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'F1', 'F2', 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'F3', 'F4', 0, 0, 0, 0, 0, 0, 0, 0, 1),

    -- Jornada 2
    ('', '', 'A1', 'A3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'A4', 'A2', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'B1', 'B3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'B4', 'B2', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'C1', 'C3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'C4', 'C2', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'D1', 'D3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'D4', 'D2', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'E1', 'E3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'E4', 'E2', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'F1', 'F3', 0, 0, 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'F4', 'F2', 0, 0, 0, 0, 0, 0, 0, 0, 2),

    -- Jornada 3
    ('', '', 'A4', 'A1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'A2', 'A3', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'B4', 'B1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'B2', 'B3', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'C4', 'C1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'C2', 'C3', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'D4', 'D1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'D2', 'D3', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'E4', 'E1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'E2', 'E3', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'F4', 'F1', 0, 0, 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'F2', 'F3', 0, 0, 0, 0, 0, 0, 0, 0, 3);
    """)
    
    conn.commit()
    conn.close()
    print("Partidos de la fase de grupos creados exitosamente")