import os
try:
    from app import create_app
except Exception as e:
    print("ERROR IMPORTANDO create_app():", e)

try:
    app = create_app()
except Exception as e:
    print("ERROR EJECUTANDO create_app():", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
