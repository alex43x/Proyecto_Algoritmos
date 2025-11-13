import tkinter as tk
from tkinter import ttk, messagebox
import re
import datetime
from controllers.partido import get_partidos, update_partido_fecha
from utils import carga_completa_fechas  

def form_partidos(ventana_padre, callback_actualizar=None):
    """
    Abre una ventana para registrar o editar fechas, horas y estadios de los partidos.
    """
    ventana_fechas = tk.Toplevel(ventana_padre)
    ventana_fechas.title("Registrar fechas de los partidos")
    ventana_fechas.state("zoomed")
    ventana_fechas.configure(bg="#f8f8f8")

    ventana_fechas.update_idletasks()
    w = 900
    h = 700
    x = (ventana_fechas.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana_fechas.winfo_screenheight() // 2) - (h // 2)
    ventana_fechas.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(
        ventana_fechas,
        text="⚽ Asignar fecha, hora y estadio a los partidos",
        font=("Segoe UI", 18, "bold"),
        bg="#f8f8f8",
        fg="#333",
    ).pack(pady=15)

    # ================= FILTRO DE JORNADA =================
    frame_filtro = tk.Frame(ventana_fechas, bg="#f8f8f8")
    frame_filtro.pack(pady=(5, 15))

    tk.Label(
        frame_filtro,
        text="Seleccionar jornada:",
        font=("Segoe UI", 13, "bold"),
        bg="#f8f8f8",
    ).pack(side="left", padx=(0, 10))

    partidos_todos = get_partidos()
    jornadas = sorted({int(p[13]) for p in partidos_todos if str(p[13]).isdigit()})

    descripciones = {
        1: "Fase de Grupos - Jornada 1",
        2: "Fase de Grupos - Jornada 2",
        3: "Fase de Grupos - Jornada 3",
        4: "Octavos de Final",
        5: "Cuartos de Final",
        6: "Semifinal",
        7: "Tercer Puesto",
        8: "Final"
    }

    valores_combo = [f"{j} - {descripciones.get(j, 'Jornada')}" for j in jornadas]
    combo_jornada = ttk.Combobox(frame_filtro, values=valores_combo, state="readonly", font=("Segoe UI", 11), width=35)
    combo_jornada.pack(side="left")

    if jornadas:
        combo_jornada.set(valores_combo[0])

    # ================= TABLA =================
    frame_tabla = tk.Frame(ventana_fechas, bg="white", bd=1, relief="solid")
    frame_tabla.pack(fill="both", expand=True, padx=30, pady=10)

    columnas = ("idPartido", "equipo1", "equipo2", "jornada", "fecha", "hora", "estadio")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
    tabla.pack(fill="both", expand=True)

    encabezados = {
        "idPartido": "ID",
        "equipo1": "Equipo 1",
        "equipo2": "Equipo 2",
        "jornada": "Jornada",
        "fecha": "Fecha (YYYY-MM-DD)",
        "hora": "Hora (HH:MM)",
        "estadio": "Estadio"
    }

    # Configuración de columnas 
    tabla.column("idPartido", anchor="center", width=60)
    tabla.column("equipo1", anchor="center", width=130)
    tabla.column("equipo2", anchor="center", width=130)
    tabla.column("jornada", anchor="center", width=100)
    tabla.column("fecha", anchor="center", width=130)
    tabla.column("hora", anchor="center", width=100)
    tabla.column("estadio", anchor="center", width=300)

    for col in columnas:
        tabla.heading(col, text=encabezados[col])

    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    estilo.map("Treeview", background=[("selected", "#c5e2da")])

    # ================= CARGAR DATOS =================
    def cargar_partidos_por_jornada(*_):
        tabla.delete(*tabla.get_children())
        seleccion = combo_jornada.get().split(" - ")[0]
        partidos = [p for p in partidos_todos if str(p[13]) == str(seleccion)]

        for p in partidos:
            valores = (
                p[0],  # idPartido
                p[3],  # equipo1_nombre
                p[4],  # equipo2_nombre
                p[13], # jornada
                p[1] if p[1] else "",  # fecha
                p[2] if p[2] else "",  # hora
                p[14] if len(p) > 14 and p[14] else ""  # estadio
            )
            tabla.insert("", "end", values=valores)

    combo_jornada.bind("<<ComboboxSelected>>", cargar_partidos_por_jornada)
    if jornadas:
        cargar_partidos_por_jornada()

    # ================= EDICIÓN =================
    def editar_celda(event):
        if carga_completa_fechas():
            messagebox.showinfo("Calendario Completo", "El calendario ya está completamente cargado.")
            return

        item = tabla.identify_row(event.y)
        col = tabla.identify_column(event.x)
        if not item or col not in ("#5", "#6", "#7"):
            return

        col_index = int(col[1:]) - 1
        old_value = tabla.item(item, "values")[col_index]

        if col == "#7":  # Edición del estadio
            top = tk.Toplevel(ventana_fechas)
            top.title("Seleccionar estadio")
            tk.Label(top, text="Selecciona el estadio:", font=("Segoe UI", 11, "bold")).pack(pady=5)

            combo_estadio = ttk.Combobox(top, state="readonly", font=("Segoe UI", 11), width=65)
            combo_estadio["values"] = [
                "Nacional Julio Martínez Prádanos - Santiago de Chile",
                "Monumental David Arellano - Santiago de Chile",
                "Claro Arena - San Carlos de Apoquindo, Las Condes",
                "Santa Laura de la Universidad SEK - Santiago de Chile"
            ]
            combo_estadio.set(old_value if old_value else combo_estadio["values"][0])
            combo_estadio.pack(pady=5)

            def confirmar_estadio():
                nuevo_estadio = combo_estadio.get()
                valores = list(tabla.item(item, "values"))
                valores[col_index] = nuevo_estadio
                tabla.item(item, values=valores)
                top.destroy()

            ttk.Button(top, text="Confirmar", command=confirmar_estadio).pack(pady=5)
            return

        # Edición de fecha/hora
        entry = tk.Entry(frame_tabla, font=("Segoe UI", 11))
        entry.insert(0, old_value)
        entry.focus()

        bbox = tabla.bbox(item, col)
        if not bbox:
            return
        entry.place(x=bbox[0] + 2, y=bbox[1] + 2, width=bbox[2] - 4, height=bbox[3] - 4)

        def guardar_editado(evento=None):
            nuevo_valor = entry.get().strip()
            valores = list(tabla.item(item, "values"))
            valores[col_index] = nuevo_valor
            tabla.item(item, values=valores)
            entry.destroy()

        def destruir_entry(evento=None):
            # Guardar el valor antes de destruir el entry
            guardar_editado()

        entry.bind("<Return>", guardar_editado)
        entry.bind("<FocusOut>", destruir_entry)

    tabla.bind("<Double-1>", editar_celda)

    # ================= VALIDACIONES =================
    def validar_fecha(fecha):
        if not fecha.strip():
            return True
        if not re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", fecha):
            return False
        try:
            anio, mes, dia = map(int, fecha.split("-"))
            datetime.date(anio, mes, dia)
            return True
        except ValueError:
            return False

    def validar_hora(hora):
        if not hora.strip():
            return True
        if not re.match(r"^\d{1,2}:\d{2}$", hora):
            return False
        h, m = map(int, hora.split(":"))
        return 0 <= h < 24 and 0 <= m < 60

    # ================= GUARDAR CAMBIOS =================
    def guardar_fechas():
        if carga_completa_fechas():
            messagebox.showinfo("Calendario Completo", "El calendario de partidos ya está completamente cargado.")
            return

        filas = tabla.get_children()
        cambios = 0
        errores = []

        for f in filas:
            valores = tabla.item(f, "values")
            idp, equipo1, equipo2, jornada, fecha, hora, estadio = valores

            if fecha.strip() and not validar_fecha(fecha):
                errores.append(f"Partido {equipo1} vs {equipo2}: Fecha inválida '{fecha}'. Usa YYYY-MM-DD.")
                continue

            if hora.strip() and not validar_hora(hora):
                errores.append(f"Partido {equipo1} vs {equipo2}: Hora inválida '{hora}'. Usa HH:MM.")
                continue

            # Solo actualiza si hay al menos uno de los campos cargados
            if fecha.strip() or hora.strip() or estadio.strip():
                try:
                    fecha_db = fecha.strip() if fecha.strip() else None
                    hora_db = hora.strip() if hora.strip() else None
                    estadio_db = estadio.strip() if estadio.strip() else None

                    print(f"Actualizando partido {idp}: fecha='{fecha_db}', hora='{hora_db}', estadio='{estadio_db}'")

                    update_partido_fecha(idp, fecha_db, hora_db, estadio_db)
                    cambios += 1

                except Exception as e:
                    errores.append(f"Error al guardar partido {idp}: {str(e)}")

        if errores:
            messagebox.showerror("Errores al guardar", "\n".join(errores[:5]))
        elif cambios > 0:
            messagebox.showinfo("Cambios Guardados", f"Fechas, horas y estadios de {cambios} partido(s) guardadas correctamente ✅")
            if callback_actualizar:
                callback_actualizar()
            ventana_fechas.destroy()
        else:
            messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

    # ================= BOTONES =================
    frame_botones = tk.Frame(ventana_fechas, bg="#f8f8f8")
    frame_botones.pack(pady=15)

    estado_boton = "normal"
    if carga_completa_fechas():
        estado_boton = "disabled"

    btn_guardar = tk.Button(
        frame_botones,
        text="Guardar Fechas y Estadios",
        font=("Segoe UI", 12, "bold"),
        bg="#68ab98",
        fg="white",
        command=guardar_fechas,
        width=20,
        relief="flat",
        padx=5,
        pady=5,
        state=estado_boton
    )
    btn_guardar.grid(row=0, column=0, padx=15)

    tk.Button(
        frame_botones,
        text="Cerrar",
        font=("Segoe UI", 12, "bold"),
        bg="#d9534f",
        fg="white",
        command=ventana_fechas.destroy,
        width=18,
        relief="flat",
        padx=5,
        pady=5
    ).grid(row=0, column=1, padx=15)