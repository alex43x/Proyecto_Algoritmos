from database import crear_tablas
from models import Equipos
from models import Torneo
from models import Partido
from datetime import datetime

def main():
    print("🏆 Sistema de Gestión de Torneo de Fútbol 🏆")
    crear_tablas()  # crea las tablas si no existen

    # Crear un torneo
    torneo = Torneo(nombreTorneo="Copa Nacional", fechaDeInicio="2025-10-14", fechaDeFin="2025-12-10",sede="Chile")
    torneo_id = torneo.guardar()
    print(f"Torneo creado: {torneo.nombreTorneo} (ID: {torneo_id})")

    # Crear equipos
    equipo1 = Equipos(identificador="A1", pais="Chile", abreviatura="CHI", confederacion="CONMEBOL", grupo="A",idGrupo="1") #Importante: aca pongan los datos que necesita la clase equipo
    equipo2 = Equipos(identificador="A3", pais="Paraguay", abreviatura="PAR", confederacion="CONMEBOL", grupo="A",idGrupo="1")#Acá igual
    id1 = equipo1.guardar()
    id2 = equipo2.guardar()
    print(f"Equipos creados: {equipo1.pais} (ID {id1}), {equipo2.pais} (ID {id2})")


    print("\n✅ Datos guardados correctamente en la base de datos.")

if __name__ == "__main__":#Para ejecutar el main tienen que estar en la carpeta que contiene este archivo y ejecutar "python main.py"
    main()
