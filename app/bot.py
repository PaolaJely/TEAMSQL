from openai import OpenAI
from config import OPENAI_API_KEY
from markupsafe import Markup
from flask import jsonify
from datetime import datetime
from difflib import SequenceMatcher



client = OpenAI(api_key=OPENAI_API_KEY)  # Usa la variable, no el string

from markupsafe import Markup
from datetime import datetime
def texto_similar(a, b, umbral=0.7):
    return SequenceMatcher(None, a, b).ratio() > umbral

def generar_respuesta_html(pregunta, db_cursor, categorias):
    pregunta_lower = pregunta.lower()
    categorias_lower = [c.lower() for c in categorias]
    
    es_consulta_precio = any(x in pregunta_lower for x in ["precio", "coste", "cuesta", "valor"])
    es_consulta_beneficio = any(x in pregunta_lower for x in ["beneficio", "promoción", "oferta", "tendencia", "descuento", "ofertas", "promociones"])
    
    if es_consulta_precio or es_consulta_beneficio:
        db_cursor.execute("SELECT LOWER(nombre) as nombre_lower, nombre as nombre_original, id_producto FROM productos")
        productos_db = db_cursor.fetchall()

        producto_match = next(
            (
                p for p in productos_db
                if any(
                    p['nombre_lower'] in palabra or texto_similar(palabra, p['nombre_lower'])
                    for palabra in pregunta_lower.split()
                )
            ),
            None
        )

        if producto_match:
            nombre_producto = producto_match['nombre_original']
            id_producto = producto_match['id_producto']

            if es_consulta_precio:
                db_cursor.execute("""
                    SELECT precio, marca, categoria 
                    FROM productos 
                    WHERE id_producto = %s
                """, (id_producto,))
                producto = db_cursor.fetchone()

                if producto:
                    return Markup(
                        f"<div class='respuesta-producto'>"
                        f"<h4>{nombre_producto}</h4>"
                        f"<p><strong>Precio:</strong> ${producto['precio']:.2f}</p>"
                        f"<p><strong>Marca:</strong> {producto['marca']}</p>"
                        f"<p><strong>Categoría:</strong> {producto['categoria']}</p>"
                        f"</div>"
                    )

            if es_consulta_beneficio:
                db_cursor.execute("""
                    SELECT 
                        tipo,
                        descuento,
                        fecha_inicio,
                        fecha_final,
                        descripcion
                    FROM beneficios
                    WHERE id_producto = %s
                    AND CURDATE() BETWEEN fecha_inicio AND fecha_final
                    ORDER BY descuento DESC
                """, (id_producto,))
                beneficios = db_cursor.fetchall()

                if beneficios:
                    html = f"""
                    <div class='beneficios-producto'>
                        <h4>Beneficios para {nombre_producto}:</h4>
                        <ul>
                    """
                    for b in beneficios:
                        html += f"""
                        <li>
                            <strong>{b['tipo'].capitalize()} ({b['descuento']}%)</strong><br>
                            <em>Válido:</em> {b['fecha_inicio']} al {b['fecha_final']}<br>
                            {b['descripcion']}
                        </li>
                        """
                    html += "</ul></div>"
                    return Markup(html)
                else:
                    return Markup(
                        f"<p class='aviso'>No hay beneficios activos para <strong>{nombre_producto}</strong>.</p>"
                    )

    if es_consulta_beneficio:
        categoria_encontrada = next(
            (categorias[i] for i, cat_lower in enumerate(categorias_lower) if cat_lower in pregunta_lower),
            None
        )

        if categoria_encontrada:
            db_cursor.execute("""
                SELECT 
                    b.tipo,
                    b.descuento,
                    b.fecha_inicio,
                    b.fecha_final,
                    b.descripcion,
                    p.nombre as producto_nombre,
                    p.id_producto
                FROM beneficios b
                LEFT JOIN productos p ON b.id_producto = p.id_producto
                WHERE (b.categoria = %s OR p.categoria = %s)
                AND CURDATE() BETWEEN b.fecha_inicio AND b.fecha_final
                ORDER BY b.descuento DESC
            """, (categoria_encontrada, categoria_encontrada))
            
            promociones = db_cursor.fetchall()
            
            if promociones:
                grupos = {'tendencia': [], 'oferta': [], 'promocion': []}
                for p in promociones:
                    grupos[p['tipo']].append(p)
                
                html = f"<div class='beneficios-categoria'><h4>Promociones en {categoria_encontrada}</h4>"
                for tipo, items in grupos.items():
                    if items:
                        html += f"<h5>{tipo.capitalize()}s</h5><ul>"
                        for item in items:
                            producto = item['producto_nombre'] or "Varios productos"
                            html += f"""
                            <li>
                                <strong>{item['descuento']}% de descuento</strong><br>
                                <em>Producto:</em> {producto}<br>
                                <em>Válido:</em> {item['fecha_inicio']} al {item['fecha_final']}<br>
                                {item['descripcion']}
                            </li>
                            """
                        html += "</ul>"
                html += "</div>"
                return Markup(html)
            else:
                return Markup(
                    f"<p class='aviso'>No hay promociones activas en la categoría <strong>{categoria_encontrada}</strong>.</p>"
                )

    return None



def generar_respuesta(pregunta):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil para clientes en un marketplace enfocado a beneficios."},
                {"role": "assistant", "content": "Tu nombre es Asistente Team."},
                {"role": "user", "content": pregunta}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar respuesta: {e}"