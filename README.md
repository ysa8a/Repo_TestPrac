
# Company Management App

**Company Management App** is a web platform that allows users to manage companies and post comments about them. The application supports three roles (`admin`, `owner`, and `user`) with different permissions and access levels.

This system simulates a realistic business environment and includes features such as user authentication, role-based access control, and dynamic forms. It uses Bootstrap for a responsive interface and intentionally includes common security vulnerabilities for educational purposes.

---

## 🚀 Features

- User authentication with role-based access
- Company listing, creation, editing, and viewing
- Commenting system
- Admin dashboard for user and company management
- Toast notifications and dynamic form behavior

---


## 🔍 1. Modelado de Amenazas (Resumen STRIDE)

El análisis STRIDE identificó vulnerabilidades clave como inyección SQL, XSS y control de sesiones. Todas fueron corregidas excepto la falta de una página genérica para errores 500.

> Consulta la tabla completa en el informe final o sección 3.


## ⚙️ 2. Justificación de Herramientas

| Herramienta       | Uso principal                                                             |
|-------------------|---------------------------------------------------------------------------|
| **Flask**         | Backend ligero, modular y extensible con Blueprints                      |
| **Veracode**      | Análisis SAST/SCA en el pipeline para detección de vulnerabilidades      |
| **GitHub Actions**| Automatización del análisis y despliegue                                |
| **Render**        | Entorno de despliegue seguro y accesible públicamente con HTTPS          |
| **Flask-WTF**     | Protección CSRF y validación segura de formularios                      |
| **dotenv**        | Gestión segura de credenciales y configuraciones                        |

---
## 🧪 3. Hallazgos de Seguridad

| CWE     | Descripción                                      | Estado     |
|---------|--------------------------------------------------|------------|
| CWE-89  | Inyección SQL en formularios                    | ✅ Corregido|
| CWE-352 | Falta de CSRF en formularios críticos           | ✅ Corregido|
| CWE-614 | Cookies inseguras en sesión                     | ✅ Corregido|
| CWE-200 | Falta de manejo de errores 500 personalizado    | ❌ No corregido|

> Ver tabla completa de 27 hallazgos en la documentación final.

## 🧱 4. Arquitectura del Proyecto

![Arquitectura](./docs/devsecops_architecture.png)

- Frontend: HTML con Bootstrap 5
- Backend: Flask + Blueprints
- BD: PostgreSQL (Render)
- CI/CD: GitHub Actions + Veracode + Deploy automático

---

## 💬 5. Reflexión Final del Equipo

> “DevSecOps permitió integrar seguridad desde el diseño hasta el despliegue. Aprendimos a automatizar el análisis, aplicar controles desde el código y entender la importancia de un entorno productivo real como Render. Seguridad, desarrollo y operaciones deben ir de la mano desde el principio.”

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-org/company-management-app.git
cd company-management-app
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python main.py
```

✅ The database will be automatically initialized on the first run.

4. Visit: `http://127.0.0.1:5000`

---

## 📂 Project Structure

```
.
├── main.py                 # Entry point to run the Flask app
├── server.py               # Flask app instance
├── db/
│   └── __init__.py         # Initializes SQLite databases
├── routes/
│   ├── auth.py             # Login/logout routes
│   ├── companies.py        # Routes for company views and comments
│   └── users_admin.py      # Admin-only user management
├── templates/
│   ├── base.html           # Shared HTML layout
│   ├── auth/               # Login page
│   ├── companies/          # Pages for listing and managing companies
│   └── admin/              # Admin dashboard templates
├── static/
│   └── css/style.css       # Custom styles
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── LICENSE                 # License file
```

---

## 🌐 Application Routes

| Route                    | Description                             | Access Level           |
|--------------------------|-----------------------------------------|------------------------|
| `/`                      | Redirects to login page                 | Public                 |
| `/login`                 | User login                              | Public                 |
| `/logout`                | Logout current session                  | Logged-in users        |
| `/admin/users`           | User management panel                   | Admin only             |
| `/admin/companies`       | View list of all companies              | Admin only             |
| `/admin/companies/add`   | Add new company                         | Admin only             |
| `/admin/companies/delete`| Delete a company                        | Admin only             |

➡️ Additional routes (such as for owners and company pages) may be dynamically registered or located in other parts of the application depending on role and logic.

---

## 🧪 Default Users

| Username | Password   | Role   | Notes                      |
|----------|------------|--------|----------------------------|
| `alice`  | password1  | user   | Can post comments          |
| `bob`    | password2  | owner  | Owns "Insegura Corp"       |
| `admin`  | admin123   | admin  | Full access                |

---
## 📄 Licencia

Este proyecto se publica con fines educativos bajo licencia MIT.
