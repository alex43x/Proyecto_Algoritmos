import sqlite3
import os

DB_PATH = os.path.join("data", "torneo.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS torneo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreTorneo TEXT NOT NULL,
        sede TEXT,
        fechaDeInicio TEXT,
        fechaDeFin TEXT
    );

    CREATE TABLE IF NOT EXISTS equipos (
        identificador INTEGER PRIMARY KEY,
        pais TEXT NOT NULL,
        abreviatura TEXT,
        confederacion TEXT,
        grupo TEXT
    );

    CREATE TABLE IF NOT EXISTS partido (
        idPartido INTEGER PRIMARY KEY,
        anio INTEGER,
        mes INTEGER,
        dia INTEGER,
        horaDeInicio INTEGER,
        minuto INTEGER,
        fecha TEXT,
        identificadorEquipoUno INTEGER,
        identificadorEquipoDos INTEGER,
        golesEquipoUno INTEGER,
        golesEquipoDos INTEGER,
        tarjetasAmarillasEquipoUno INTEGER,
        tarjetasAmarillasEquipoDos INTEGER,
        tarjetasRojasEquipoUno INTEGER,
        tarjetasRojasEquipoDos INTEGER,
        puntosEquipoUno INTEGER,
        puntosEquipoDos INTEGER,
        jornada INTEGER,
        FOREIGN KEY (identificadorEquipoUno) REFERENCES equipos(identificador),
        FOREIGN KEY (identificadorEquipoDos) REFERENCES equipos(identificador)
    );
    """)
    conn.commit()
    conn.close()

# FUNCIONES DE ACCESO A LA BASE
def insert_torneo(nombreTorneo, sede, fechaDeInicio, fechaDeFin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO torneo (nombreTorneo, sede, fechaDeInicio, fechaDeFin)
        VALUES (?, ?, ?, ?)
    """, (nombreTorneo, sede, fechaDeInicio, fechaDeFin))
    conn.commit()
    conn.close()

def insert_equipo(identificador, pais, abreviatura, confederacion, grupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO equipos (identificador, pais, abreviatura, confederacion, grupo)
        VALUES (?, ?, ?, ?, ?)
    """, (identificador, pais, abreviatura, confederacion, grupo))
    conn.commit()
    conn.close()

def insert_partido(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO partido (
            idPartido, anio, mes, dia, horaDeInicio, minuto, fecha,
            identificadorEquipoUno, identificadorEquipoDos,
            golesEquipoUno, golesEquipoDos,
            tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
            tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,
            puntosEquipoUno, puntosEquipoDos, jornada
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()