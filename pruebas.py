import tkinter as tk
from tkinter import messagebox
import random

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
        self.contador()
        self.widgets()
        self.mapeado()
        

    # 0 para jugar normal | 1 para mapeado resuelto con su final
    def mapeado(self):
        if self.eleccion_mapeado == 0:
            self.random_bombas()
        elif self.eleccion_mapeado == 1:
            self.random_bombas_mapeado()

    def widgets(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=5, height=2, bg="grey", state="normal")
                button.grid(row=row, column=col)
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
                self.verificar_bomba(row, col)
    
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)

    def contar_bombas_cercanas(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) in self.bombas:
                    count += 1
        return " " if count == 0 else count

  
                        


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
            if bombas_cercanas == " ":
                self.expandir_casillas_vacias(row, col)  # Aquí se invoca la función para expandir casillas
            else:
                self.buttons[(row, col)].config(text=bombas_cercanas, bg="white")
            

    # Función añadida para expandir las casillas vacías alrededor de una casilla sin bombas cercanas
    def expandir_casillas_vacias(self, row, col):
        casillas_procesadas = set()
        cola_casillas = [(row, col)]
        while cola_casillas:
            r, c = cola_casillas.pop(0)
            if (r, c) not in casillas_procesadas and (r, c) not in self.bombas:
                casillas_procesadas.add((r, c))
                bombas_cercanas = self.contar_bombas_cercanas(r, c)
                self.buttons[(r, c)].config(text=bombas_cercanas, bg="white")
                self.casillas_desbloqueadas += 1
                if bombas_cercanas == " ":
                    for ri in range(max(0, r-1), min(self.rows, r+2)):
                        for ci in range(max(0, c-1), min(self.cols, c+2)):
                            if (ri, ci) not in casillas_procesadas:
                                cola_casillas.append((ri, ci))

    def marcar_bomba(self, row, col):
        if self.buttons[(row, col)]['bg'] == "white":
            return "break"
        elif self.buttons[(row, col)]['text'] == '🚩':
            self.buttons[(row, col)]['text'] = ''
            self.banderas += 1
        elif self.banderas > 0 and self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = '🚩'
            self.banderas -= 1
        self.actualizar_banderas()

    def contador(self):
        self.s = 0
        self.m = 0
        self.label_tiempo = tk.Label(self.ventana, text='', width=12, height=2, bg="white", fg="black")
        self.label_tiempo.grid(row=self.rows, columnspan=3)
        self.label_banderas = tk.Label(self.ventana, text='', width=20, height=2, bg="white", fg="black")
        self.label_banderas.grid(row=self.rows, column=3, columnspan=self.cols-3)
        self.actualizar_banderas()
        self.actualizar_tiempo()

    def actualizar_banderas(self):
        self.label_banderas.config(text=f"Banderas restantes: {self.banderas} 🚩")

    def actualizar_tiempo(self):
        if self.estado == True: # Se verifica si el juego aún está en curso    
            tiempo = f"Tiempo: {self.m:02d}:{self.s:02d} ⏳"
            self.label_tiempo.config(text=tiempo)
            self.s += 1
            if self.s == 60:
                self.s = 0
                self.m += 1
            self.ventana.after(1000, self.actualizar_tiempo)
            
        else:
            self.final_juego(self.s, self.m)

    def final_juego(self, s, m):
        tiempo = f"Tiempo: {m:02d}:{s:02d}"
        total_casillas = self.cols * self.rows
        ventana_estadisticas = tk.Toplevel()
        ventana_estadisticas.title("Estadísticas")
        ventana_estadisticas.geometry("250x200")
        estadisticas = f"FIN DEL JUEGO\n ¡Has perdido!\n\n{tiempo}\nTamaño del tablero: {total_casillas} casillas"
        tk.Label(ventana_estadisticas, text=estadisticas).pack()

        # Se desactivan los botones del juego para evitar más interacciones después de finalizar el juego.
        for button in self.buttons.values():
            #button.config(state=tk.DISABLED)
            button.unbind('<Button-1>')
            button.unbind('<Button-3>')




def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    root.config(bg="black")
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
