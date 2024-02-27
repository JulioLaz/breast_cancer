import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV

def predecir_tumor(data):
    global selected_columns_rfecv

    df = pd.read_csv('data_cancer_final.csv')
    X = df.drop(columns='diagnostico', axis=1)
    y = df.diagnostico

    scaler = StandardScaler()
    scaler.fit(X)

    X_std = scaler.transform(X)
    data= scaler.transform([data])

    ### Crear df con data estandarizadods:
    df_data_std = pd.DataFrame(data, columns= X.keys())

    X_train, X_test, y_train, y_test = train_test_split(X_std, y, random_state= 42, test_size= 0.3)
    
    logistic_regression = LogisticRegression(C=1, n_jobs=-1)
    rfecv_logistic = RFECV(estimator=logistic_regression, cv=5, scoring='accuracy')

    # Ajustar el selector de características al conjunto de entrenamiento
    rfecv_logistic.fit(X_train, y_train)

    # Transformar los conjuntos de entrenamiento y prueba
    rfecv_train = rfecv_logistic.transform(X_train)
    rfecv_test = rfecv_logistic.transform(X_test)

    # Crear un clasificador de regresión logística con características seleccionadas
    logistic_selected = LogisticRegression(C=1, n_jobs=-1)

    # Entrenar el clasificador con características seleccionadas
    logistic_selected.fit(rfecv_train, y_train)

    # Predicciones logistic
    y_pred_lg = logistic_selected.predict(rfecv_test)

    # Calcular métricas logistic:
    # accuracy_logistic = logistic_selected.score(rfecv_test, y_test)
    precision_logistic = precision_score(y_test, y_pred_lg)
    recall_logistic = recall_score(y_test, y_pred_lg)
    # f1_logistic = f1_score(y_test, y_pred_lg)
    # conf_matrix_logistic = confusion_matrix(y_test, y_pred_lg)

    # Obtener los índices de las características seleccionadas
    selected_columns_indices = rfecv_logistic.support_
    selected_columns_rfecv = X.columns[selected_columns_indices]
    columnas=X.columns[selected_columns_indices]
    df_pronticar=df_data_std[columnas]
 
    probabilidades_predichas = logistic_selected.predict_proba(df_pronticar)
    prediccion = logistic_selected.predict(df_pronticar)

   # Seleccionar las probabilidades de la clase 1 (default)
    probabilidades_tumor_maligno = probabilidades_predichas[:, 1]

   # Establecer un umbral para determinar la clase
    umbral = 0.5
    prediccion_binaria = (probabilidades_tumor_maligno > umbral).astype(int)

   # Calcular el porcentaje de acierto para la clase Diagnóstico: Maligno:
    if prediccion_binaria[0] == 1:
      porcentaje_acierto_tumor_maligno = probabilidades_tumor_maligno[prediccion_binaria == 1].mean()
    else:
      porcentaje_acierto_tumor_maligno = probabilidades_tumor_maligno[prediccion_binaria == 0].mean()

    if prediccion_binaria[0] == 1:
      # result= f'Tumor Maligo. Porcentaje de acierto: {porcentaje_acierto_tumor_maligno * 100:.2f}%'
      porc_acierto=round(porcentaje_acierto_tumor_maligno * 100)
      result=f'El modelo puede identificar correctamente el {recall_logistic:.0%} de los casos de tumores malignos en el conjunto de datos de prueba.'
    else:
      # result=f'Tumor Benigno. Porcentaje de acierto: {(1 - porcentaje_acierto_tumor_maligno) * 100:.2f}%'
      porc_acierto=round((1-porcentaje_acierto_tumor_maligno) * 100)
      result=f'El modelo puede identificar correctamente el {precision_logistic:.0%} de los casos de tumores benignos en el conjunto de datos de prueba.'
    print('prediccion:  ',prediccion)
    # print('probabilidades_predichas:  ',probabilidades_predichas[0],type(probabilidades_predichas[0]))
    if 0 == prediccion[0]:
        mensaje = "Tumor benigno"
        color="no"
    else:
        mensaje = "Tumor maligno"
        color="si"
    return result,prediccion_binaria,porcentaje_acierto_tumor_maligno,porc_acierto,mensaje,color
