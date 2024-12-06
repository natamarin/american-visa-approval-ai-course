import pandas as pd
import numpy as np
import tkinter as tk
import joblib as jb
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Cargar los datos
def cargar_datos(archivo_entrada='/Users/natalia.marin/Documents/CursoTalentTech/Taller2/datosProcesar/datos.csv'):
    data = pd.read_csv(archivo_entrada , header=0 , encoding='utf-8', sep=';')
    return data

# Preprocesamiento de los datos
def preprocesar_datos(data):
    # Dividir los datos en características (X) y etiqueta (y)

    y = data[['y']] # La variable dependiente 'y'
    X = data.iloc[:,0:11] # Todas las columnas excepto 'y'
    # Las variables edad y sueldo ya están normalizadas, no es necesario escalarlas nuevamente.
    # Se puede proceder directamente con las variables binarias y las normalizadas (edad, sueldo).
    return X, y

# Dividir los datos en entrenamiento, validación y prueba
def dividir_datos(X, y):
    # Dividir los datos en conjunto de entrenamiento (35,000), conjunto de validación (4,000) y conjunto de prueba (1,000)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.1, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.1, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test

# Definir el modelo de red neuronal
def crear_modelo(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='sigmoid'))  # Capa de entrada
    model.add(Dense(32, activation='sigmoid'))  # Capa oculta
    model.add(Dense(1, activation='sigmoid'))  # Salida con activación sigmoidea para probabilidad
    
    # Compilar el modelo
    model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    return model

# Entrenar el modelo
def entrenar_modelo(model, X_train, y_train, X_val, y_val):
    model.fit(X_train, y_train, epochs=20, batch_size=128, validation_data=(X_val, y_val), verbose=1)
    
    # Guardar el modelo entrenado como pkl
    jb.dump(model, '/Users/natalia.marin/Documents/CursoTalentTech/Taller2/modelo/modelo_entrenado.pkl')
    return model

# Evaluar el modelo
def evaluar_modelo(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Loss: {loss}")
    print(f"Accuracy: {accuracy}")
    print("Ahora vamos a hacer un pronostico....")
    
def predecir_y_mostrar_interfaz():
    def on_submit():
        inputs = [
            entry_age.get(),
            entry_salary.get(),
            entry_visa_denied.get(),
            entry_parents_usa.get(),
            entry_family_usa.get(),
            entry_friends_usa.get(),
            entry_married.get(),
            entry_cohabiting.get(),
            entry_single.get(),
            entry_widowed.get(),
            entry_traveled_abroad.get()
        ]
        inputs_array = np.array(inputs).astype(float).reshape(1, -1)
        result = model.predict(inputs_array)
        if result[0] >= 0.5:
            messagebox.showinfo("Resultado", "Segun la información dada, la visa sería APROBADA")
        else:
            messagebox.showinfo("Resultado", "Segun la información dada, la visa sería NEGADA")
        root.destroy()

    root = tk.Tk()
    root.title("Información del Usuario")

    tk.Label(root, text="Edad:", anchor='w').grid(row=0, sticky='w')
    tk.Label(root, text="Salario mensual:", anchor='w').grid(row=1, sticky='w')
    tk.Label(root, text="Te han negado la visa americana? Si:1, No:0", anchor='w').grid(row=2, sticky='w')
    tk.Label(root, text="Tus padres viven en USA? Si:1, No:0", anchor='w').grid(row=3, sticky='w')
    tk.Label(root, text="Tienes familiares en USA? Si:1, No:0", anchor='w').grid(row=4, sticky='w')
    tk.Label(root, text="Tienes conocidos en USA? Si:1, No:0", anchor='w').grid(row=5, sticky='w')
    tk.Label(root, text="Estas casado? Si:1, No:0", anchor='w').grid(row=6, sticky='w')
    tk.Label(root, text="Vives en unión libre? Si:1, No:0", anchor='w').grid(row=7, sticky='w')
    tk.Label(root, text="Estas soltero? Si:1, No:0", anchor='w').grid(row=8, sticky='w')
    tk.Label(root, text="Eres viudo? Si:1, No:0", anchor='w').grid(row=9, sticky='w')
    tk.Label(root, text="Has viajado al exterior? Si:1, No:0", anchor='w').grid(row=10, sticky='w')

    entry_age = tk.Entry(root)
    entry_salary = tk.Entry(root)
    entry_visa_denied = tk.Entry(root)
    entry_parents_usa = tk.Entry(root)
    entry_family_usa = tk.Entry(root)
    entry_friends_usa = tk.Entry(root)
    entry_married = tk.Entry(root)
    entry_cohabiting = tk.Entry(root)
    entry_single = tk.Entry(root)
    entry_widowed = tk.Entry(root)
    entry_traveled_abroad = tk.Entry(root)

    entry_age.grid(row=0, column=1)
    entry_salary.grid(row=1, column=1)
    entry_visa_denied.grid(row=2, column=1)
    entry_parents_usa.grid(row=3, column=1)
    entry_family_usa.grid(row=4, column=1)
    entry_friends_usa.grid(row=5, column=1)
    entry_married.grid(row=6, column=1)
    entry_cohabiting.grid(row=7, column=1)
    entry_single.grid(row=8, column=1)
    entry_widowed.grid(row=9, column=1)
    entry_traveled_abroad.grid(row=10, column=1)

    tk.Button(root, text='Hacer Predicción', command=on_submit).grid(row=11, column=0, columnspan=2, pady=4, sticky='ew')

    root.mainloop()

# Load the saved model
model = jb.load('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/modelo/modelo_entrenado.pkl')


def main():
    # Cargar los datos
    data = cargar_datos()
    
    # Preprocesar los datos
    X, y = preprocesar_datos(data)
    
    # Dividir los datos en entrenamiento, validación y prueba
    X_train, X_val, X_test, y_train, y_val, y_test = dividir_datos(X, y)
    
    # Crear el modelo de red neuronal
    model = crear_modelo(input_dim=X_train.shape[1])
    
    # Entrenar el modelo
    model = entrenar_modelo(model, X_train, y_train, X_val, y_val)
    
    # Evaluar el modelo en el conjunto de prueba
    evaluar_modelo(model, X_test, y_test)
    
    # Crear la interfaz gráfica con Tkinter
    predecir_y_mostrar_interfaz() 


if __name__ == "__main__":
    main()
    