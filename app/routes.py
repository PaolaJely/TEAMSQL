from flask import Blueprint, render_template, request, redirect, url_for, g
from markupsafe import escape, Markup
from .bot import generar_respuesta, generar_respuesta_html

main_bp = Blueprint('main', __name__, static_folder='static')

@main_bp.route('/', methods=['GET', 'POST'])
def chat():
    respuesta = None
    if request.method == 'POST':
        pregunta = escape(request.form['pregunta'])  # Sanitizar input
        id_cliente = request.form.get('id_cliente', 'CLI0001')
        
        # Primero intenta con generación de HTML para promociones
        respuesta = generar_respuesta_html(
            pregunta=pregunta,
            db_cursor=g.cursor,
            categorias=["Celulares", "Electrodomésticos", "Computación", "Video", "Audio","Electrónica"]  # Tus categorías reales
        )
        
        # Si no es sobre promociones, usa OpenAI
        if respuesta is None:
            respuesta_raw = generar_respuesta(pregunta)
            respuesta = Markup(respuesta_raw.replace('\n', '<br>'))

        # Guardar en DB (usamos respuesta_raw si existe para evitar guardar HTML)
        g.cursor.execute(
            "INSERT INTO mensaje_bot (id_cliente, pregunta, respuesta, creado_el) VALUES (%s, %s, %s, NOW())",
            (id_cliente, pregunta, respuesta_raw if 'respuesta_raw' in locals() else str(respuesta))
        )
        g.db.commit()

    return render_template("chat.html", respuesta=respuesta)
