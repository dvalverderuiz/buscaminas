import tkinter as tk
from tkinter import messagebox
import random
import time


class Buscaminas:
    def __init__(self, ventana, rows, cols, nbombas, banderas):
        self.casillas_desbloqueadas = 0
        estado = True
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.banderas = banderas
        self.nbombas = nbombas
        self.buttons = {}
        self.bombas = set()
        self.estado = estado
        self.widgets()
        self.random_bombas()
        self.contador()
        
    def widgets(self):        
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=5, height=2, bg="pale green")
                button.grid(row=row, column=col)
                #button.config(command=lambda r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-1>', lambda event, r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.marcar_bomba(r, c))
                self.buttons[(row, col)] = button
                
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)
        
    def verificar_bomba(self, row, col):
        if self.buttons[(row, col)]['text'] == 'B':
            return "break"
        elif (row, col) in self.bombas:
            self.estado = False
            for position, button in self.buttons.items():
                if position in self.bombas:
                    button.config(text='*', bg="tomato")         
        else:
            self.casillas_desbloqueadas = self.casillas_desbloqueadas + 1
            self.buttons[(row, col)].config(text='', bg="bisque")
            
    
    
    
    def marcar_bomba(self, row, col):
        if self.buttons[(row, col)]['bg'] == "bisque":
            return "break"
        elif self.buttons[(row, col)]['text'] == 'B':
            self.buttons[(row, col)]['text'] = ''
            self.banderas = self.banderas + 1
            self.actualizar_banderas()
        elif self.banderas < 1:
            return "break"
        elif self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = 'B'
            self.banderas = self.banderas - 1
            self.actualizar_banderas()
        
        return "break"
    
       
    def contador(self):
        self.s = 0
        self.m = 0

        self.label_tiempo = tk.Label(self.ventana, text='', width=10, height=2, bg="white", fg="black")
        self.label_tiempo.grid(row=self.rows, columnspan=2)
        self.label_banderas = tk.Label(self.ventana, text='', width=20, height=2, bg="white", fg="black")   

        self.label_banderas.grid(row=self.rows, columnspan=20)
        
        self.actualizar_banderas()
        self.actualizar_tiempo()
        
        
    def actualizar_banderas(self):
        self.label_banderas.config(text=f"Banderas restantes: {self.banderas}")
    
    
    def actualizar_tiempo(self):
        tiempo = f"Tiempo: {self.m:02d}:{self.s:02d}"
        self.label_tiempo.config(text=tiempo)
        self.s += 1
        if self.s == 60:
            self.s = 0
            self.m += 1
        elif self.estado == False:
            for i in range(1):
                self.final_juego(self.s, self.m, self.casillas_desbloqueadas) 
                self.estado = True
        self.ventana.after(1000, self.actualizar_tiempo)


    def final_juego(self, s, m, casillas_desbloqueadas):
        self.ventana.destroy()
        tiempo = f"Tiempo: {self.m:02d}:{self.s:02d}"
        total_casillas = self.cols * self.rows

        # Añadir funcion de contar las casillas beige. Para mostrar en estadisticas.
        


        print("Fin del juego")
        ventana_estadisticas = tk.Tk()
        ventana_estadisticas.title("Estadisticas")
        ventana_estadisticas.geometry("250x500")
        titulo = tk.Label(ventana_estadisticas, text="\nFIN DEL JUEGO \n\n\n ESTADISTICAS:\n ")
        titulo.pack()
        tiempo_stat = tk.Label(ventana_estadisticas, text=tiempo)
        tiempo_stat.pack()
        total_casillas_stat = tk.Label(ventana_estadisticas, text=f"Tamaño del tablero: {total_casillas} casillas")
        total_casillas_stat.pack()
        casillas_pulsadas_stat = tk.Label(ventana_estadisticas, text=f"Casillas desbloqueadas: {self.casillas_desbloqueadas}")
        casillas_pulsadas_stat.pack()
        #self.ventana.destroy()



