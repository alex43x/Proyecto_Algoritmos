import tkinter as tk
from tkinter import ttk, messagebox
import re
import datetime
from controllers.partido import get_partidos, update_partido_fecha


def form_partidos(ventana_padre):
    """
    Abre una ventana para registrar o editar fechas y horas de los partidos.
    """

    ventana_fechas = tk.Toplevel(ventana_padre)
    ventana_fechas.title("Registrar fechas de los partidos")
    ventana_fechas.state("zoomed")
    ventana_fechas.configure(bg="#f8f8f8")

    # Centrar la ventana
    ventana_fechas.update_idletasks()
    w = 900
    h = 650
    x = (ventana_fechas.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana_fechas.winfo_screenheight() // 2) - (h // 2)
    ventana_fechas.geometry(f"{w}x{h}+{x}+{y}")

    # === TÍTULO ===
    tk.Label(
        ventana_fechas,
        text="⚽ Asignar fecha y hora a los partidos",
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
    jornadas = sorted({p[3] for p in partidos_todos})

    # Diccionario de nombres según el número de jornada
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

    # Mostrar en el combobox el texto descriptivo
    valores_combo = [f"{j} - {descripciones.get(j, 'Jornada')}" for j in jornadas]
    combo_jornada = ttk.Combobox(frame_filtro, values=valores_combo, state="readonly", font=("Segoe UI", 11), width=35)
    combo_jornada.pack(side="left")

    if jornadas:
        combo_jornada.set(valores_combo[0])

    # ================= TABLA =================
    frame_tabla = tk.Frame(ventana_fechas, bg="white", bd=1, relief="solid")
    frame_tabla.pack(fill="both", expand=True, padx=30, pady=10)

    columnas = ("idPartido", "equipo1", "equipo2", "jornada", "fecha", "hora")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
    tabla.pack(fill="both", expand=True)

    # --- Encabezados ---
    encabezados = {
        "idPartido": "ID",
        "equipo1": "Equipo 1",
        "equipo2": "Equipo 2",
        "jornada": "Jornada",
        "fecha": "Fecha (YYYY-MM-DD)",
        "hora": "Hora (HH:MM)"
    }

    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, anchor="center", width=130)

    # Estilo más moderno para la tabla
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#1a493c")
    estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    estilo.map("Treeview", background=[("selected", "#c5e2da")])

    # ================= CARGAR DATOS =================
    def cargar_partidos_por_jornada(*_):
        tabla.delete(*tabla.get_children())
        seleccion = combo_jornada.get().split(" - ")[0]  # Obtener solo el número
        partidos = [p for p in partidos_todos if str(p[3]) == str(seleccion)]
        for p in partidos:
            tabla.insert("", "end", values=p)

    combo_jornada.bind("<<ComboboxSelected>>", cargar_partidos_por_jornada)
    if jornadas:
        cargar_partidos_por_jornada()

    # ================= EDICIÓN EN LA TABLA =================
    def editar_celda(event):
        item = tabla.identify_row(event.y)
        col = tabla.identify_column(event.x)
        if not item or col not in ("#5", "#6"):  # Solo fecha (#5) y hora (#6)
            return

        col_index = int(col[1:]) - 1
        old_value = tabla.item(item, "values")[col_index]
        entry = tk.Entry(frame_tabla, font=("Segoe UI", 11))
        entry.insert(0, old_value)
        entry.focus()

        bbox = tabla.bbox(item, col)
        if not bbox:
            return
        entry.place(x=bbox[0] + 2, y=bbox[1] + 2, width=bbox[2] - 4, height=bbox[3] - 4)

        def guardar_editado(evento):
            nuevo_valor = entry.get().strip()
            valores = list(tabla.item(item, "values"))
            valores[col_index] = nuevo_valor
            tabla.item(item, values=valores)
            entry.destroy()

        def destruir_entry(evento):
            entry.destroy()

        entry.bind("<Return>", guardar_editado)
        entry.bind("<FocusOut>", destruir_entry)

    tabla.bind("<Double-1>", editar_celda)

    # ================= VALIDACIONES =================
    def validar_fecha(fecha):
        if not re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", fecha):
            return False
        try:
            anio, mes, dia = map(int, fecha.split("-"))
            datetime.date(anio, mes, dia)
            return True
        except ValueError:
            return False

    def validar_hora(hora):
        if not re.match(r"^\d{1,2}:\d{2}$", hora):
            return False
        h, m = map(int, hora.split(":"))
        return 0 <= h < 24 and 0 <= m < 60

    # ================= GUARDAR CAMBIOS =================
    def guardar_fechas():
        filas = tabla.get_children()
        cambios = 0

        for f in filas:
            valores = tabla.item(f, "values")
            idp, _, _, _, fecha, hora = valores

            if not fecha.strip() and not hora.strip():
                continue

            if fecha.strip() and not validar_fecha(fecha):
                messagebox.showwarning("Formato inválido", f"Fecha incorrecta en partido {idp}. Usa YYYY-MM-DD.")
                return
            if hora.strip() and not validar_hora(hora):
                messagebox.showwarning("Formato inválido", f"Hora incorrecta en partido {idp}. Usa HH:MM.")
                return

            update_partido_fecha(idp, fecha.strip(), hora.strip())
            cambios += 1

        if cambios > 0:
            messagebox.showinfo("Éxito", f"Fechas de {cambios} partido(s) guardadas correctamente ✅")
            ventana_fechas.destroy()
        else:
            messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

    # ================= BOTONES =================
    frame_botones = tk.Frame(ventana_fechas, bg="#f8f8f8")
    frame_botones.pack(pady=15)

    tk.Button(
        frame_botones,
        text="Guardar Fechas",
        font=("Segoe UI", 12, "bold"),
        bg="#68ab98",
        fg="white",
        command=guardar_fechas,
        width=18,
        relief="flat",
        padx=5,
        pady=5
    ).grid(row=0, column=0, padx=15)

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
