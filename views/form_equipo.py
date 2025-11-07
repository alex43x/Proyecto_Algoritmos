import tkinter as tk
from tkinter import messagebox
from models.equipos import Equipos
from controllers.equipos import insert_equipo,get_equipos_por_grupo
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

    grupos = get_grupo()  # [(idGrupo, nombreGrupo), ...]

    if len(grupos) == 0:
        messagebox.showerror("Error", "No hay grupos disponibles. Primero agrega un grupo.")
        ventana.destroy()
        return

    # Crear mapa nombre → id
    mapa_grupos = {str(g[1]): g[0] for g in grupos}

    # Variable del OptionMenu (lo que ve el usuario)
    var_grupo = tk.StringVar(value=str(grupos[0][1]))

    # Crear el menú desplegable mostrando solo los nombres
    op_grupo = tk.OptionMenu(frame_inputs, var_grupo, *[str(g[1]) for g in grupos])
    op_grupo.config(width=10, font=("Segoe UI", 12))
    op_grupo.grid(row=4, column=1, sticky="w")

    # Luego, cuando necesites el valor real del grupo:
    # grupo_nombre = var_grupo.get()
    # grupo_id = mapa_grupos[grupo_nombre]


    def guardar_equipo():
        identificador = e_identificador.get()
        pais = e_pais.get()
        abreviatura = e_abreviatura.get()
        confederacion = e_confederacion.get()
        idGrupo = mapa_grupos[var_grupo.get()]
        
        if not identificador or not pais or not abreviatura or not confederacion:
            messagebox.showerror("Error", "Debes completar todos los campos")
            return
        # --- Validación de cantidad de equipos ---
        equipos_en_grupo = get_equipos_por_grupo(idGrupo)
        print(equipos_en_grupo)
        if len(equipos_en_grupo) >= 4:
            messagebox.showerror("Error", f"El grupo {var_grupo.get()} ya tiene 4 equipos.")
            return

        # --- Guardado ---
        equipo = Equipos(identificador, pais, abreviatura, confederacion, idGrupo)
        equipo.guardar()
        messagebox.showinfo("Éxito", f"Equipo '{pais}' registrado correctamente")
        ventana.destroy()
        callback_actualizar()


    tk.Button(
        ventana, text="Guardar Equipo",
        font=("Arial", 12), bg="#FF9800", fg="white",
        command=guardar_equipo
    ).pack(pady=10)
