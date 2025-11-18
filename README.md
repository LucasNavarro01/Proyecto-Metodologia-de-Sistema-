# Departamento Navarro 

Sitio web para promocionar el departamento Navarro en Malargue. Incluye landing con galeria y tarifas, registro/login de usuarios y una pagina independiente de agradecimiento.

## Tecnologias usadas
- Flask
- Python
- Html

## Requisitos
- Python 3.10+
- pip
- (Opcional) virtualenv

## Configuracion local
1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/LucasNavarro01/Proyecto-Metodologia-de-Sistema-.git

   ```
2. **Crear entorno virtual (opcional)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate           # Windows
   ```
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicializar la base de datos**
   ```bash
   python init_db.py
   ```
   Genera `users.db` con la tabla `users` y el usuario de ejemplo `admin/1234`.
5. **Ejecutar**
   En la terminal colocar
   ```bash
   python init_db.py
   ```
   Navega a `http://127.0.0.1:5000`.

## Rutas principales
- `/` Landing con galeria y tarifas.
- `/register` Registro de usuarios.
- `/login` Inicio de sesion (almacena sesi�n y permite ver productos/carrito).
- `/reserva` Mensaje de ¡Gracias por tu reserva! una vez realizado el.



