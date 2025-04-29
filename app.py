from flask import Flask, render_template_string
import json
import base64
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def mostrar_graficas():
    with open('JMarketingIA(1).ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    elementos = []
    contador = 0  # Contador inicial para las gráficas

    # Define los títulos manualmente en una lista
    titulos_personalizados = [
        "0", 
        "0", 
        "0", 
        "0", 
        "0", 
        "0", 
        "0", 
        "0", 
        "0", 
        "0 ",
        "Cluster", 
        "Numero de clusters", 
        "0", 
        "0",
        "0", 
        "0",
        "0", 
        "0",
        "0", 
        "0",
        "Matriz de Correlación Ventas", 
        "Cluster",
        "0", 
        # Agrega tantos títulos como necesites
    ]

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            for output in cell.get('outputs', []):
                if 'data' in output:
                    if 'image/png' in output['data']:
                        img_base64 = output['data']['image/png']
                        # Asignar título basado en el contador
                        if contador < len(titulos_personalizados):
                            titulo = titulos_personalizados[contador]
                        else:
                            titulo = f'Gráfica {contador + 1}'  # Título por defecto si no hay más títulos
                        elementos.append({
                            'tipo': 'imagen',
                            'contenido': img_base64,
                            'titulo': titulo
                        })
                        contador += 1
                    elif 'application/vnd.plotly.v1+json' in output['data']:
                        plot_json = output['data']['application/vnd.plotly.v1+json']
                        plot_html = pio.to_html(plot_json, full_html=False, include_plotlyjs='cdn')
                        # Asignar título basado en el contador
                        if contador < len(titulos_personalizados):
                            titulo = titulos_personalizados[contador]
                        else:
                            titulo = f'Gráfica {contador + 1}'  # Título por defecto si no hay más títulos
                        elementos.append({
                            'tipo': 'plotly',
                            'contenido': plot_html,
                            'titulo': titulo
                        })
                        contador += 1

    # Filtrado de gráficas (según tus necesidades)
    elementos = elementos[10:]  # Quitar las primeras 10
    if len(elementos) > 9:
        elementos = elementos[:2] + elementos[10:]  # Quitar de la 3 a la 10
    if len(elementos) > 17:
        elementos = elementos[:13] + elementos[18:]  # Quitar de la 13 a la 17

    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MARKETING</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f2f5;
            }
            h1 {
                text-align: center;
                padding: 20px;
                color: #333;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
                max-width: 1400px;
                margin: auto;
            }
            .grafica {
                background: #ffffff;
                padding: 15px;
                border: none;  /* Eliminado el borde */
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                /* Eliminadas las animaciones y transiciones */
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .grafica h2 {
                font-size: 18px;
                color: #555;
                margin-bottom: 15px;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 5px;
                border: none;  /* Eliminado el borde */
            }
            .grafica div {
                width: 100%;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <h1>MARKETING</h1>
        <div class="grid-container">
            {% for elem in elementos %}
                <div class="grafica">
                    <h2>{{ elem.titulo }}</h2>
                    {% if elem.tipo == 'imagen' %}
                        <img src="data:image/png;base64,{{ elem.contenido }}">
                    {% elif elem.tipo == 'plotly' %}
                        <div>{{ elem.contenido | safe }}</div>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''

    return render_template_string(html, elementos=elementos)

if __name__ == '__main__':
    app.run(debug=True)
