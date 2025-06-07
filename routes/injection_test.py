# routes/injection_test.py
from flask import request, render_template_string, Blueprint

injection_test = Blueprint('injection_test', __name__)

@injection_test.route('/run', methods=['POST'])
def run_code():
    # VULNERABILIDAD: ejecuta código recibido desde el usuario (Code Injection)
    user_code = request.form.get('code')
    try:
        result = eval(user_code)  # 🧨 PELIGRO: ejecución arbitraria
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error al ejecutar el código: {e}"
