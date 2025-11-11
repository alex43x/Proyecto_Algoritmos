import sqlite3
import os

    # Obtiene la ruta base del archivo actual (carpeta del modulo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Construye la ruta completa a la base de datos dentro de la carpeta "data"
DB_PATH = os.path.join(BASE_DIR, "..", "data", "torneo.db")

def conectar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

    # Crea todas las tablas necesarias para el sistema si aun no existen
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS torneo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreTorneo TEXT NOT NULL UNIQUE,
        sede TEXT NOT NULL UNIQUE,
        fechaDeInicio TEXT NOT NULL UNIQUE,
        fechaDeFin TEXT NOT NULL UNIQUE,
        jornada INTEGER NOT NULL DEFAULT 1
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
        identificadorEquipoUno TEXT,
        identificadorEquipoDos TEXT,
        golesEquipoUno INTEGER NOT NULL,
        golesEquipoDos INTEGER NOT NULL,
        tarjetasAmarillasEquipoUno INTEGER NOT NULL,
        tarjetasAmarillasEquipoDos INTEGER NOT NULL,
        tarjetasRojasEquipoUno INTEGER NOT NULL,
        tarjetasRojasEquipoDos INTEGER NOT NULL,
        jornada INTEGER NOT NULL,
        FOREIGN KEY (identificadorEquipoUno) REFERENCES equipos(identificador),
        FOREIGN KEY (identificadorEquipoDos) REFERENCES equipos(identificador)
    );
    """)
    conn.commit()
    conn.close()
    # Inserta los partidos predefinidos de las 3 jornadas de la fase de grupos
def crear_partidos_fase_grupos():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.executescript("""
    INSERT INTO partido (fecha, hora, identificadorEquipoUno, identificadorEquipoDos, golesEquipoUno, golesEquipoDos, tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos, tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, jornada) VALUES
    -- Jornada 1
    ('', '', 'A1', 'A2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'A3', 'A4', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'B1', 'B2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'B3', 'B4', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'C1', 'C2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'C3', 'C4', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'D1', 'D2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'D3', 'D4', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'E1', 'E2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'E3', 'E4', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'F1', 'F2', 0, 0, 0, 0, 0, 0, 1),
    ('', '', 'F3', 'F4', 0, 0, 0, 0, 0, 0, 1),

    -- Jornada 2
    ('', '', 'A1', 'A3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'A4', 'A2', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'B1', 'B3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'B4', 'B2', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'C1', 'C3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'C4', 'C2', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'D1', 'D3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'D4', 'D2', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'E1', 'E3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'E4', 'E2', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'F1', 'F3', 0, 0, 0, 0, 0, 0, 2),
    ('', '', 'F4', 'F2', 0, 0, 0, 0, 0, 0, 2),

    -- Jornada 3
    ('', '', 'A4', 'A1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'A2', 'A3', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'B4', 'B1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'B2', 'B3', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'C4', 'C1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'C2', 'C3', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'D4', 'D1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'D2', 'D3', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'E4', 'E1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'E2', 'E3', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'F4', 'F1', 0, 0, 0, 0, 0, 0, 3),
    ('', '', 'F2', 'F3', 0, 0, 0, 0, 0, 0, 3);
    """)
    
    conn.commit()
    conn.close()
    print("Partidos de la fase de grupos creados exitosamente")
def crear_partidos_fase_final():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.executescript("""
    INSERT INTO partido (fecha, hora, identificadorEquipoUno, identificadorEquipoDos, golesEquipoUno, golesEquipoDos, tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos, tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, jornada) VALUES
    -- Octavos de Final/8 PARTIDOS/J4
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 4),
    --Cuartos de Final/4 PARTIDOS/J5
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 5),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 5),
    --Semifinal/2 PARTIDOS/J6 
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 6),
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 6),
    --3er Puesto /1 PARTIDO/J7
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 7),
    --Final /1 PARTIDO/J8
    ('', '', '', '', 0, 0, 0, 0, 0, 0, 8);
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
               tarjetasRojasEquipoUno, tarjetasRojasEquipoDos
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
                tarjetasRojasEquipoUno = ?, tarjetasRojasEquipoDos = ?
            WHERE idPartido = ? AND jornada = ?;
        """, (*datos, id_partido, jornada))
    conn.commit()
    conn.close()
    print(f"Detalles (goles, tarjetas) actualizados correctamente para la jornada {jornada}.")
#para asignar cuartos, busca la jornada anterior, guarda, define, busca la actual, actualiza y no retorna nada ya qu esolo es para actualizar la platilla.
def asignar_cuartos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, identificadorEquipoUno, identificadorEquipoDos,
               golesEquipoUno, golesEquipoDos
        FROM partido
        WHERE jornada = 4
        ORDER BY idPartido ASC;
    """)
    partidos = cursor.fetchall()
    ganadores = []
    for id_partido, eq1, eq2, g1, g2 in partidos:
        if g1 > g2:
            ganadores.append(eq1)
        else:
            ganadores.append(eq2)
    enfrentamientos = []
    for j in range(0, len(ganadores), 2):
        equipo_uno = ganadores[j]
        equipo_dos = ganadores[j + 1]
        enfrentamientos.append((equipo_uno, equipo_dos))
    cursor.execute("""
        SELECT idPartido
        FROM partido
        WHERE jornada = 5
        ORDER BY idPartido ASC;
    """)
    partidos_cuartos = cursor.fetchall()
    k = 0
    for fila in partidos_cuartos:
        id_partido = fila[0]
        equipo_uno = enfrentamientos[k][0]
        equipo_dos = enfrentamientos[k][1]

        cursor.execute("""
            UPDATE partido
            SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
            WHERE idPartido = ?;
        """, (equipo_uno, equipo_dos, id_partido))

        k += 1
    conn.commit()
    conn.close()
    print("Enfrentamientos de los Cuartos de Final asignados correctamente.")
    
