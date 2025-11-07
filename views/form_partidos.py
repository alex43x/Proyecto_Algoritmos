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
    ventana_fechas.geometry("850x600")
    ventana_fechas.configure(bg="#f8f8f8")

    tk.Label(
        ventana_fechas,
        text="Asignar fecha y hora a los partidos",
        font=("Segoe UI", 16, "bold"),
        bg="#f8f8f8",
    ).pack(pady=10)

    # ================= FILTRO DE JORNADA =================
    frame_filtro = tk.Frame(ventana_fechas, bg="#f8f8f8")
    frame_filtro.pack(pady=(5, 10))

    tk.Label(
        frame_filtro,
        text="Seleccionar jornada:",
        font=("Segoe UI", 12),
        bg="#f8f8f8"
    ).pack(side="left", padx=(0, 10))

    partidos_todos = get_partidos()
    jornadas = sorted({p[3] for p in partidos_todos})
    combo_jornada = ttk.Combobox(frame_filtro, values=jornadas, state="readonly", font=("Segoe UI", 11))
    combo_jornada.pack(side="left")
    if jornadas:
        combo_jornada.set(jornadas[0])

    # ================= TABLA =================
    frame_tabla = tk.Frame(ventana_fechas)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("idPartido", "equipo1", "equipo2", "jornada", "fecha", "hora")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
    tabla.pack(fill="both", expand=True)

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
        tabla.column(col, anchor="center", width=120)

    # ================= CARGAR DATOS =================
    def cargar_partidos_por_jornada(*_):
        tabla.delete(*tabla.get_children())
        seleccion = combo_jornada.get()
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
        # Permite 2025-10-05 o 2025-10-5
        if not re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", fecha):
            return False
        try:
            anio, mes, dia = map(int, fecha.split("-"))
            datetime.date(anio, mes, dia)
            return True
        except ValueError:
            return False

    def validar_hora(hora):
        # Permite 9:00 o 09:00
        if not re.match(r"^\d{1,2}:\d{2}$", hora):
            return False
        h, m = map(int, hora.split(":"))
        return 0 <= h < 24 and 0 <= m < 60

    # ================= GUARDAR CAMBIOS =================
    def guardar_fechas():
        filas = tabla.get_children()
        cambios = 0  # Contador de partidos actualizados

        for f in filas:
            valores = tabla.item(f, "values")
            idp, _, _, _, fecha, hora = valores

            # Si no hay datos, ignorar
            if not fecha.strip() and not hora.strip():
                continue

            # Validar solo si hay datos
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
    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones,
        text="Guardar Fechas",
        font=("Segoe UI", 12),
        bg="#4CAF50",
        fg="white",
        command=guardar_fechas,
        width=15,
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botones,
        text="Cerrar",
        font=("Segoe UI", 12),
        bg="#F44336",
        fg="white",
        command=ventana_fechas.destroy,
        width=15,
    ).grid(row=0, column=1, padx=10)
