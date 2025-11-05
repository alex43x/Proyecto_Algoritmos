import tkinter as tk

def menu_principal(ventana, abrir_configuracion):
    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(
        ventana, text="Gestión de Torneo de Fútbol",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        ventana, text="Configuración del torneo",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        command=lambda: abrir_configuracion()
    ).pack(pady=10)

    tk.Button(
        ventana, text="Registro de Resultados",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        state="disabled"
    ).pack(pady=10)

    tk.Button(
        ventana, text="Informes",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        state="disabled"
    ).pack(pady=10)



    tk.Button(
        ventana, text="Salir",
        font=("Arial", 12), bg="#f44336", fg="white",
        command=ventana.destroy
    ).pack(pady=10)
