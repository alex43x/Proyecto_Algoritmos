import datetime

class Torneo:
    def __init__(self, nombreTorneo, sede, fechaDeInicio, fechaDeFin):
        self.nombreTorneo = nombreTorneo
        self.sede = sede
        self.fechaDeInicio = fechaDeInicio
        self.fechaDeFin = fechaDeFin
        

class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, grupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
        self.grupo = grupo


class Partido:
    def __init__(self, anio, mes, dia, minuto, horaDeInicio,identificadorEquipoUno, identificadorEquipoDos,golesEquipoUno, golesEquipoDos,tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,idPartido, puntosEquipoUno, puntosEquipoDos, jornada):
        self.anio = anio
        self.mes = mes
        self.dia = dia
        self.minuto = minuto
        self.horaDeInicio = horaDeInicio
        self.fecha = datetime.datetime(anio, mes, dia, horaDeInicio, minuto)
        self.identificadorEquipoUno = identificadorEquipoUno
        self.identificadorEquipoDos = identificadorEquipoDos
        self.golesEquipoUno = golesEquipoUno
        self.golesEquipoDos = golesEquipoDos
        self.tarjetasAmarillasEquipoUno = tarjetasAmarillasEquipoUno
        self.tarjetasAmarillasEquipoDos = tarjetasAmarillasEquipoDos
        self.tarjetasRojasEquipoUno = tarjetasRojasEquipoUno
        self.tarjetasRojasEquipoDos = tarjetasRojasEquipoDos
        self.idPartido = idPartido
        self.puntosEquipoUno = puntosEquipoUno
        self.puntosEquipoDos = puntosEquipoDos
        self.jornada = jornada