import datetime 

class Torneo:
    def __init__(self, nombre_torneo, sede, fecha_de_inicio, fecha_de_fin, grupos):
        self.nombre_torneo = nombre_torneo
        self.sede = sede
        self.fecha_de_inicio = fecha_de_inicio
        self.fecha_de_fin = fecha_de_fin
    def partidos_por_fecha(self, fecha, lista_partidos):
        # Muestra los partidos que se juegan en una fecha dada
            print(f"Partidos del {fecha.strftime('%d/%m/%Y')}")
            for p in lista_partidos:
                if p.fecha.date() == fecha.date():
                    print(f"{p.identificador_equipo_uno} vs {p.identificador_equipo_dos} - {p.hora_de_inicio}:{p.minuto:02d}")     

class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, grupo, id_grupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
        self.grupo = grupo
        self.id_grupo = id_grupo
    def mostrar_resultados(self, lista_partidos):
        # Muestra los resultados de todos los partidos de este equipo
        print(f"\nResultados de {self.pais}:")
        for p in lista_partidos:
            if p.identificador_equipo_uno == self.identidicador or p.identificador_equipo_dos == self.identificador:
                print(f"{p.fecha.strftime('%d/%m/Y')} - {p.identificador_equipo_uno} {p.goles_equipo_dos} {p.identificador_equipo_dos}")
    
class Partido:
    def __init__(self, anio ,mes ,dia , minuto, hora_de_inicio, identificador_equipo_uno, identificador_equipo_dos, goles_equipo_uno , goles_equipo_dos, tarjetas_amarillas_equipo_uno, tarjetas_amarillas_equipo_dos, tarjetas_rojas_equipo_uno, tarjetas_rojas_equipo_dos, id_partido, puntos_equipo_uno, puntos_equipo_dos, jornada):
        self.amio = anio
        self.mes = mes
        self.dia = dia
        self.minuto = minuto
        self.hora_de_inicio = hora_de_inicio
        self.fecha = datetime(anio, mes, dia, hora_de_inicio, minuto)
        self.identificador_equipo_uno = identificador_equipo_uno
        self.identificador_equipo_dos = identificador_equipo_dos
        self.goles_equipo_uno = goles_equipo_uno
        self.goles_equipo_dos = goles_equipo_dos
        self.tarjetas_amarillas_equipo_uno = tarjetas_amarillas_equipo_uno
        self.tarjetas_amarillas_equipo_dos = tarjetas_amarillas_equipo_dos
        self.tarjetas_rojas_equipo_uno = tarjetas_rojas_equipo_uno
        self.tarjetas_rojas_equipo_dos = tarjetas_rojas_equipo_dos
        self.id_partido = id_partido
        self.puntos_equipo_uno = puntos_equipo_uno
        self.puntos_equipo_dos = puntos_equipo_dos
        self.jornada = jornada
    def mostrar_partido(self):
        print(f"{self.fecha.strftime('%d/%m/%Y')} - {self.identificador_equipo_uno} {self.goles_equipo_uno}:{self.goles_equipo_dos} {self.identificador_equipo_dos}")

class Grupos:
    def __init__(self, id_grupo, nombre_grupo ):
        self.id_grupo = id_grupo
        self.nombre_grupo = nombre_grupo
    def mostrar_tabla(self, lista_equipos):
        # Muestra la tabla de posiciones del grupo
        equipos_grupo = [k for k in lista_equipos if k.id_grupo == self.id_grupo]
        equipos_ordenados = sorted(equipos_grupo, key = lambda x: x.puntos, reverse = True)
        
        print(f"\nTabla del grupo {self.nombre_grupo}:")
        print("Equipo\tPuntos")
        for k in equipos_ordenados:
            print(f"{k.pais}\t{k.puntos}")

        
        
        
        

    