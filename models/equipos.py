from controllers.equipos import insert_equipo
class Equipos:
    def __init__(self, identificador, pais, abreviatura, confederacion, idGrupo):
        self.identificador = identificador
        self.pais = pais
        self.abreviatura = abreviatura
        self.confederacion = confederacion
        self.idGrupo = idGrupo
                
    def guardar(self):
        insert_equipo(
            self.identificador,
            self.pais,
            self.abreviatura,
            self.confederacion,
            self.idGrupo
        )
        print(f"Equipo '{self.pais}' guardado correctamente en la base de datos.")