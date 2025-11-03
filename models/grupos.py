from database import insert_grupo
class Grupos:
    def __init__(self, idGrupo, nombreGrupo):
        self.idGrupo = idGrupo
        self.nombreGrupo = nombreGrupo
    def guardarG(self):
            insert_grupo(
                self.idGrupo,
                self.nombreGrupo
            )
            print(f"Grupo {self.nombreGrupo} Guardado correctamente en la base de datos")
    def mostrarTabla(self, listaEquipos):
        # Muestra la tabla de posiciones del grupo
        equiposGrupo = [k for k in listaEquipos if k.idGrupo == self.idGrupo]
        equiposOrdenados = sorted(equiposGrupo, key=lambda x: x.puntos, reverse=True)

        print(f"Tabla del grupo {self.nombreGrupo}:")
        print("Equipo\tPuntos")
        for k in equiposOrdenados:
            print(f"{k.pais}\t{k.puntos}")
