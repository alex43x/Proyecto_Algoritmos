import tkinter as tk
from tkinter import messagebox
from controllers.torneo import get_torneos
from controllers.grupos import get_grupo
from controllers.equipos import get_equipo
from views.form_grupo import form_grupo
from views.form_equipo import form_equipo
from models.torneo import Torneo
import datetime

def pantalla_configuracion(ventana, volver_menu):
    for widget in ventana.winfo_children():
        widget.destroy()
        
    def volver():
        volver_menu(ventana)
        
    data = get_torneos()
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    anios = [str(i) for i in range(2025,2031)]

    def validar_fecha(dia, mes, anio):
        try:
            datetime.date(int(anio), meses.index(mes)+1, int(dia))
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

        fecha_inicio = f"{anio_i}-{meses.index(mes_i)+1:02d}-{int(dia_i):02d}"
        fecha_fin = f"{anio_f}-{meses.index(mes_f)+1:02d}-{int(dia_f):02d}"
        if fecha_fin <= fecha_inicio:
            messagebox.showerror("Error", "La fecha de cierre no puede ser menor o igual a la de inicio")
            return

        Torneo(nombre, sede, fecha_inicio, fecha_fin).guardar()
        messagebox.showinfo("Éxito", "Torneo registrado correctamente")
        volver_menu(ventana)

    tk.Label(ventana, text="Configuración del Torneo", font=("Segoe UI",16)).pack(pady=10)

    # --- Formulario si no hay torneo ---
    if len(data) == 0:
        frame_inputs = tk.Frame(ventana)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Nombre:",font=("Segoe UI",12)).grid(row=0, column=0, sticky="w",pady=5,padx=(0,3))
        lnombre = tk.Entry(frame_inputs,width=25,font=("Segoe UI",12))
        lnombre.grid(row=0, column=1,sticky="w")

        tk.Label(frame_inputs, text="Sede:",font=("Segoe UI",12)).grid(row=1, column=0,sticky="w", pady=5)
        lsede = tk.Entry(frame_inputs,width=20,font=("Segoe UI",12))
        lsede.grid(row=1, column=1, sticky="w")

        tk.Label(frame_inputs, text="Fecha de Inicio:",font=("Segoe UI",12)).grid(row=2, column=0, sticky="w", pady=5,padx=(0,3))
        e_dia_inicio = tk.Entry(frame_inputs, width=8,font=("Segoe UI",12))
        e_dia_inicio.grid(row=2, column=1, sticky="w")
        var_mes_inicio = tk.StringVar(value=meses[0])
        op_mes_inicio = tk.OptionMenu(frame_inputs, var_mes_inicio, *meses)
        op_mes_inicio.config(width=12,font=("Segoe UI",12))
        op_mes_inicio.grid(row=2, column=1,sticky="e")
        var_anio_inicio = tk.StringVar(value=anios[0])
        op_anio_inicio = tk.OptionMenu(frame_inputs, var_anio_inicio, *anios)
        op_anio_inicio.config(width=5,font=("Segoe UI",12))
        op_anio_inicio.grid(row=2, column=2)

        tk.Label(frame_inputs, text="Fecha de Cierre:",font=("Segoe UI",12)).grid(row=3, column=0,sticky="w", pady=5,padx=(0,3))
        e_dia_fin = tk.Entry(frame_inputs, width=8,font=("Segoe UI",12))
        e_dia_fin.grid(row=3, column=1, sticky="w")
        var_mes_fin = tk.StringVar(value=meses[0])
        op_mes_fin = tk.OptionMenu(frame_inputs, var_mes_fin, *meses)
        op_mes_fin.config(width=12,font=("Segoe UI",12))
        op_mes_fin.grid(row=3, column=1,sticky="e")
        var_anio_fin = tk.StringVar(value=anios[0])
        op_anio_fin = tk.OptionMenu(frame_inputs, var_anio_fin, *anios)
        op_anio_fin.config(width=5,font=("Segoe UI",12))
        op_anio_fin.grid(row=3, column=2)

        tk.Button(
            ventana, text="Guardar datos del torneo",
            font=("Arial", 12), bg="#4CAF50", fg="white",
            command=guardar_torneo
        ).pack(pady=4)

    else:
        torneo = data[0]

        # --- Frame principal ---
        frame_main = tk.Frame(ventana)
        frame_main.pack(fill="x", padx=40, pady=10)

        # --- Frame izquierdo (info torneo) ---
        frame_info = tk.Frame(frame_main)
        frame_info.pack(side="left", anchor="nw")

        tk.Label(frame_info, text=torneo[1], font=("Arial",12,"bold")).pack(anchor="w", pady=2)
        tk.Label(frame_info, text="Sede: " + torneo[2], font=("Arial",10,"bold")).pack(anchor="w", pady=2)
        tk.Label(frame_info, text="Fecha de Inicio: " + torneo[3], font=("Arial",10,"bold")).pack(anchor="w", pady=2)
        tk.Label(frame_info, text="Fecha de Cierre: " + torneo[4], font=("Arial",10,"bold")).pack(anchor="w", pady=2)

        # --- Frame central (grupos y equipos) ---
        frame_centro = tk.Frame(frame_main)
        frame_centro.pack(side="left", padx=20)

        def mostrar_grupos_equipos():
            for widget in frame_centro.winfo_children():
                widget.destroy()

            grupos_actualizados = get_grupo()   # [(idGrupo, nombreGrupo), ...]
            equipos_actualizados = get_equipo() # [(identificador, pais, abreviatura, confederacion, grupo_id), ...]

            # Crear mapping idGrupo -> nombreGrupo
            id_a_nombre = {str(grupo[0]): grupo[1] for grupo in grupos_actualizados}

            # Crear diccionario de grupos por nombre, aunque estén vacíos
            grupos_dict = {nombre: [] for _, nombre in grupos_actualizados}

            # Asignar equipos a sus grupos por id
            for equipo in equipos_actualizados:
                grupo_id = str(equipo[4])
                grupo_nombre = id_a_nombre.get(grupo_id, None)
                if grupo_nombre:
                    grupos_dict[grupo_nombre].append(equipo)
                else:
                    # Equipo con grupo desconocido, lo agregamos con su id como nombre
                    grupos_dict[grupo_id] = [equipo]

            # --- Mostrar grupos en 3 columnas ---
            max_cols = 3
            row = 0
            col = 0
            for gid, equipos_del_grupo in grupos_dict.items():
                frame_grupo = tk.LabelFrame(
                    frame_centro, text=f"Grupo {gid}", padx=10, pady=5, font=("Arial", 11, "bold")
                )
                frame_grupo.grid(row=row, column=col, padx=10, pady=10, sticky="n")

                # Mostrar equipos en filas de 3 si hay
                for i, eq in enumerate(equipos_del_grupo):
                    tk.Label(
                        frame_grupo,
                        text=f"{eq[1]} ({eq[2]})",
                        font=("Arial", 10)
                    ).grid(row=i // 3, column=i % 3, padx=5, pady=3)

                # Si el grupo está vacío, agregamos un label de aviso
                if len(equipos_del_grupo) == 0:
                    tk.Label(frame_grupo, text="(Sin equipos)", font=("Arial", 10, "italic")).pack(padx=5, pady=5)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1


        mostrar_grupos_equipos()

        def actualizar_grupos_equipos():
            mostrar_grupos_equipos()
            if len(get_grupo()) >= 6:
                b_grupos.config(state="disabled")
            else:
                b_grupos.config(state="normal")
            if len(get_equipo()) >= 24:
                b_equipos.config(state="disabled")
            else:
                b_equipos.config(state="normal")

        # --- Frame derecho (botones) ---
        frame_buttons = tk.Frame(frame_main)
        frame_buttons.pack(side="right", anchor="ne")

        tk.Button(
            frame_buttons,
            text="Volver al menú principal",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=volver
        ).pack(anchor="e", pady=4)

        def abrir_form_grupo():
            form_grupo(ventana, actualizar_grupos_equipos)

        def abrir_form_equipo():
            form_equipo(ventana, actualizar_grupos_equipos)

        b_grupos = tk.Button(
            frame_buttons,
            text="Agregar Grupo",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=abrir_form_grupo
        )
        b_grupos.pack(anchor="e", pady=4)
        if len(get_grupo()) >= 6:
            b_grupos.config(state="disabled")

        b_equipos = tk.Button(
            frame_buttons,
            text="Agregar Equipo",
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            command=abrir_form_equipo
        )
        b_equipos.pack(anchor="e", pady=4)
        if len(get_equipo()) >= 24 or len(get_grupo())<6:
            b_equipos.config(state="disabled")
