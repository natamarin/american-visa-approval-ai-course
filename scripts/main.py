import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Cargar los datos
def cargar_datos(archivo_entrada='C:/Users/juanim/OneDrive - Caja de Compensacion Familiar de Antioquia COMFAMA/P.VISA/american-visa-approval-ai-course/datosProcesar/datos.csv'):
    data = pd.read_csv(archivo_entrada , header=0 , encoding='utf-8', sep=';')

# Preprocesamiento de los datos
def preprocesar_datos(data):
    #X = data.drop('y', axis=1)  
    #y = data['y']  
    # Dividir los datos en características (X) y etiqueta (y)

    y = data[["y"]]# La variable dependiente 'y'
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
    return model

# Evaluar el modelo
def evaluar_modelo(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Loss: {loss}")
    print(f"Accuracy: {accuracy}")
    print("Ahora vamos a hacer un pronostico....")

def Pronostico(model):
    x1=input("Ingresa la edad")
    x2=input("Ingresa el salario mensual")
    x3=input("Escribe 1 si te han negado la visa antes o 0 si no la han negado")
    x4=input("Escribe 1 si tus padres vive en USA, 0 si no")
    x5=input("Escribe 1 si tienes familia en USA, 0 si no")
    x6=input("Escribe 1 si tienes conocidos en USA, 0 si no")
    x7=input("Escribe 1 si eres casado o 0 si no eres casado")
    x8=input("Escribe 1 si estas en union libre o 0 estas en union libre")
    x9=input("Escribe 1 si eres soltero o 0 si no eres soltero")
    x10=input("Escribe 1 si eres viudo o 0 si no eres viudo")
    x11=input("Ingresa 1 si has viado al exterior o 0 en caso contrario")
    inputs=[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11]
    result = model.predict(inputs).flatten()   
    if result == 1:
        result = "Segun la informacion la visa seria aprobada"
    else:    
        result = "Segun la informacion la visa seria negada"
    
    return print(result)

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

    # Realizar Pronosticos con datos de Entrada nuevoa
    # Pronostico(model)


if __name__ == "__main__":
    main()