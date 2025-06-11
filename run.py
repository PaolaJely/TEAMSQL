from app import app  # Importa tu aplicación Flask desde la carpeta app

if __name__ == "__main__":
    # Esto SOLO se ejecutará si inicias con python run.py (LOCAL)
    app.run(host='0.0.0.0', port=5000)
