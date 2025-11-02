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
    print(f"Torneo creado: {torneo.nombre} (ID: {torneo_id})")

    # Crear equipos
    equipo1 = Equipos(nombre="Los Leones", ciudad="Asunción", entrenador="Carlos López") #Importante: aca pongan los datos que necesita la clase equipo
    equipo2 = Equipos(nombre="Tiburones FC", ciudad="Encarnación", entrenador="Mario Ruiz")#Acá igual
    id1 = equipo1.guardar()
    id2 = equipo2.guardar()
    print(f"Equipos creados: {equipo1.nombre} (ID {id1}), {equipo2.nombre} (ID {id2})")

    # Registrar un partido
    partido = Partido(#Acá tambien tienen que poner los datos correctos que necesita la clase partido para crear una instancia
        equipo_local_id=id1,
        equipo_visitante_id=id2,
        goles_local=3,
        goles_visitante=1,
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M"),
        
    )
    partido_id = partido.guardar()
    print(f"Partido registrado (ID: {partido_id})")

    print("\n✅ Datos guardados correctamente en la base de datos.")

if __name__ == "__main__":#Para ejecutar el main tienen que estar en la carpeta que contiene este archivo y ejecutar "python main.py"
    main()
