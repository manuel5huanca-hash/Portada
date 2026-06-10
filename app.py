from flask import Flask, request, render_template_string

app = Flask(__name__)

USUARIO_CORRECTO = "admin"
PASSWORD_CORRECTO = "1234"

html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I&S Market Mini</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #f0f0f0; font-family: sans-serif; }

  .navbar {
    background: #fff;
    border: 2px solid #2e7d32;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 28px;
    margin: 20px auto;
    max-width: 1300px;
    gap: 16px;
  }

  .navbar-left {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .navbar-logo img {
    height: 52px;
    object-fit: contain;
  }

  .delivery-btn {
    border: 2px solid #2e7d32;
    color: #2e7d32;
    background: #fff;
    border-radius: 24px;
    padding: 8px 20px;
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
  }

  .navbar-right {
    display: flex;
    align-items: center;
    gap: 18px;
  }

  .search-box {
    border: 1.5px solid #ccc;
    border-radius: 24px;
    padding: 8px 18px;
    font-size: 14px;
    width: 220px;
    outline: none;
    color: #888;
  }

  .nav-phone {
    color: #c62828;
    display: flex;
    align-items: center;
    white-space: nowrap;
    text-decoration: none;
  }

  .nav-account {
    color: #333;
    display: flex;
    align-items: center;
    white-space: nowrap;
    cursor: pointer;
    text-decoration: none;
  }

  .promo {
    max-width: 1000px;
    margin: 0 auto 30px;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 6px 30px rgba(0,0,0,.12);
  }

  .promo img {
    width: 100%;
    display: block;
  }

  .overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.45);
    z-index: 100;
    align-items: center;
    justify-content: center;
  }

  .overlay.active {
    display: flex;
  }

  .modal {
    background: #fff;
    border-radius: 20px;
    padding: 40px 36px 32px;
    width: 100%;
    max-width: 400px;
    position: relative;
    box-shadow: 0 20px 60px rgba(0,0,0,.2);
    animation: popIn .25s ease;
  }

  @keyframes popIn {
    from { transform: scale(.9); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
  }

  .modal-close {
    position: absolute;
    top: 14px;
    right: 18px;
    background: none;
    border: none;
    font-size: 22px;
    cursor: pointer;
    color: #999;
  }

  .modal-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 18px;
  }

  .modal-logo img {
    height: 60px;
    object-fit: contain;
  }

  .modal h2 {
    text-align: center;
    font-size: 22px;
    font-weight: 800;
    color: #1b5e20;
    margin-bottom: 6px;
  }

  .modal p {
    text-align: center;
    font-size: 13px;
    color: #888;
    margin-bottom: 24px;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
  }

  .input-group label {
    font-size: 13px;
    font-weight: 700;
    color: #333;
  }

  .input-group input {
    border: 1.5px solid #ddd;
    border-radius: 10px;
    padding: 11px 16px;
    font-size: 14px;
    outline: none;
  }

  .btn-login {
    width: 100%;
    background: #2e7d32;
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 13px;
    font-size: 15px;
    font-weight: 800;
    cursor: pointer;
  }

  .mensaje-error {
    color: #c62828;
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    margin-top: 12px;
  }

  .modal-footer {
    text-align: center;
    margin-top: 16px;
    font-size: 13px;
    color: #888;
  }

  .modal-footer a {
    color: #2e7d32;
    font-weight: 700;
    text-decoration: none;
  }

  .divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 18px 0;
    color: #ccc;
    font-size: 12px;
  }

  .divider::before,
  .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #eee;
  }
</style>
</head>
<body>

<nav class="navbar">
  <div class="navbar-left">
    <div class="navbar-logo">
      <img src="/static/logo.png" alt="logo">
    </div>

    <button class="delivery-btn">
      Delivery: Ingresa tu dirección
    </button>
  </div>

  <div class="navbar-right">
    <input class="search-box" type="text" placeholder="¿Qué deseas pedir?">

    <a href="#" class="nav-phone">
      (01) 613 5000
    </a>

    <a href="#" class="nav-account" onclick="abrirModal()">
      Mi cuenta
    </a>
  </div>
</nav>

<div class="promo">
  <img src="/static/promocion.png" alt="promocion">
</div>

<!--LOGIN -->
<div class="overlay" id="overlay" onclick="cerrarModalFuera(event)">
  <div class="modal" id="modal">

    <button class="modal-close" onclick="cerrarModal()">✕</button>

    <div class="modal-logo">
      <img src="/static/logo.png" alt="logo">
    </div>

    <h2>¡Bienvenido!</h2>
    <p>Inicia sesión para continuar</p>

    <div class="input-group">
      <label>Usuario</label>
      <input type="text" id="usuario" placeholder="Tu usuario">

      <label>Contraseña</label>
      <input type="password" id="password" placeholder="••••••••">
    </div>

    <button class="btn-login" onclick="iniciarSesion()">
      Iniciar sesión
    </button>

    <p class="mensaje-error" id="mensaje" style="display:none;">
      Usuario o contraseña incorrectos
    </p>

    <div class="divider">o</div>

    <div class="modal-footer">
      ¿No tienes cuenta? <a href="#" onclick="mostrarRegistro()">Regístrate aquí</a>
    </div>
  </div>
