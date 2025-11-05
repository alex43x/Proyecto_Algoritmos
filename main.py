import tkinter as tk
from tkinter import messagebox
from controllers.pool import crear_tablas
from models.equipos import Equipos
from models.torneo import Torneo
from models.partido import Partido

def crear_datos():
    crear_tablas()  # ahora conecta correctamente usando pool.py

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
        idGrupo="1"
    )
    equipo2 = Equipos(
        identificador="A3",
        pais="Paraguay",
        abreviatura="PAR",
        confederacion="CONMEBOL",
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
    partido.mostrarPartido()

    messagebox.showinfo("Éxito", f"Torneo '{torneo.nombreTorneo}' creado.\nPartido simulado correctamente.")

# ---- Pantalla de configuración ----
def pantalla_configuracion(ventana):
    # Limpia todo el contenido actual
    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(ventana, text="Configuración del Torneo", font=("Arial", 14, "bold")).pack(pady=20)
    
    tk.Button(
        ventana, text="Volver al menú principal",
        font=("Arial", 12), bg="#2196F3", fg="white",
        command=lambda: menu_principal(ventana)
    ).pack(pady=10)

# ---- Menú principal ----
def menu_principal(ventana):
    # Limpia los widgets anteriores (por si se regresa)
    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(ventana, text="Gestión de Torneo de Fútbol", font=("Arial", 14, "bold")).pack(pady=20)

    opciones = [
        ("Configuración del torneo", lambda: pantalla_configuracion(ventana)),
        ("Registro de Resultados", None),
        ("Informes", None),
        ("Crear Torneo y Simular Partido", crear_datos),
    ]

    for texto, comando in opciones:
        tk.Button(
            ventana, text=texto, font=("Arial", 12),
            bg="#4CAF50", fg="white", command=comando
        ).pack(pady=10)

    tk.Button(
        ventana, text="Salir", font=("Arial", 12),
        bg="#f44336", fg="white", command=ventana.destroy
    ).pack(pady=10)

# ---- MAIN ----
def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Torneo de Fútbol")
    ventana.geometry("800x450")
    menu_principal(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()