from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import crud_usuarios

# Configurado para buscar el HTML en la raíz y el JS en la carpeta static
app = Flask(__name__, template_folder='.', static_folder='static')
app.secret_key = 'secreto_84_parcial2'

@app.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        datos = request.get_json()
        if crud_usuarios.gestionar_login(datos.get('usuario'), datos.get('clave')):
            session['activo'] = datos.get('usuario')
            return jsonify({"status": "success", "url": "/admin"})
        return jsonify({"status": "fail", "msj": "Credenciales inválidas"}), 401
    return render_template('índice.html', page='login')

@app.route('/admin')
def panel_admin():
    if 'activo' not in session:
        return redirect(url_for('inicio_sesion'))
    return render_template('índice.html', page='panel')

@app.route('/api/add', methods=['POST'])
def api_add():
    if 'activo' not in session: return jsonify({"msj": "Denegado"}), 403
    return jsonify(crud_usuarios.gestionar_insertar(request.get_json()))

@app.route('/api/get', methods=['GET'])
def api_get():
    if 'activo' not in session: return jsonify({"msj": "Denegado"}), 403
    return jsonify(crud_usuarios.gestionar_buscar(request.args.get('q', '')))

@app.route('/api/update/<int:id>', methods=['PUT'])
def api_update(id):
    if 'activo' not in session: return jsonify({"msj": "Denegado"}), 403
    return jsonify(crud_usuarios.gestionar_actualizar(id, request.get_json()))

@app.route('/api/del/<int:id>', methods=['DELETE'])
def api_del(id):
    if 'activo' not in session: return jsonify({"msj": "Denegado"}), 403
    return jsonify(crud_usuarios.gestionar_eliminar(id))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio_sesion'))

if __name__ == '__main__':
    app.run(debug=True)