</div>
<div class="modal" id="registroModal" style="display:none;">

  <button class="modal-close" onclick="volverLogin()">✕</button>

  <div class="modal-logo">
    <img src="/static/logo.png" alt="logo">
  </div>

  <h2>Crear cuenta</h2>
  <p>Regístrate para continuar</p>

  <div class="input-group">

    <label>Correo electrónico</label>
    <input type="email" id="correo" placeholder="correo@ejemplo.com">

    <label>Contraseña</label>
    <input type="password" id="passwordRegistro" placeholder="••••••••">

  </div>

  <button class="btn-login" onclick="registrarse()">
    Registrarse
  </button>

  <div class="modal-footer">
      <a href="#" onclick="volverLogin()">Volver al login</a>
  </div>

</div>
<script>
  function abrirModal() {
    document.getElementById('overlay').classList.add('active');
  }

  function cerrarModal() {
    document.getElementById('overlay').classList.remove('active');
    document.getElementById('mensaje').style.display = 'none';
  }

  function cerrarModalFuera(e) {
    if (e.target === document.getElementById('overlay')) {
      cerrarModal();
    }
  }

  function iniciarSesion() {
    var usuario = document.getElementById('usuario').value;
    var password = document.getElementById('password').value;

    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body:
        'usuario=' + encodeURIComponent(usuario) +
        '&password=' + encodeURIComponent(password)
    })
    .then(function(r) {
      return r.json();
    })
    .then(function(data) {
      if (data.ok) {
        window.location.href = '/bienvenida';
      } else {
        document.getElementById('mensaje').style.display = 'block';
      }
    });
  }
  function mostrarRegistro() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('registroModal').style.display = 'block';
}

function volverLogin() {
    document.getElementById('registroModal').style.display = 'none';
    document.getElementById('modal').style.display = 'block';
}

function registrarse() {

    var correo = document.getElementById('correo').value;
    var password = document.getElementById('passwordRegistro').value;

    if(correo === "" || password === ""){
        alert("Completa todos los campos");
        return;
    }

    fetch('/guardar_registro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body:
            'correo=' + encodeURIComponent(correo) +
            '&password=' + encodeURIComponent(password)
    })
    .then(function(response){
        return response.text();
    })
    .then(function(data){
        alert("Registro exitoso");
        volverLogin();
    });
}
</script>

</body>
</html>
"""

bienvenida_html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Bienvenido</title>

<style>
  body {
    background: #f0f0f0;
    font-family: sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    flex-direction: column;
    gap: 16px;
  }

  h1 {
    color: #1b5e20;
    font-size: 32px;
  }

  a {
    color: #2e7d32;
    font-weight: 700;
  }
</style>
</head>

<body>
  <h1>Autenticación Exitosa</h1>
  <h2>Bienvenido a I&S Market Mini</h2>

  <a href="/">Volver al inicio</a>
</body>
</html>
"""

@app.route("/registro")
def registro():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Registro</title>
    <style>
        body{
            background:#f0f0f0;
            font-family:sans-serif;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }

        .card{
            background:#fff;
            width:380px;
            padding:35px;
            border-radius:20px;
            box-shadow:0 10px 30px rgba(0,0,0,.15);
        }

        h2{
            text-align:center;
            color:#1b5e20;
            margin-bottom:10px;
        }

        p{
            text-align:center;
            color:#777;
            margin-bottom:20px;
        }

        input{
            width:100%;
            padding:12px;
            border:1px solid #ddd;
            border-radius:10px;
            margin-bottom:15px;
        }

        button{
            width:100%;
            background:#2e7d32;
            color:white;
            border:none;
            padding:12px;
            border-radius:10px;
            font-weight:bold;
            cursor:pointer;
        }

        a{
            color:#2e7d32;
            text-decoration:none;
        }

        .footer{
            text-align:center;
            margin-top:15px;
        }
    </style>
    </head>

    <body>

    <div class="card">
        <h2>Crear cuenta</h2>
        <p>Regístrate para continuar</p>

        <form action="/guardar_registro" method="POST">

            <input
                type="email"
                name="correo"
                placeholder="Correo electrónico"
                required>

            <input
                type="password"
                name="password"
                placeholder="Contraseña"
                required>

            <button type="submit">
                Registrarse
            </button>

        </form>

        <div class="footer">
            <a href="/">Volver al inicio</a>
        </div>

    </div>

    </body>
    </html>
    """

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]

    if usuario == USUARIO_CORRECTO and password == PASSWORD_CORRECTO:
        return {"ok": True}
    else:
        return {"ok": False}
    
@app.route("/guardar_registro", methods=["POST"])
def guardar_registro():
    correo = request.form["correo"]
    password = request.form["password"]

    print("Nuevo usuario registrado:", correo)

    return "ok"

@app.route("/bienvenida")
def bienvenida():
    return render_template_string(bienvenida_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
