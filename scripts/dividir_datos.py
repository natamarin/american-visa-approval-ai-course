import pandas as pd
from sklearn.model_selection import train_test_split

def dividir_datos(archivo_entrada='/Users/natalia.marin/american-visa-approval-ai-course/datosProcesar/datos.csv'):
    # Leer los datos
    data=pd.read_csv(archivo_entrada)
    
    # Dividir los datos en caracteristicas y etiquetas
    target_col='y'
    X=data.drop(target_col, axis=1)
    y=data[target_col]
    
    # Dividir los datos en conjunto de entrenamiento y conjunto temporal
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    # Dividir el conjunto temporal en conjunto de validacion y conjunto de validacion
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    # Guardar el conjunto de entrenamiento  
    X_train.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/X_train.csv', index=False)
    X_val.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/X_val.csv', index=False)
    X_test.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/X_test.csv', index=False)
    y_train.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/y_train.csv', index=False)
    y_val.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/y_val.csv', index=False)
    y_test.to_csv('/Users/natalia.marin/Documents/CursoTalentTech/Taller2/dataSet/y_test.csv', index=False)
    print('Datos divididos exitosamente')  
    