from server import create_app
from routes import auth, companies, companies_admin, users_admin

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
