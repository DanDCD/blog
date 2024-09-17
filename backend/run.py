from src.app import app, create_prod_db, add_routes


if __name__ == '__main__':
    create_prod_db(app)
    add_routes(app)
    app.run(debug=True)
