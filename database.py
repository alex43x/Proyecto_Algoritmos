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
        sede TEXT NOT NULL,
        fechaDeInicio TEXT NOT NULL,
        fechaDeFin TEXT NOT NULL
    );
     CREATE TABLE IF NOT EXISTS grupos(
        idGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreGrupo NOT NULL
    );
    CREATE TABLE IF NOT EXISTS equipos (
        identificador TEXT PRIMARY KEY,
        pais TEXT NOT NULL,
        abreviatura TEXT NOT NULL,
        confederacion TEXT NOT NULL,
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

def insert_equipo(identificador, pais, abreviatura, confederacion, idGrupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO equipos (identificador, pais, abreviatura, confederacion, idGrupo)
        VALUES ( ?, ?, ?, ?, ?)
    """, (identificador, pais, abreviatura, confederacion, idGrupo))
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
def insert_grupo(nombreGrupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO grupos (nombreGrupo)
        Values (?)
    """, ( nombreGrupo))
    conn.commit()
    conn.close()
def conectar():
    # Abre una conexión con la base de datos SQLite.
    return sqlite3.connect(DB_PATH)
