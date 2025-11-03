import tkinter as tk
from tkinter import messagebox
from database import crear_tablas
from models.equipos import Equipos
from models.torneo import Torneo
from models.partido import Partido

def crear_datos():
    crear_tablas()

    torneo = Torneo(
        nombreTorneo="Copa Nacional",
        fechaDeInicio="2025-10-14",
        fechaDeFin="2025-12-10",
        sede="Chile"
    )
    torneo_id = torneo.guardar()

    equipo1 = Equipos(
        identificador="A1",
        pais="Chile",
        abreviatura="CHI",
        confederacion="CONMEBOL",
        grupo="A",
        idGrupo="1"
    )
    equipo2 = Equipos(
        identificador="A3",
        pais="Paraguay",
        abreviatura="PAR",
        confederacion="CONMEBOL",
        grupo="A",
        idGrupo="1"
    )

    id1 = equipo1.guardar()
    id2 = equipo2.guardar()

    partido = Partido(
        anio=2025, mes=11, dia=25, minuto=30, horaDeInicio=13,
        identificadorEquipoUno=equipo1.identificador,
        identificadorEquipoDos=equipo2.identificador,
        golesEquipoUno=0, golesEquipoDos=0,
        tarjetasAmarillasEquipoUno=0, tarjetasAmarillasEquipoDos=0,
        tarjetasRojasEquipoUno=0, tarjetasRojasEquipoDos=0,
        idPartido=3, puntosEquipoUno=0, puntosEquipoDos=0,
        jornada=1
    )

    partido.simularPartido(15)

    # Mostrar datos por consola
    partido.mostrarPartido()

    # Mostrar ventana de confirmación
    messagebox.showinfo("Éxito", f"Torneo '{torneo.nombreTorneo}' y equipos creados correctamente.\nPartido simulado.")

def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Torneo de Fútbol")
    ventana.geometry("400x250")

    titulo = tk.Label(ventana, text="Gestión de Torneo de Fútbol", font=("Arial", 14, "bold"))
    titulo.pack(pady=20)

    boton_crear = tk.Button(
        ventana,
        text="Crear Torneo y Simular Partido",
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        command=crear_datos
    )
    boton_crear.pack(pady=20)

    boton_salir = tk.Button(
        ventana,
        text="Salir",
        font=("Arial", 12),
        bg="#f44336",
        fg="white",
        command=ventana.destroy
    )
    boton_salir.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    main()
