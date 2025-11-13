import tkinter as tk
from views.menu_principal import menu_principal
from controllers.pool import crear_tablas

# MAIN
def main():
    crear_tablas()
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión Torneo")
    ventana.state('zoomed')
    
    # Primer arranque: menú principal
    menu_principal(ventana)
    ventana.mainloop()
 

if __name__ == "__main__":
    main()
