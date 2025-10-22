from database import insert_torneo, insert_equipo, insert_partido
from models import Torneo, Equipos, Partido

# CONTROLADORES DE SINCRONIZACIÓN
def guardar_torneo(torneo: Torneo):
    insert_torneo(torneo.nombreTorneo, torneo.sede, torneo.fechaDeInicio, torneo.fechaDeFin)

def guardar_equipo(equipo: Equipos):
    insert_equipo(equipo.identificador, equipo.pais, equipo.abreviatura, equipo.confederacion, equipo.grupo)

def guardar_partido(partido: Partido):
    datos = (
        partido.idPartido, partido.anio, partido.mes, partido.dia,
        partido.horaDeInicio, partido.minuto,
        partido.fecha.strftime("%Y-%m-%d %H:%M"),
        partido.identificadorEquipoUno, partido.identificadorEquipoDos,
        partido.golesEquipoUno, partido.golesEquipoDos,
        partido.tarjetasAmarillasEquipoUno, partido.tarjetasAmarillasEquipoDos,
        partido.tarjetasRojasEquipoUno, partido.tarjetasRojasEquipoDos,
        partido.puntosEquipoUno, partido.puntosEquipoDos, partido.jornada
    )
    insert_partido(datos)