def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    root.config(bg="SlateBlue2")
    def configurar_eleccion(opcion):
        #global eleccion
        eleccion = opcion
        verificar_nivel(eleccion)
    def verificar_nivel(eleccion):
        if eleccion == "facil":
            row = 10
            col = 10
            nbombas = 10
            banderas = nbombas 
            enviar_valores(row, col, nbombas, banderas)
        elif eleccion == "medio":
            row = 15
            col = 15
            nbombas = 15
            banderas = nbombas 
            enviar_valores(row, col, nbombas, banderas)         
        elif eleccion == "dificil":
            row = 20
            col = 20
            nbombas = 20
            banderas = nbombas 
            enviar_valores(row, col, nbombas, banderas)
        elif eleccion == "personalizado":
            nueva_ventana = tk.Toplevel()
            nueva_ventana.title("Buscaminas personalizado")
            nueva_ventana.geometry("500x250")

            row1 = tk.Entry(nueva_ventana)
            row1.insert(0, "")
            row_label = tk.Label(nueva_ventana, text="Número de filas:")
            row_label.place(x="90", y="0")
            row1.pack()

            col1 = tk.Entry(nueva_ventana)
            col1.insert(0, "")
            col_label = tk.Label(nueva_ventana, text="Número de columnas:")
            col_label.place(x="60", y="20")
            col1.pack()

            nbombas1 = tk.Entry(nueva_ventana)
            nbombas1.insert(0, "")
            nbombas_label = tk.Label(nueva_ventana, text="Número de bombas:")
            nbombas_label.place(x="70", y="40")
            nbombas1.pack()

            def obtener_valores():
                nbombas = nbombas1.get()
                banderas = nbombas
                col = col1.get()
                row = row1.get()
                
                try:
                    col = int(col)
                    row = int(row)
                    banderas = int(banderas)
                    nbombas = int(nbombas)
                    maximo_bombas = (col * row) / 3 
                except ValueError:
                    print("Error")

                # Control de errores: Campo personalizado
                if not isinstance(col, int) or not isinstance(row, int) or not isinstance(nbombas, int):
                    messagebox.showwarning(title="Advertencia", message="Los campos no pueden estar vacios ni contener letras.")
                    return "break"
                elif col and row < 10:
                    messagebox.showwarning(title="Advertencia", message="Dimensiones mínimas: 10x10")
                    return "break"
                elif nbombas > maximo_bombas:
                    messagebox.showwarning(title="Advertencia", message=f"Demasiadas bombas para el tablero seleccionado, solo se permiten una tercera parte del total de casillas. \n\n Max: {maximo_bombas:.0f} bombas")
                    return "break"
                elif col > 42 or row > 24:
                    messagebox.showwarning(title="Advertencia", message=f"Medidas maximas: 24 filas x 42 columnas")
                    return "break"
                else:
                    nueva_ventana.destroy()
                    enviar_valores(row, col, nbombas, banderas)

            boton_confirmar = tk.Button(nueva_ventana, text="Confirmar", command=obtener_valores)
            boton_confirmar.pack()

            nueva_ventana.mainloop()
        else:
            print("")

    def enviar_valores(row, col, nbombas, banderas):
        Buscaminas(root, row, col, nbombas, banderas)

    



    boton_facil = tk.Button(root, text="Fácil", command=lambda: configurar_eleccion("facil"))
    boton_facil.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_facil.place(x="55", y="20")

    boton_mediano = tk.Button(root, text="Medio", command=lambda: configurar_eleccion("medio"))
    boton_mediano.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_mediano.place(x="55", y="60")

    boton_dificil = tk.Button(root, text="Dificil", command=lambda: configurar_eleccion("dificil"))
    boton_dificil.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_dificil.place(x="55", y="100")
    
    boton_personalizado = tk.Button(root, text="Personalizado", command=lambda: configurar_eleccion("personalizado"))
    boton_personalizado.config(cursor="hand2", bg="goldenrod", relief="flat", width=12, height=1, font=("Calisto MT", 12, "bold"))
    boton_personalizado.place(x="35", y="140")
    
    root.mainloop()

if __name__ == "__main__":
    main()
