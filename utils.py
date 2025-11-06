from controllers.pool import conectar   
from models.torneo import Torneo
def tabla_posiciones():
    """
    Genera la tabla de posiciones general basada en los puntos acumulados de cada equipo.
    Muestra el identificador (A1, B3, etc.), el país y los puntos totales.
    Retorna una lista de tuplas: [(identificador, pais, puntos), ...]
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            e.identificador,
            e.pais,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.puntosEquipoUno ELSE 0 END
            ), 0)
            +
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoDos = e.identificador THEN p.puntosEquipoDos ELSE 0 END
            ), 0)
            AS puntos_totales
        FROM equipos e
        LEFT JOIN partido p
        ON e.identificador = p.identificadorEquipoUno
        OR e.identificador = p.identificadorEquipoDos
        GROUP BY e.identificador, e.pais
        ORDER BY puntos_totales DESC;
    """)
    tabla = cursor.fetchall()
    conn.close()

    # Mostrar tabla en consola
    print("\nTABLA DE POSICIONES")
    print(f"{'Identificador':<15}{'País':<15}{'Puntos':<10}")
    print("-" * 40)
    for fila in tabla:
        print(f"{fila[0]:<15}{fila[1]:<15}{fila[2]:<10}")
    return tabla