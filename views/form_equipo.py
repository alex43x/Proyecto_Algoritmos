import tkinter as tk
from tkinter import ttk, messagebox
from models.equipos import Equipos
from controllers.equipos import insert_equipo, get_equipos_por_grupo
from controllers.grupos import get_grupo


def form_equipo(ventana_principal, callback_actualizar):
    # --- Crear ventana secundaria ---
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Agregar Equipo")
    ventana.configure(bg="#f8f8f8")
    ventana.resizable(False, False)

    # --- Centrar ventana ---
    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    centrar_ventana(ventana, 420, 420)
    ventana.grab_set()

    # --- Frame principal tipo tarjeta ---
    frame_main = tk.Frame(ventana, bg="white", bd=2, relief="groove", padx=20, pady=20)
    frame_main.pack(padx=20, pady=20, fill="both", expand=True)

    # --- Título ---
    tk.Label(
        frame_main,
        text="Registrar Equipo",
        font=("Segoe UI", 14, "bold"),
        fg="#333",
        bg="white"
    ).pack(pady=(0, 15))

    frame_inputs = tk.Frame(frame_main, bg="white")
    frame_inputs.pack(pady=5)

    # --- Identificador ---
    tk.Label(frame_inputs, text="Identificador:", font=("Segoe UI", 11, "bold"), bg="white").grid(row=0, column=0, sticky="e", pady=6, padx=5)
    e_identificador = tk.Entry(frame_inputs, width=15, font=("Segoe UI", 11), relief="solid", bd=1)
    e_identificador.grid(row=0, column=1, sticky="w", pady=6, padx=5)

    # --- País ---
    tk.Label(frame_inputs, text="País:", font=("Segoe UI", 11, "bold"), bg="white").grid(row=1, column=0, sticky="e", pady=6, padx=5)
    e_pais = tk.Entry(frame_inputs, width=25, font=("Segoe UI", 11), relief="solid", bd=1)
    e_pais.grid(row=1, column=1, sticky="w", pady=6, padx=5)

    # --- Abreviatura ---
    tk.Label(frame_inputs, text="Abreviatura:", font=("Segoe UI", 11, "bold"), bg="white").grid(row=2, column=0, sticky="e", pady=6, padx=5)
    e_abreviatura = tk.Entry(frame_inputs, width=10, font=("Segoe UI", 11), relief="solid", bd=1)
    e_abreviatura.grid(row=2, column=1, sticky="w", pady=6, padx=5)

    # --- Confederación ---
    tk.Label(frame_inputs, text="Confederación:", font=("Segoe UI", 11, "bold"), bg="white").grid(row=3, column=0, sticky="e", pady=6, padx=5)
    e_confederacion = tk.Entry(frame_inputs, width=20, font=("Segoe UI", 11), relief="solid", bd=1)
    e_confederacion.grid(row=3, column=1, sticky="w", pady=6, padx=5)

    # --- Grupo ---
    tk.Label(frame_inputs, text="Grupo:", font=("Segoe UI", 11, "bold"), bg="white").grid(row=4, column=0, sticky="e", pady=6, padx=5)

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

    # --- Función de guardado ---
    def guardar_equipo():
        identificador = e_identificador.get().strip()
        pais = e_pais.get().strip()
        abreviatura = e_abreviatura.get().strip()
        confederacion = e_confederacion.get().strip()
        idGrupo = mapa_grupos[var_grupo.get()]

        if not identificador or not pais or not abreviatura or not confederacion:
            messagebox.showerror("Error", "Debes completar todos los campos.")
            return

        equipos_en_grupo = get_equipos_por_grupo(idGrupo)
        if len(equipos_en_grupo) >= 4:
            messagebox.showerror("Error", f"El grupo {var_grupo.get()} ya tiene 4 equipos.")
            return

        equipo = Equipos(identificador, pais, abreviatura, confederacion, idGrupo)
        equipo.guardar()
        messagebox.showinfo("✅ Éxito", f"Equipo '{pais}' registrado correctamente.")
        ventana.destroy()
        callback_actualizar()

    # --- Frame de botones ---
    frame_botones = tk.Frame(frame_main, bg="white")
    frame_botones.pack(pady=(15, 0))

    # --- Botón Guardar ---
    tk.Button(
        frame_botones,
        text="Guardar",
        font=("Segoe UI", 11, "bold"),
        bg="#68ab98",
        fg="white",
        width=12,
        command=guardar_equipo
    ).grid(row=0, column=0, padx=10)

    # --- Botón Cancelar ---
    tk.Button(
        frame_botones,
        text="Cancelar",
        font=("Segoe UI", 11, "bold"),
        bg="#e57373",
        fg="white",
        width=12,
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

    # --- Mantener modal ---
    ventana.transient(ventana_principal)
    ventana.grab_set()
    ventana_principal.wait_window(ventana)
