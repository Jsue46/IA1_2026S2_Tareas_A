# Archivo Backend (.py) con comentarios técnicos
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de los middlewares de CORS para permitir peticiones externas desde el frontend en el navegador
CORS(app)

# Inicialización del motor de inferencia lógic Prolog (PySwip)
prolog = Prolog()
# Cargar el archivo .pl que contiene los hechos y la lógica
prolog.consult("inventario.pl")

# Creación de una API REST que exponga un endpoint GET
@app.route('/buscar', methods=['GET'])
def buscar_item():
    """
    Endpoint principal para buscar un ítem en el inventario.
    Se inyecta el parámetro ingresado al motor de Prolog y se 
    capturan y serializan las respuestas unificadas.
    """
    # Obtener el parámetro ingresado mediante query parameters (ej. ?item=espada)
    item_buscado = request.args.get('item', '')
    
    if not item_buscado:
        return jsonify({"error": "Debe ingresar un ítem a buscar."}), 400

    # Configuración de PySwip para ejecutar la consulta principal
    # Inyectamos el parámetro ingresado directamente a la regla procesar_inventario/5
    query_str = f"procesar_inventario({item_buscado}, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado)"
    
    try:
        # Ejecuta la consulta dinámicamente y captura los resultados
        # pyswip devuelve un generador, usamos list() para evaluarlo
        resultados = list(prolog.query(query_str))
        
        if resultados:
            # Dado que el member/2 puede arrojar varios resultados idénticos si hay duplicados,
            # capturamos solo la primera respuesta unificada que nos da el generador
            primer_resultado = resultados[0]
            
            # Capturamos las variables unificadas que devuelve Prolog y las formateamos en un diccionario
            # Nota: pySwip devuelve Atoms de prolog como objetos, los parseamos a strings
            respuesta_json = {
                "TotalItems": primer_resultado["TotalItems"],
                "InventarioInvertido": [str(item) for item in primer_resultado["InventarioInvertido"]],
                "InventarioUnico": [str(item) for item in primer_resultado["InventarioUnico"]],
                "InventarioOrdenado": [str(item) for item in primer_resultado["InventarioOrdenado"]]
            }
            # Serializa la respuesta en un JSON mediante jsonify()
            return jsonify(respuesta_json), 200
        else:
            # Si 'resultados' está vacío, significa que member/2 falló porque el ítem no se encontró
            return jsonify({"error": "Ítem no encontrado en el inventario."}), 404
            
    except Exception as e:
        # Captura errores en la ejecución de la consulta
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Iniciar servidor en el puerto 5000 sin lanzar ningún Syntax Error
    print("Backend de Inventario iniciado correctamente...")
    app.run(debug=True, port=5000)
