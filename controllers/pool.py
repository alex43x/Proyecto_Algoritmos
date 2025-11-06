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
        anio INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        dia INTEGER NOT NULL,
        horaDeInicio INTEGER NOT NULL,
        minuto INTEGER NOT NULL,
        fecha TEXT NOT NULL,
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
