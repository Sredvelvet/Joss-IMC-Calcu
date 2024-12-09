import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def dibujar_medidor(imc):
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'polar': True})

    # Colores para las diferentes categorías
    categorias = [
        (0, 18.5, 'lightblue'),
        (18.5, 24.9, 'lightgreen'),
        (25, 29.9, 'yellow'),
        (30, 40, 'pink')
    ]

    # Dibujar las secciones del medidor
    for start, end, color in categorias:
        ang = np.linspace(np.pi * (start / 40), np.pi * (end / 40), 100)
        ax.fill_between(ang, 0, 1, color=color, alpha=0.7)

    # Dibujar la aguja del IMC
    ang_imc = np.pi * (imc / 40)
    ax.plot([ang_imc, ang_imc], [0, 1], color='red', linewidth=3)

    # Etiquetas de las categorías
    etiquetas = ['Bajo peso', 'Normal', 'Sobrepeso', 'Obesidad']
    for i, (start, end, label) in enumerate(zip([0, 18.5, 25, 30], [18.5, 24.9, 29.9, 40], etiquetas)):
        ang_label = np.pi * ((start + end) / 2 / 40)
        ax.text(ang_label, 0.5, label, horizontalalignment='center', fontsize=10, color='black')

    # Configurar el eje
    ax.set_yticklabels([])
    ax.set_xticks(np.pi * np.linspace(0, 1, 9))
    ax.set_xticklabels(['0', '5', '10', '15', '20', '25', '30', '35', '40'])

    return fig

def mostrar_medidor():
    try:
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
        if peso < 0 or altura < 0:
            raise ValueError("El peso y la altura no pueden ser negativos")
        imc = calcular_imc(peso, altura)
        fig = dibujar_medidor(imc)

        # Mostrar el gráfico en el Canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def mostrar_recomendaciones():
    try:
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
        if peso < 0 or altura < 0:
            raise ValueError("El peso y la altura no pueden ser negativos")
        imc = calcular_imc(peso, altura)
        if imc < 18.5:
            messagebox.showinfo("Resultados", "Basado en su IMC= {:.2f}. Usted presenta bajo peso.\nRecomendaciones: Consuma más calorías saludables.".format(imc))
        elif 18.5 <= imc <= 24.9:
            messagebox.showinfo("Resultados", "Basado en su IMC= {:.2f}. Usted presenta peso normal.\nRecomendaciones: Mantenga una dieta balanceada y ejercicio regular.".format(imc))
        elif 25 <= imc <= 29.9:
            messagebox.showinfo("Resultados", "Basado en su IMC= {:.2f}. Usted presenta sobrepeso.\nRecomendaciones: Incrementar la actividad física y controlar la ingesta calórica.".format(imc))
        elif 30 <= imc <= 39.9:
            messagebox.showinfo("Resultados", "Basado en su IMC= {:.2f}. Usted presenta obesidad.\nRecomendaciones: Consulte a un profesional de la salud para un plan personalizado.".format(imc))
        else:
            messagebox.showinfo("Resultados", "Basado en su IMC= {:.2f}. Usted presenta obesidad mórbida.\nRecomendaciones: Es esencial buscar atención médica especializada.".format(imc))
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
window = tk.Tk()
window.title("Calculadora de IMC con Medidor")
#Etiqueta

label = tk.Label(window,
                    text="Ingrese para calcular su IMC",
                    font=("Arial", 10, "bold"),
                    fg="white",
                    bg="lightblue",
                    width=50,
                    height=2,
                    padx=10,
                    pady=5
                    )
label.pack(pady=10)

# Frame para los campos de entrada
frame_entrada = tk.Frame(window)
frame_entrada.pack(pady=20)

tk.Label(frame_entrada, text="Peso (kg):").grid(row=0, column=0, padx=5)
entry_peso = tk.Entry(frame_entrada)
entry_peso.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Altura (m):").grid(row=1, column=0, padx=5)
entry_altura = tk.Entry(frame_entrada)
entry_altura.grid(row=1, column=1, padx=5)

# Botón para mostrar el medidor
boton = tk.Button(window, text="Calcular IMC", command=mostrar_medidor)
boton.pack(pady=20)

# Botón para mostrar recomendaciones
boton_recomendaciones = tk.Button(window, text="Mostrar Recomendaciones", command=mostrar_recomendaciones)
boton_recomendaciones.pack(pady=5)

# Frame para el gráfico
frame_grafico = tk.Frame(window)
frame_grafico.pack(pady=20)

# Iniciar el bucle principal
window.mainloop()
