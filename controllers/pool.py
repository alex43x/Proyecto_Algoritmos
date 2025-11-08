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
def crear_partidos_fase_final():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.executescript("""
    INSERT INTO partido (fecha, hora, identificadorEquipoUno, identificadorEquipoDos, golesEquipoUno, golesEquipoDos, tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos, tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, puntosEquipoUno, puntosEquipoDos, jornada) VALUES
    -- Octavos de Final/8 PARTIDOS/J4
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 4),
    --Cuartos de Final/4 PARTIDOS/J5
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 5),
    --Semifinal/2 PARTIDOS/J6 
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 6),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 6);
    --Final y 3er Puesto /2 PARTIDOS/J7
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 7),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 7);
    """)
    conn.commit()
    conn.close()
    print("Partidos de la fase eliminatoria creados exitosamente")
#que viene ya de definir_enfretamientos_octavos
#dicha lista trae (id_partido, id1, pais1, id2, pais2)
def asignar_octavos(enfrentamientos_octavos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido
        FROM partido
        WHERE jornada = 4
        ORDER BY idPartido ASC;
    """)
    partidos_j4 = cursor.fetchall()
    for i in range(len(partidos_j4)):
        id_partido_bd = partidos_j4[i][0]
        id1 = enfrentamientos_octavos[i][1]  # identificador del equipo 1
        id2 = enfrentamientos_octavos[i][3]  # identificador del equipo 2

        cursor.execute("""
            UPDATE partido
            SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
            WHERE idPartido = ? AND jornada = 4;
        """, (id1, id2, id_partido_bd))
    conn.commit()
    conn.close()
    print("Equipos de octavos asignados correctamente en la jornada 4.")
#pongo extra ya que en update_partido_sin_jugar de controllers.partidos
#pide equipos-fecha , pero en caso de las eliminatorias, el codigo debe asignar 
#los enfrentamientos, entonces los detales y fecha deben poner el usuario.
#esos dos son generales ya que los cuartos, semis y final van a adquirir la misma metodologia.
def actualizar_fechas_eliminatorias(jornada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, fecha, hora
        FROM partido
        WHERE jornada = ?
        ORDER BY idPartido ASC;
    """, (jornada,))
    partidos = cursor.fetchall()
    for id_partido, fecha, hora in partidos:
        cursor.execute("""
            UPDATE partido
            SET fecha = ?, hora = ?
            WHERE idPartido = ? AND jornada = ?;
        """, (fecha, hora, id_partido, jornada))
    conn.commit()
    conn.close()
    print(f"Fechas y horas actualizadas correctamente para la jornada {jornada}.")
def actualizar_detalles_eliminatorias(jornada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido,
               golesEquipoUno, golesEquipoDos,
               tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
               tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,
               puntosEquipoUno, puntosEquipoDos
        FROM partido
        WHERE jornada = ?
        ORDER BY idPartido ASC;
    """, (jornada,))
    partidos = cursor.fetchall()
    for detalle in partidos:
        id_partido = detalle[0]
        datos = detalle[1:]  # para no tocar id_partidos 
        cursor.execute("""
            UPDATE partido
            SET golesEquipoUno = ?, golesEquipoDos = ?,
                tarjetasAmarillasEquipoUno = ?, tarjetasAmarillasEquipoDos = ?,
                tarjetasRojasEquipoUno = ?, tarjetasRojasEquipoDos = ?,
                puntosEquipoUno = ?, puntosEquipoDos = ?
            WHERE idPartido = ? AND jornada = ?;
        """, (*datos, id_partido, jornada))
    conn.commit()
    conn.close()
    print(f"Detalles (goles, tarjetas, puntos) actualizados correctamente para la jornada {jornada}.")