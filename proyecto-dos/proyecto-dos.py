import tkinter as tk
from client.gui_registrar_aeropuerto_app import FrameRegisterAirport
from client.gui_registrar_ruta import FrameRegisterRute
from client.gui_ver_rutas import FrameViewRutes
from client.gui_buscar_ruta import FrameSearchRute

class main():
    def __init__(self):
        root = tk.Tk()
        root.title('Proyecto dos')
        root.iconbitmap('img/grafo.ico')
        # root.resizable(0, 0)
        
        self.nav_bar(root)
        self.current_frame = FrameRegisterAirport(root = root)
        
        root.mainloop()
    
    def nav_bar(self, root):
        nav_bar = tk.Menu(root)
        root.config(menu=nav_bar, width=500, height=500)
        
        # menu_registro_aeropuertos = tk.Menu(nav_bar, tearoff=0)
        # nav_bar.add_cascade(label='Registro de aeropuertos', menu=menu_registro_aeropuertos)
        
        # menu_registro_aeropuertos.add_command(label='crear aeropuerto')
        # menu_registro_aeropuertos.add_command(label='eliminar aeropuerto')
        # menu_registro_aeropuertos.add_command(label='salir', command=root.destroy)
        
        nav_bar.add_cascade(label='Registro de aeropuertos', command=lambda: self.show_frame(FrameRegisterAirport(root = root)))
        
        record_routes = tk.Menu(nav_bar, tearoff=0)
        nav_bar.add_cascade(label='Registro de rutas', menu=record_routes)
        record_routes.add_command(label='registrar ruta', command=lambda: self.show_frame(FrameRegisterRute(root = root)))
        record_routes.add_command(label='buscar ruta', command=lambda: self.show_frame(FrameSearchRute(root = root)))
        record_routes.add_command(label='ver rutas', command=lambda: self.show_frame(FrameViewRutes(root = root)))
        
        nav_bar.add_cascade(label='salir', command=root.destroy)

    def show_frame(self, frame):
        self.current_frame.destroy()
        
        self.current_frame = frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)

main()
