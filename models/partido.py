import datetime
import random
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
        self.eventos = []  # Lista de eventos generados (minuto, descripción)

    def simularPartido(self, porcentajeDeOcurrencia):
        """
        Simula un partido de fútbol entre equipoUno y equipoDos.
        porcentajeDeOcurrencia: probabilidad (en %) de que ocurra un evento en cada minuto.
        """
        # 11 jugadores por equipo
        jugadoresEquipoUno = [0] * 11
        jugadoresEquipoDos = [0] * 11

        prob = porcentajeDeOcurrencia / 100.0  # Ej: 10 → 0.10

        # Simular los 90 minutos
        for minuto in range(91):
            if random.random() < prob:
                eventoAleatorio = random.randint(0, 8)
                jugador = minuto % 11  # Jugador involucrado (0-10)
                descripcion = ""

                # Determinar tipo de evento
                if eventoAleatorio == 1:
                    descripcion = f"Min {minuto}: Falta a favor sin amonestación rival"
                elif eventoAleatorio == 2:
                    descripcion = f"Min {minuto}: Falta a favor con amarilla rival (jugador {jugador + 1})"
                    self.tarjetasAmarillasEquipoDos += 1
                    jugadoresEquipoDos[jugador] += 1
                elif eventoAleatorio == 3:
                    descripcion = f"Min {minuto}: Expulsión directa rival (jugador {jugador + 1})"
                    self.tarjetasRojasEquipoDos += 1
                    jugadoresEquipoDos[jugador] += 2
                elif eventoAleatorio == 4:
                    descripcion = f"Min {minuto}: Falta en contra sin amonestación"
                elif eventoAleatorio == 5:
                    descripcion = f"Min {minuto}: Falta en contra con amarilla nuestra (jugador {jugador + 1})"
                    self.tarjetasAmarillasEquipoUno += 1
                    jugadoresEquipoUno[jugador] += 1
                elif eventoAleatorio == 6:
                    descripcion = f"Min {minuto}: Expulsión directa nuestra (jugador {jugador + 1})"
                    self.tarjetasRojasEquipoUno += 1
                    jugadoresEquipoUno[jugador] += 2
                elif eventoAleatorio == 7:
                    descripcion = f"Min {minuto}: 🥅 ¡GOL de {self.identificadorEquipoUno}!"
                    self.golesEquipoUno += 1
                elif eventoAleatorio == 8:
                    descripcion = f"Min {minuto}: 🥅 ¡GOL de {self.identificadorEquipoDos}!"
                    self.golesEquipoDos += 1
                else:
                    descripcion = f"Min {minuto}: Nada ocurrió"

                # Guardar el evento en la lista
                self.eventos.append(descripcion)

        # Crear y devolver un resumen del partido
        resumen = {
            "equipoUno": self.identificadorEquipoUno,
            "equipoDos": self.identificadorEquipoDos,
            "resultado": f"{self.golesEquipoUno}-{self.golesEquipoDos}",
            "amarillas": (self.tarjetasAmarillasEquipoUno, self.tarjetasAmarillasEquipoDos),
            "rojas": (self.tarjetasRojasEquipoUno, self.tarjetasRojasEquipoDos),
            "eventosTotales": len(self.eventos),
            "detalleEventos": self.eventos
        }

        return resumen
    

    def mostrarPartido(self):
        print(f"{self.fecha.strftime('%d/%m/%Y')} - {self.identificadorEquipoUno} {self.golesEquipoUno}:{self.golesEquipoDos} {self.identificadorEquipoDos}")

