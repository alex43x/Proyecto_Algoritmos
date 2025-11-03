import datetime
class Partido:
    def __init__(self, anio, mes, dia, minuto, horaDeInicio, identificadorEquipoUno, identificadorEquipoDos,
                 golesEquipoUno, golesEquipoDos, tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
                 tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, idPartido, puntosEquipoUno, puntosEquipoDos, jornada):
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

    def mostrarPartido(self):
        print(f"{self.fecha.strftime('%d/%m/%Y')} - {self.identificadorEquipoUno} {self.golesEquipoUno}:{self.golesEquipoDos} {self.identificadorEquipoDos}")

