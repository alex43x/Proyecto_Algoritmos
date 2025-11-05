from controllers.equipos import insert_equipo
class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, idGrupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
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
            self.idGrupo
        )
        print(f"Equipo '{self.pais}' guardado correctamente en la base de datos.")