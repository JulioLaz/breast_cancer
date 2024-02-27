from flask import Flask, render_template, request
import pandas as pd
from models import predecir_tumor
from visitas import contar_visitas

def crear_app():

    app = Flask(__name__, template_folder="templates")

    @app.route('/')
    def index():
        total_visitas = contar_visitas()
        return render_template('index.html', total_visitas=total_visitas)

    @app.route('/predecir', methods=['POST'])
    def predecir():
        try:
            if request.method == 'POST':
                datos = {
                    'radio_promedio' : float(request.form['radio_promedio']),
                    'textura_promedio' : float(request.form['textura_promedio']),
                    'perimetro_promedio' : float(request.form['perimetro_promedio']),
                    'area_promedio' : float(request.form['area_promedio']),
                    'suavidad_promedio': 0.,
                    'compacidad_promedio' : float(request.form['compacidad_promedio']),
                    'concavidad_promedio' : float(request.form['concavidad_promedio']),
                    'puntos_concavos_promedio' : float(request.form['puntos_concavos_promedio']),
                    'simetria_promedio' : float(request.form['simetria_promedio']),
                    'dimension fractal promedio': 0,

                    'radio_se' : float(request.form['radio_se']),
                    'textura se': 0,
                    'perimetro_se' : float(request.form['perimetro_se']),
                    'area_se' : float(request.form['area_se']),
                    'suavidad_se' : float(request.form['suavidad_se']),
                    'compacidad_se' : float(request.form['compacidad_se']),
                    'concavidad se':0,
                    'puntos_concavos_se' : float(request.form['puntos_concavos_se']),
                    'simetria_se' : float(request.form['simetria_se']),
                    'dimension_fractal_se' : float(request.form['dimension_fractal_se']),

                    'radio_peor' : float(request.form['radio_peor']),
                    'textura_peor' : float(request.form['textura_peor']),
                    'perimetro_peor' : float(request.form['perimetro_peor']),
                    'area_peor' : float(request.form['area_peor']),
                    'suavidad_peor' : float(request.form['suavidad_peor']),
                    'compacidad peor':0,
                    'concavidad_peor' : float(request.form['concavidad_peor']),
                    'puntos_concavos_peor' : float(request.form['puntos_concavos_peor']),
                    'simetria_peor' : float(request.form['simetria_peor']),
                    'dimension fractal peor': 0
            }
            df = pd.DataFrame.from_dict(datos, orient='index', columns=['valor'])
            resultado = predecir_tumor(df.valor)
            return render_template('resultado.html', resultado=(resultado[0],resultado[1][0],resultado[2]),acierto=resultado[3],pronostico=resultado[0],result=resultado[4],color=resultado[5])
        
        except Exception as e:
            mensaje_error = f"Error durante la predicción: {str(e)}"
            print(mensaje_error)
            return f"Error: {mensaje_error}", 500
    
    @app.route('/info')
    def info():
            with open('wdbc.txt', 'r') as f:
                contenido = f.read()
            return render_template('/info.html', contenido=contenido)
    
    return app

if __name__ == '__main__':
    app=crear_app()
    app.run(debug=True)
