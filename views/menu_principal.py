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

    # configuración base con gradiente simulado
    ventana.configure(bg="#0f3b2f")

    # frame principal con sombra visual
    frame_principal = tk.Frame(ventana, bg="#0f3b2f")
    frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

    # encabezado con efecto moderno
    header_frame = tk.Frame(frame_principal, bg="#0f3b2f")
    header_frame.pack(pady=(20, 40))

    # título principal con mejor jerarquía visual
    tk.Label(
        header_frame,
        text="🏆 GESTIÓN DE TORNEO",
        font=("Segoe UI", 24, "bold"),
        fg="#ffffff",
        bg="#0f3b2f"
    ).pack(pady=(0, 5))

    tk.Label(
        header_frame,
        text="Sistema Integral de Administración Futbolística",
        font=("Segoe UI", 12),
        fg="#68ab98",
        bg="#0f3b2f"
    ).pack()

    # frame que contiene los botones con fondo elevado
    frame_botones = tk.Frame(
        frame_principal, 
        bg="#1a4d3c", 
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightbackground="#2a6d56"
    )
    frame_botones.pack(pady=20, padx=50, fill="both", expand=True)

    # estilo mejorado para los botones
    estilo_boton_principal = {
        "font": ("Segoe UI", 12, "bold"),
        "width": 28,
        "height": 2,
        "relief": "flat",
        "cursor": "hand2",
        "bd": 0,
        "highlightthickness": 1,
        "highlightbackground": "#3a8d76",
        "highlightcolor": "#4aad96"
    }

    # funciones de los botones (sin cambios)
    def abrir_configuracion():
        pantalla_configuracion(ventana, volver_al_menu)
        
    def abrir_registro_resultados():
        if not carga_completa_fechas():
            messagebox.showwarning(
                "Calendario Incompleto", 
                "No se puede acceder al registro de resultados hasta que todas las fechas y horas de los partidos estén cargadas.\n\n"
                "Por favor, completa primero el calendario en la Configuración del Torneo."
            )
            return
        pantalla_resultados(ventana, volver_al_menu)

    def abrir_emision_informes():
        if not carga_completa_fechas():
            messagebox.showwarning(
                "Calendario Incompleto", 
                "No se puede acceder a la emisión de informes hasta que todas las fechas y horas de los partidos estén cargadas.\n\n"
                "Por favor, completa primero el calendario en la Configuración del Torneo."
            )
            return
        pantalla_informes(ventana, volver_al_menu)

    def volver_al_menu(v):
        menu_principal(v)
        
    def salir_aplicacion():
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir de la aplicación?"):
            ventana.destroy()

    # efectos hover para botones
    def on_enter(e):
        e.widget.configure(bg="#5a9987")
        
    def on_leave(e):
        e.widget.configure(bg="#68ab98")

    # lista de botones con colores diferenciados
    botones_config = [
        ("⚙️  Configuración del Torneo", "#68ab98", abrir_configuracion),
        ("📋  Registro de Resultados", "#5a8fab", abrir_registro_resultados),
        ("📊  Emisión de Informes", "#ab8f5a", abrir_emision_informes),
        ("🚪  Salir de la Aplicación", "#ab685a", salir_aplicacion)
    ]

    # crear botones dinámicamente
    for texto, color, comando in botones_config:
        boton = tk.Button(
            frame_botones,
            text=texto,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            command=comando,
            **estilo_boton_principal
        )
        boton.pack(pady=12, padx=40)
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

    # frame de información del sistema
    info_frame = tk.Frame(frame_principal, bg="#0f3b2f")
    info_frame.pack(side="bottom", fill="x", pady=(30, 10))

    # estado del calendario
    estado_calendario = "✅ COMPLETO" if carga_completa_fechas() else "⚠️ INCOMPLETO"
    color_estado = "#4CAF50" if carga_completa_fechas() else "#FF9800"
    
    tk.Label(
        info_frame,
        text=f"Estado del Calendario: ",
        font=("Segoe UI", 9),
        bg="#0f3b2f",
        fg="#cccccc"
    ).pack(side="left", padx=(0, 5))
    
    tk.Label(
        info_frame,
        text=estado_calendario,
        font=("Segoe UI", 9, "bold"),
        bg="#0f3b2f",
        fg=color_estado
    ).pack(side="left")

    # pie de página mejorado
    footer_frame = tk.Frame(frame_principal, bg="#0f3b2f")
    footer_frame.pack(side="bottom", fill="x", pady=10)

    tk.Label(
        footer_frame,
        text="Desarrollado por Sintax FC • © 2025 • Versión 1.0",
        font=("Segoe UI", 9),
        bg="#0f3b2f",
        fg="#68ab98"
    ).pack()

    # línea separadora decorativa
    separador = tk.Frame(
        footer_frame, 
        height=1, 
        bg="#2a6d56",
        relief="sunken"
    )
    separador.pack(fill="x", pady=(0, 5))

    # actualizar ventana
    ventana.update_idletasks()