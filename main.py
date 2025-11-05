import tkinter as tk
from views.menu_principal import menu_principal
from views.menu_torneo import pantalla_configuracion

def crear_datos():
    # Tu función para simular partido
    print("Simulando torneo...")

def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Torneo de Fútbol")
    ventana.geometry("800x350")

    # Función para abrir configuración y pasar menú principal como callback
    def abrir_configuracion():
        pantalla_configuracion(ventana, volver_menu=lambda: menu_principal(ventana, abrir_configuracion))

    menu_principal(ventana, abrir_configuracion)
    ventana.mainloop()

if __name__ == "__main__":
    main()
