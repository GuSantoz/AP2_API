from app import create_app, db

app = create_app()

# Cria o banco automaticamente na primeira execução
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
