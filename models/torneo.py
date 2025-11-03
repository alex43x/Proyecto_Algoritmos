from database import insert_torneo
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

