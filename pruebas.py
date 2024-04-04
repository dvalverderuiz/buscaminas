import tkinter as tk
from tkinter import messagebox
import random
import time

# 0 para mapeado sin mostrar minas | 1 para mapeado con minas mostradas

class Buscaminas:
    def __init__(self, ventana, rows, cols, nbombas, banderas, eleccion_mapeado):
        self.eleccion_mapeado = eleccion_mapeado
        self.casillas_desbloqueadas = 0
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.banderas = banderas
        self.nbombas = nbombas
        self.buttons = {}
        self.bombas = set()
        self.estado = True
        self.widgets()
        self.mapeado()
        self.contador()
        
    def mapeado(self):
        if self.eleccion_mapeado == 0:
            self.random_bombas()
        elif self.eleccion_mapeado == 1:
            self.random_bombas_mapeado()

    def widgets(self):        
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=5, height=2, bg="pale green", state="normal")
                button.grid(row=row, column=col)
                #button.config(command=lambda r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-1>', lambda event, r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.marcar_bomba(r, c))
                self.buttons[(row, col)] = button
    
    
    def random_bombas_mapeado(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)    
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.bombas:
                    for position, button in self.buttons.items():
                        if position in self.bombas:
                            button.config(text='💣', bg="tomato")
            
            
                    
    
    
    
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)
            
    def contar_bombas_cercanas(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if (r, c) in self.bombas:
                        count+=1                
        if(count == 0):
            return " "
        else:
            return count
        
    def verificar_bomba(self, row, col):
        if self.buttons[(row, col)]['text'] == '🚩':
            return "break"
        elif (row, col) in self.bombas:
            self.estado = False
            for position, button in self.buttons.items():
                if position in self.bombas:
                    button.config(text='💣', bg="tomato")
        else:
            bombas_cercanas = self.contar_bombas_cercanas(row, col)
            if bombas_cercanas == 0:
                self.expandir_casillas_vacias(row, col, bombas_cercanas)
            else:
                self.buttons[(row, col)].config(text=bombas_cercanas, bg="bisque")
            self.casillas_desbloqueadas += 1             
                 
   
    
    def marcar_bomba(self, row, col):
        if self.buttons[(row, col)]['bg'] == "bisque":
            return "break"
        elif self.buttons[(row, col)]['text'] == '🚩':
            self.buttons[(row, col)]['text'] = ''
            self.banderas = self.banderas + 1
            self.actualizar_banderas()
        elif self.banderas < 1:
            return "break"
        elif self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = '🚩'
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
                for e in range(self.rows):
                    for f in range(self.cols):
                        self.buttons[(e, f)]['state'] = tk.DISABLED
                        for button in self.buttons.values():
                            button.unbind('<Button-1>')
                            button.unbind('<Button-3>')

        self.ventana.after(1000, self.actualizar_tiempo)


    def final_juego(self, s, m, casillas_desbloqueadas):
        
        tiempo = f"Tiempo: {self.m:02d}:{self.s:02d}"
        total_casillas = self.cols * self.rows
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
            # 0 para mapeado sin mostrar minas | 1 para mapeado con minas mostradas
            eleccion_mapeado = 0
            enviar_valores(row, col, nbombas, banderas, eleccion_mapeado)
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
                eleccion_mapeado = 0
                try:
                    col = int(col)
                    row = int(row)
                    banderas = int(banderas)
                    nbombas = int(nbombas)
                    maximo_bombas = (col * row) / 3 
                except ValueError:
                    print("No se ha podido convertir a INT")
                    print(col, row, banderas, nbombas, maximo_bombas)

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
                    enviar_valores(row, col, nbombas, banderas, eleccion_mapeado)

            boton_confirmar = tk.Button(nueva_ventana, text="Confirmar", command=obtener_valores)
            boton_confirmar.pack()

            nueva_ventana.mainloop()
        elif eleccion == "mapeado":
            row = 10
            col = 10
            nbombas = 10
            banderas = nbombas
            # 0 para mapeado sin mostrar minas | 1 para mapeado con minas mostradas
            eleccion_mapeado = 1
            enviar_valores(row, col, nbombas, banderas, eleccion_mapeado)
        else:
            print("")

    def enviar_valores(row, col, nbombas, banderas, eleccion_mapeado):
        Buscaminas(root, row, col, nbombas, banderas, eleccion_mapeado)

    boton_facil = tk.Button(root, text="Fácil", command=lambda: configurar_eleccion("facil"))
    boton_facil.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_facil.place(x="55", y="55")

    boton_personalizado = tk.Button(root, text="Personalizado", command=lambda: configurar_eleccion("personalizado"))
    boton_personalizado.config(cursor="hand2", bg="goldenrod", relief="flat", width=12, height=1, font=("Calisto MT", 12, "bold"))
    boton_personalizado.place(x="35", y="100")
    
    boton_mapeado = tk.Button(root, text="Mapeado", command=lambda: configurar_eleccion("mapeado"))
    boton_mapeado.config(cursor="hand2", bg="goldenrod", relief="flat", width=12, height=1, font=("Calisto MT", 12, "bold"))
    boton_mapeado.place(x="35", y="145")
    root.mainloop()

if __name__ == "__main__":
    main()
