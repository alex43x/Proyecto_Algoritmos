from controllers.torneo import insert_torneo
class Torneo:
    def __init__(self, nombreTorneo, sede, fechaDeInicio, fechaDeFin,):
        self.nombreTorneo = nombreTorneo
        self.sede = sede
        self.fechaDeInicio = fechaDeInicio
        self.fechaDeFin = fechaDeFin
    def guardar(self):
        insert_torneo(
            self.nombreTorneo,
            self.sede,
            str(self.fechaDeInicio),
            str(self.fechaDeFin)
        )
        print(f"Torneo '{self.nombreTorneo}' guardado correctamente en la base de datos.")
    
