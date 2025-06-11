print("==> Iniciando debug.py")

try:
    from app import create_app
    print("==> Se importó create_app()")
    app = create_app()
    print("==> Se ejecutó create_app()")
except Exception as e:
    print("❌ Error en imports o create_app():", e)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    print(f"==> Ejecutando app en puerto {port}")
    app.run(host="0.0.0.0", port=port)
