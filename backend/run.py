from src.app import app, create_local_db, add_routes


if __name__ == '__main__':
    create_local_db(app)
    add_routes(app)
    app.run(debug=True)
