import tkinter as tk
from tkinter import messagebox
from views.menu_torneo import pantalla_configuracion
from views.menu_resultados import pantalla_resultados
from views.menu_informes import pantalla_informes

from utils import carga_completa_fechas  # Importar la función


def menu_principal(ventana):
    # limpiar ventana
    for widget in ventana.winfo_children():
        widget.destroy()

    # configuración base
    ventana.configure(bg="#f5f5f5")

    # título principal
    tk.Label(
        ventana,
        text="🏆 Gestión Torneo de fútbol",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#f5f5f5"
    ).pack(pady=30)

    # frame que contiene los botones
    frame_botones = tk.Frame(ventana, bg="#f5f5f5")
    frame_botones.pack(pady=10)

    # estilo común para los botones
    estilo_boton = {
        "font": ("Segoe UI", 12, "bold"),
        "width": 25,
        "height": 2,
        "relief": "flat",
        "cursor": "hand2",
        "bd": 2
    }

    # funciones de los botones
    def abrir_configuracion():
        pantalla_configuracion(ventana, volver_al_menu)
        
    def abrir_registro_resultados():
        # Verificar si todas las fechas están cargadas antes de permitir el acceso
        if not carga_completa_fechas():
            messagebox.showwarning(
                "Calendario Incompleto", 
                "No se puede acceder al registro de resultados hasta que todas las fechas y horas de los partidos estén cargadas.\n\n"
                "Por favor, completa primero el calendario en la Configuración del Torneo."
            )
            return
        pantalla_resultados(ventana, volver_al_menu)

    def volver_al_menu(v):
        menu_principal(v)

    def abrir_emision_informes():
        pantalla_informes(ventana, volver_al_menu)
        
    def salir_aplicacion():
        ventana.destroy()

    # botón configuración
    tk.Button(
        frame_botones,
        text="⚙️ Configuración del torneo",
        bg="#68ab98",
        fg="white",
        activebackground="#5a9987",
        activeforeground="white",
        command=abrir_configuracion,
        **estilo_boton
    ).pack(pady=10)

    # botón registro de resultados
    tk.Button(
        frame_botones,
        text="📋 Registro de resultados",
        bg="#68ab98",
        fg="white",
        activebackground="#5a9987",
        activeforeground="white",
        command=abrir_registro_resultados,
        **estilo_boton
    ).pack(pady=10)

    # botón emisión de informes
    tk.Button(
        frame_botones,
        text="📑 Emisión de informes",
        bg="#68ab98",
        fg="white",
        activebackground="#5a9987",
        activeforeground="white",
        command=abrir_emision_informes,
        **estilo_boton
    ).pack(pady=10)

    # botón salir
    tk.Button(
        frame_botones,
        text="❌ Salir",
        bg="#68ab98",
        fg="white",
        activebackground="#5a9987",
        activeforeground="white",
        command=salir_aplicacion,
        **estilo_boton
    ).pack(pady=10)

    # pie de página
    tk.Label(
        ventana,
        text="Desarrollado por Sintax FC © 2025",
        font=("Segoe UI", 9),
        bg="#f5f5f5",
        fg="#777"
    ).pack(side="bottom", pady=10)