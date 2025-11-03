from database import insert_torneo,insert_equipo
import datetime
import random

class Torneo:
    def __init__(self, nombreTorneo, sede, fechaDeInicio, fechaDeFin):
        self.nombreTorneo = nombreTorneo
        self.sede = sede
        self.fechaDeInicio = fechaDeInicio
        self.fechaDeFin = fechaDeFin

    def partidosPorFecha(self, fecha, listaPartidos):
        # Muestra los partidos que se juegan en una fecha dada
        print(f"Partidos del {fecha.strftime('%d/%m/%Y')}")
        for p in listaPartidos:
            if p.fecha.date() == fecha.date():
                print(f"{p.identificadorEquipoUno} vs {p.identificadorEquipoDos} - {p.horaDeInicio}:{p.minuto:02d}")

    def sorteoGrupos(self, listaEquipos, grupos, maxEuropa=2):
        random.shuffle(listaEquipos)
        asignaciones = {g.idGrupo: [] for g in grupos}
        for equipo in listaEquipos:
            asignado = False
            random.shuffle(grupos)
            for grupo in grupos:
                confeds = [e.confederacion for e in asignaciones[grupo.idGrupo]]
                if equipo.confederacion not in confeds:
                    asignaciones[grupo.idGrupo].append(equipo)
                    equipo.idGrupo = grupo.idGrupo
                    asignado = True
                    break
                if equipo.confederacion == "UEFA" and confeds.count("UEFA") < maxEuropa:
                    asignaciones[grupo.idGrupo].append(equipo)
                    equipo.idGrupo = grupo.idGrupo
                    asignado = True
                    break
            if not asignado:
                print(f" No se pudo asignar el equipo {equipo.nombre} (confederación: {equipo.confederacion}).")

        print(" Resultado del sorteo:")
        for grupo in grupos:
            print(f"Grupo {grupo.nombreGrupo}:")
            for e in asignaciones[grupo.idGrupo]:
                print(f"  - {e.nombre} ({e.confederacion})")

        return asignaciones
    
    def guardar(self):
        insert_torneo(
            self.nombreTorneo,
            self.sede,
            str(self.fechaDeInicio),
            str(self.fechaDeFin)
        )
        print(f"Torneo '{self.nombreTorneo}' guardado correctamente en la base de datos.")


class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, grupo, idGrupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
        self.grupo = grupo
        self.idGrupo = idGrupo

    def mostrarResultados(self, listaPartidos):
        # Muestra los resultados de todos los partidos de este equipo
        print(f"\nResultados de {self.pais}:")
        for p in listaPartidos:
            if p.identificadorEquipoUno == self.identificador or p.identificadorEquipoDos == self.identificador:
                print(f"{p.fecha.strftime('%d/%m/%Y')} - {p.identificadorEquipoUno} {p.golesEquipoUno}:{p.golesEquipoDos} {p.identificadorEquipoDos}")
                
    def guardar(self):
        insert_equipo(
            self.identificador,
            self.pais,
            self.abreviatura,
            self.confederacion,
            self.grupo,
            self.idGrupo
        )
        print(f"Equipo '{self.pais}' guardado correctamente en la base de datos.")


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


class Grupos:
    def __init__(self, idGrupo, nombreGrupo):
        self.idGrupo = idGrupo
        self.nombreGrupo = nombreGrupo

    def mostrarTabla(self, listaEquipos):
        # Muestra la tabla de posiciones del grupo
        equiposGrupo = [k for k in listaEquipos if k.idGrupo == self.idGrupo]
        equiposOrdenados = sorted(equiposGrupo, key=lambda x: x.puntos, reverse=True)

        print(f"Tabla del grupo {self.nombreGrupo}:")
        print("Equipo\tPuntos")
        for k in equiposOrdenados:
            print(f"{k.pais}\t{k.puntos}")




        
        

    