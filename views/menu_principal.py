import tkinter as tk
from views.menu_torneo import pantalla_configuracion

def menu_principal(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(ventana, text="Gestión de Torneo de Fútbol",
             font=("Arial", 14, "bold")).pack(pady=20)

    # Botón para abrir configuración
    def abrir_configuracion():
        pantalla_configuracion(ventana, volver_al_menu)

    def volver_al_menu(v):
        menu_principal(v)

    tk.Button(ventana, text="Configuración del torneo",
              font=("Arial", 12), bg="#4CAF50", fg="white",
              command=abrir_configuracion).pack(pady=10)

    tk.Button(ventana, text="Salir",
              font=("Arial", 12), bg="#f44336", fg="white",
              command=ventana.destroy).pack(pady=10)
