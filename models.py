import datetime 
class Torneo:
    def __init__(self, nombre_torneo, sede, fecha_de_inicio, fecha_de_fin):
        self.nombre_torneo = nombre_torneo
        self.sede = sede
        self.fecha_de_inicio = fecha_de_inicio
        self.fecha_de_fin = fecha_de_fin
        
class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, grupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
        self.grupo = grupo

class partido:
    def __init__(self,anio , mes, dia, minuto, hora_de_inicio, identificador_equipo_uno, identificador_equipo_dos, goles_equipo_uno , goles_equipo_dos, tarjetas_amarillas_equipo_uno, tarjetas_amarillas_equipo_dos, tarjetas_rojas_equipo_uno, tarjetas_rojas_equipo_dos, id_partido, puntos_equipo_uno, puntos_equipo_dos, jornada):
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
        
      

        
        
        
        

    