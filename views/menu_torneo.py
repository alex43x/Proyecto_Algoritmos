from tkinter import ttk, messagebox
import tkinter as tk
import datetime
from controllers.partido import get_partidos
from controllers.torneo import get_torneos
from controllers.grupos import get_grupo
from controllers.equipos import get_equipo
from views.form_grupo import form_grupo
from views.form_equipo import form_equipo
from views.form_partidos import form_partidos   
from models.torneo import Torneo


def pantalla_configuracion(ventana, volver_menu):
    for widget in ventana.winfo_children():
        widget.destroy()

    def volver():
        volver_menu(ventana)

    data = get_torneos()
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    anios = [str(i) for i in range(2025, 2031)]

    def validar_fecha(dia, mes, anio):
        try:
            datetime.date(int(anio), meses.index(mes) + 1, int(dia))
            return True
        except ValueError:
            return False

    def guardar_torneo():
        dia_i, mes_i, anio_i = e_dia_inicio.get(), var_mes_inicio.get(), var_anio_inicio.get()
        dia_f, mes_f, anio_f = e_dia_fin.get(), var_mes_fin.get(), var_anio_fin.get()
        nombre = lnombre.get()
        sede = lsede.get()

        if not nombre or not sede:
            messagebox.showerror("Error", "Debes completar todos los campos")
            return
        if not validar_fecha(dia_i, mes_i, anio_i):
            messagebox.showerror("Error", "Fecha de inicio inválida")
            return
        if not validar_fecha(dia_f, mes_f, anio_f):
            messagebox.showerror("Error", "Fecha de cierre inválida")
            return

        fecha_inicio = f"{anio_i}-{meses.index(mes_i) + 1:02d}-{int(dia_i):02d}"
        fecha_fin = f"{anio_f}-{meses.index(mes_f) + 1:02d}-{int(dia_f):02d}"
        if fecha_fin <= fecha_inicio:
            messagebox.showerror("Error", "La fecha de cierre no puede ser menor o igual a la de inicio")
            return

        Torneo(nombre, sede, fecha_inicio, fecha_fin).guardar()
        messagebox.showinfo("Éxito", "Torneo registrado correctamente")
        volver_menu(ventana)

    tk.Label(ventana, text="Configuración General", font=("Segoe UI", 24,"bold")).pack(pady=(30,0))

    # Si no hay torneo registrado
    if len(data) == 0:
        frame_inputs = tk.Frame(ventana)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Nombre:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5, padx=(0, 3))
        lnombre = tk.Entry(frame_inputs, width=25, font=("Segoe UI", 12))
        lnombre.grid(row=0, column=1, sticky="w")

        tk.Label(frame_inputs, text="Sede:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=5)
        lsede = tk.Entry(frame_inputs, width=20, font=("Segoe UI", 12))
        lsede.grid(row=1, column=1, sticky="w")

        tk.Label(frame_inputs, text="Fecha de Inicio:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", pady=5)
        e_dia_inicio = tk.Entry(frame_inputs, width=8, font=("Segoe UI", 12))
        e_dia_inicio.grid(row=2, column=1, sticky="w")
        var_mes_inicio = tk.StringVar(value=meses[0])
        tk.OptionMenu(frame_inputs, var_mes_inicio, *meses).grid(row=2, column=1, sticky="e")
        var_anio_inicio = tk.StringVar(value=anios[0])
        tk.OptionMenu(frame_inputs, var_anio_inicio, *anios).grid(row=2, column=2)

        tk.Label(frame_inputs, text="Fecha de Cierre:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="w", pady=5)
        e_dia_fin = tk.Entry(frame_inputs, width=8, font=("Segoe UI", 12))
        e_dia_fin.grid(row=3, column=1, sticky="w")
        var_mes_fin = tk.StringVar(value=meses[0])
        tk.OptionMenu(frame_inputs, var_mes_fin, *meses).grid(row=3, column=1, sticky="e")
        var_anio_fin = tk.StringVar(value=anios[0])
        tk.OptionMenu(frame_inputs, var_anio_fin, *anios).grid(row=3, column=2)

        tk.Button(
            ventana, text="Guardar datos del torneo",
            font=("Segoe UI", 12), bg="#4CAF50", fg="white",
            command=guardar_torneo
        ).pack(pady=4)

    else:
        torneo = data[0]

        frame_main = tk.Frame(ventana)
        frame_main.pack(fill="x", padx=10, pady=10)

        # Información del torneo
        frame_info = tk.Frame(frame_main, bg="#f8f8f8", bd=3, relief="groove", padx=20, pady=20)
        frame_info.pack(side="left", anchor="nw", padx=40, pady=20, fill="y")

        # Título principal
        tk.Label(
            frame_info,
            text="🏆 Información del Torneo",
            font=("Segoe UI", 14, "bold"),
            bg="#f8f8f8",
            fg="#333"
        ).pack(anchor="w", pady=(0, 15))

        # Datos del torneo
        tk.Label(frame_info, text=f"Nombre: {torneo[1]}", font=("Segoe UI", 11), bg="#f8f8f8", fg="#000").pack(anchor="w", pady=2)
        tk.Label(frame_info, text=f"Sede: {torneo[2]}", font=("Segoe UI", 11), bg="#f8f8f8", fg="#000").pack(anchor="w", pady=2)
        tk.Label(frame_info, text=f"Fecha de Inicio: {torneo[3]}", font=("Segoe UI", 10), bg="#f8f8f8", fg="#333").pack(anchor="w", pady=2)
        tk.Label(frame_info, text=f"Fecha de Cierre: {torneo[4]}", font=("Segoe UI", 10), bg="#f8f8f8", fg="#333").pack(anchor="w", pady=2)

        # Línea divisoria visual
        tk.Frame(frame_info, height=2, bg="#68ab98").pack(fill="x", pady=15)

        # --- Funciones internas ---
        def actualizar_grupos_equipos():
            mostrar_grupos_equipos()
            if len(get_grupo()) >= 6:
                b_grupos.config(state="disabled")
            else:
                b_grupos.config(state="normal")

            if len(get_equipo()) >= 24 or len(get_grupo()) < 6:
                b_equipos.config(state="disabled")
            else:
                b_equipos.config(state="normal")

        def actualizar_estados_botones():
            # Cambia color o texto según estado
            if len(get_grupo()) >= 6:
                b_grupos.config(bg="#cccccc", fg="#666", text="Agregar Grupo (Terminado)")
            else:
                b_grupos.config(bg="#68ab98", fg="white", text="Agregar Grupo")

            if len(get_equipo()) >= 24:
                b_equipos.config(bg="#cccccc", fg="#666", text="Agregar Equipo (Terminado)")
            elif len(get_grupo()) < 6:
                b_equipos.config(bg="#cccccc", fg="#666", text="Agregar Equipo (Faltan grupos)")
            else:
                b_equipos.config(bg="#68ab98", fg="white", text="Agregar Equipo")

        def abrir_form_grupo():
            if len(get_grupo()) >= 6:
                messagebox.showinfo("Límite alcanzado", "Ya has registrado los 6 grupos permitidos.")
                return
            form_grupo(ventana, actualizar_grupos_equipos)

        def abrir_form_equipo():
            if len(get_grupo()) < 6:
                messagebox.showwarning("Atención", "Debes registrar los 6 grupos antes de agregar equipos.")
                return
            if len(get_equipo()) >= 24:
                messagebox.showinfo("Límite alcanzado", "Ya has registrado los 24 equipos permitidos.")
                return
            form_equipo(ventana, actualizar_grupos_equipos)

        def abrir_form_partidos():
            if len(get_equipo()) < 24:
                messagebox.showwarning("Atención", "Debes cargar los 24 equipos antes de registrar los partidos.")
                return
            form_partidos(ventana)

        def volver_menu_principal():
            volver()

        # --- Estilo de botones ---
        boton_estilo = {
            "font": ("Segoe UI", 12),
            "bg": "#68ab98",
            "fg": "white",
            "activebackground": "#5a9686",
            "activeforeground": "white",
            "relief": "flat",
            "width": 25,
            "cursor": "hand2",
            "bd": 0,
            "pady": 6
        }

        # --- Botones ---

        b_grupos = tk.Button(
            frame_info,
            text="Agregar Grupo",
            command=abrir_form_grupo,
            **boton_estilo
        )
        b_grupos.pack(anchor="center", pady=8)

        b_equipos = tk.Button(
            frame_info,
            text="Agregar Equipo",
            command=abrir_form_equipo,
            **boton_estilo
        )
        b_equipos.pack(anchor="center", pady=8)

        tk.Button(
            frame_info,
            text="Registrar Fechas de Partidos",
            command=abrir_form_partidos,
            **boton_estilo
        ).pack(anchor="center", pady=8)

        tk.Button(
            frame_info,
            text="Volver al Menú Principal",
            command=volver_menu_principal,
            **boton_estilo
        ).pack(anchor="center", pady=8)
        # Inicializa los estados visuales
        actualizar_estados_botones()

        # Frame Central: Equipos-Grupos
        frame_centro = tk.Frame(frame_main)
        frame_centro.pack(side="left", fill="both", expand=True, padx=(10,0))

        # Subframe para el título
        frame_titulo = tk.Frame(frame_centro)
        frame_titulo.pack(anchor="w")

        tk.Label(
            frame_titulo,
            text="Grupos y Equipos",
            font=("Segoe UI", 16, "bold"),
            fg="#333"
        ).pack(pady=10)

        # Subframe que contendrá los grupos dinámicos
        frame_contenido = tk.Frame(frame_centro)
        frame_contenido.pack(fill="both", expand=True)

        def mostrar_grupos_equipos():
            for widget in frame_contenido.winfo_children():
                widget.destroy()

            grupos_actualizados = get_grupo()
            equipos_actualizados = get_equipo()

            id_a_nombre = {str(g[0]): g[1] for g in grupos_actualizados}
            grupos_dict = {nombre: [] for _, nombre in grupos_actualizados}

            for eq in equipos_actualizados:
                grupo_id = str(eq[4])
                grupo_nombre = id_a_nombre.get(grupo_id)
                if grupo_nombre:
                    grupos_dict[grupo_nombre].append(eq)

            row, col = 0, 0
            for gid, equipos_del_grupo in grupos_dict.items():
                frame_grupo = tk.LabelFrame(
                    frame_contenido,
                    text=f"Grupo {gid}",
                    padx=10,
                    pady=5,
                    font=("Segoe UI", 11, "bold"),
                    bg="#f2f2f2",
                    fg="#333"
                )
                frame_grupo.grid(row=row, column=col, padx=10, pady=10, sticky="n")

                if equipos_del_grupo:
                    # Encabezado tipo tabla
                    encabezados = ["ID", "Abreviatura", "Nombre", "Confederación"]
                    for j, encabezado in enumerate(encabezados):
                        tk.Label(
                            frame_grupo,
                            text=encabezado,
                            font=("Segoe UI", 10, "bold"),
                            bg="#68ab98",
                            fg="#222",
                            relief="ridge",
                            width=14,
                            padx=3,
                            pady=3
                        ).grid(row=0, column=j, sticky="nsew", padx=1, pady=1)

                    # Filas con datos
                    for i, eq in enumerate(equipos_del_grupo, start=1):
                        identificador, nombre, abrev, conf = eq[0], eq[1], eq[2], eq[3]

                        celdas = [identificador, abrev, nombre, conf]
                        for j, valor in enumerate(celdas):
                            tk.Label(
                                frame_grupo,
                                text=valor,
                                font=("Segoe UI", 10),
                                bg="#ffffff",
                                fg="#000",
                                relief="ridge",
                                width=[10,10,20,16][j],
                                anchor=["center","center","w","center"][j]
                            ).grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                else:
                    tk.Label(
                        frame_grupo,
                        text="(Sin equipos en este grupo)",
                        font=("Segoe UI", 10, "italic"),
                        bg="#f2f2f2",
                        fg="#666"
                    ).pack(pady=10)

                col += 1
                if col >= 2:
                    col = 0
                    row += 1

        mostrar_grupos_equipos()


        

