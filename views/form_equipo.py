import tkinter as tk
from tkinter import messagebox
from models.equipos import Equipos
from controllers.equipos import insert_equipo
from controllers.grupos import get_grupo

def form_equipo(ventana_principal, callback_actualizar):
    # Crear ventana secundaria
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Agregar Equipo")
    ventana.geometry("400x350")
    ventana.grab_set()  # Bloquea interacción con la ventana principal

    tk.Label(ventana, text="Registrar Equipo", font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame_inputs = tk.Frame(ventana)
    frame_inputs.pack(pady=10)

    # --- Identificador ---
    tk.Label(frame_inputs, text="Identificador:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5, padx=(0,3))
    e_identificador = tk.Entry(frame_inputs, width=15, font=("Segoe UI", 12))
    e_identificador.grid(row=0, column=1, sticky="w")

    # --- País ---
    tk.Label(frame_inputs, text="País:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=5, padx=(0,3))
    e_pais = tk.Entry(frame_inputs, width=25, font=("Segoe UI", 12))
    e_pais.grid(row=1, column=1, sticky="w")

    # --- Abreviatura ---
    tk.Label(frame_inputs, text="Abreviatura:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", pady=5)
    e_abreviatura = tk.Entry(frame_inputs, width=10, font=("Segoe UI", 12))
    e_abreviatura.grid(row=2, column=1, sticky="w")

    # --- Confederación ---
    tk.Label(frame_inputs, text="Confederación:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="w", pady=5)
    e_confederacion = tk.Entry(frame_inputs, width=20, font=("Segoe UI", 12))
    e_confederacion.grid(row=3, column=1, sticky="w")

    # --- Grupo ---
    tk.Label(frame_inputs, text="Grupo:", font=("Segoe UI", 12)).grid(row=4, column=0, sticky="w", pady=5)
    grupos = get_grupo()
    if len(grupos) == 0:
        messagebox.showerror("Error", "No hay grupos disponibles. Primero agrega un grupo.")
        ventana.destroy()
        return
    var_grupo = tk.StringVar(value=str(grupos[0][0]))
    op_grupo = tk.OptionMenu(frame_inputs, var_grupo, *[str(g[0]) for g in grupos])
    op_grupo.config(width=10, font=("Segoe UI", 12))
    op_grupo.grid(row=4, column=1, sticky="w")

    def guardar_equipo():
        identificador = e_identificador.get()
        pais = e_pais.get()
        abreviatura = e_abreviatura.get()
        confederacion = e_confederacion.get()
        idGrupo = (var_grupo.get())

        if not identificador or not pais or not abreviatura or not confederacion:
            messagebox.showerror("Error", "Debes completar todos los campos")
            return

        equipo = Equipos(identificador, pais, abreviatura, confederacion, idGrupo)
        equipo.guardar()
        messagebox.showinfo("Éxito", f"Equipo '{pais}' registrado correctamente")
        ventana.destroy()
        callback_actualizar()  # Actualiza la lista de equipos en la ventana principal

    tk.Button(
        ventana, text="Guardar Equipo",
        font=("Arial", 12), bg="#FF9800", fg="white",
        command=guardar_equipo
    ).pack(pady=10)