#asignar semifinales , misma logica que los de cuartos 
def asignar_semifinales():
    conn = conectar()
    cursor = conn.cursor()
    # Obtener los ganadores de los cuartos (jornada 5)
    cursor.execute("""
        SELECT identificadorEquipoUno, identificadorEquipoDos,
               golesEquipoUno, golesEquipoDos
        FROM partido
        WHERE jornada = 5
        ORDER BY idPartido ASC;
    """)
    partidos_cuartos = cursor.fetchall()
    ganadores = []
    for fila in partidos_cuartos:
        equipo_uno = fila[0]
        equipo_dos = fila[1]
        goles_uno = fila[2]
        goles_dos = fila[3]

        if goles_uno > goles_dos:
            ganadores.append(equipo_uno)
        else:
            ganadores.append(equipo_dos)
    # Crear los enfrentamientos (1 vs 2, 3 vs 4)
    enfrentamientos = []
    i = 0
    while i < len(ganadores):
        equipo_uno = ganadores[i]
        equipo_dos = ganadores[i + 1]
        enfrentamientos.append((equipo_uno, equipo_dos))
        i = i + 2
    # Asignar los equipos ganadores a los partidos de semifinales (jornada 6)
    cursor.execute("""
        SELECT idPartido
        FROM partido
        WHERE jornada = 6
        ORDER BY idPartido ASC;
    """)
    partidos_semifinal = cursor.fetchall()
    for f in range(len(partidos_semifinal)):
        id_partido = partidos_semifinal[f][0]
        equipo_uno = enfrentamientos[f][0]
        equipo_dos = enfrentamientos[f][1]

        cursor.execute("""
            UPDATE partido
            SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
            WHERE idPartido = ?;
        """, (equipo_uno, equipo_dos, id_partido))
    conn.commit()
    conn.close()
    print("Equipos de semifinales asignados correctamente en la jornada 6.")
#para asignar las finales, misma logica que las anteriores, solo con la diferencia que guarda los persdedores para el tercer puesto.
def asignar_tercer_puesto():
    conn = conectar()
    cursor = conn.cursor()
    # Traer semifinales (jornada 6)
    cursor.execute("""
        SELECT identificadorEquipoUno, identificadorEquipoDos,
               golesEquipoUno, golesEquipoDos
        FROM partido
        WHERE jornada = 6
        ORDER BY idPartido ASC;
    """)
    partidos_semis = cursor.fetchall()
    # Determinar perdedores directamente
    perdedores = []
    for eq1, eq2, g1, g2 in partidos_semis:
        if g1 > g2:
            perdedores.append(eq2)
        else:
            perdedores.append(eq1)

    # Obtener el partido del tercer puesto (jornada 7)
    cursor.execute("""
        SELECT idPartido
        FROM partido
        WHERE jornada = 7
        ORDER BY idPartido ASC;
    """)
    fila = cursor.fetchone()

    if fila is not None:
        id_partido = fila[0]

        equipo_uno = perdedores[0]
        equipo_dos = perdedores[1]

        cursor.execute("""
            UPDATE partido
            SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
            WHERE idPartido = ?;
        """, (equipo_uno, equipo_dos, id_partido))

        print("Equipos del 3er puesto asignados correctamente en la jornada 7.")
    else:
        print("No existe partido asignado para la jornada 7.")

    conn.commit()
    conn.close()
def asignar_final():
    conn = conectar()
    cursor = conn.cursor()

    # Traer semifinales (jornada 6)
    cursor.execute("""
        SELECT identificadorEquipoUno, identificadorEquipoDos,
               golesEquipoUno, golesEquipoDos
        FROM partido
        WHERE jornada = 6
        ORDER BY idPartido ASC;
    """)
    partidos_semis = cursor.fetchall()

    # Determinar ganadores directamente
    ganadores = []
    for eq1, eq2, g1, g2 in partidos_semis:
        if g1 > g2:
            ganadores.append(eq1)
        else:
            ganadores.append(eq2)

    # Obtener el partido de la FINAL (jornada 8)
    cursor.execute("""
        SELECT idPartido
        FROM partido
        WHERE jornada = 8
        ORDER BY idPartido ASC;
    """)
    fila = cursor.fetchone()

    if fila is not None:
        id_partido = fila[0]

        equipo_uno = ganadores[0]
        equipo_dos = ganadores[1]

        cursor.execute("""
            UPDATE partido
            SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
            WHERE idPartido = ?;
        """, (equipo_uno, equipo_dos, id_partido))

        print("Equipos de la FINAL asignados correctamente en la jornada 8.")
    else:
        print("No existe partido asignado para la jornada 8.")
    conn.commit()
    conn.close()
#OJO todo esto pensado que para definir 4tos ya esta totalmente cargado la platilla de 8vos, 4tos para semis y semis para final.
