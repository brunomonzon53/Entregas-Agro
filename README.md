# Litros360

Litros360 es una aplicación web desarrollada con Django para administrar clientes y sus cuentas corrientes de combustible. Permite llevar por separado las unidades de negocio FyO y Campo Simple, registrar operaciones y consultar los saldos en litros.

## Funcionalidades

- Inicio de sesión y acceso al panel principal.
- Panel con cantidades de clientes, cuentas y movimientos, saldos por unidad de negocio y últimos movimientos.
- Alta y consulta de clientes, con búsqueda por razón social o CUIT.
- Cuentas corrientes para FyO y Campo Simple.
- Registro de liquidaciones FyO, calculando los litros a partir del importe y el precio por litro.
- Registro de compras de combustible para Campo Simple y de retiros de combustible.
- Historial de movimientos con filtros y búsqueda.
- Administración de clientes, cuentas y movimientos desde Django Admin.
- Asistente de ayuda con respuestas predefinidas por palabras clave; no utiliza un servicio de inteligencia artificial.

## Tecnologías

- Python 3.14
- Django 6.0.10
- SQLite
- HTML, CSS y JavaScript

## Requisitos

- Python 3.14 instalado.
- Git, si se quiere clonar el repositorio o subir los cambios desde la terminal.

## Instalación y ejecución en Windows

Abrí PowerShell en la carpeta del proyecto y ejecutá:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

La aplicación necesita una clave secreta configurada en la variable de entorno `DJANGO_SECRET_KEY`. Para generar una clave local y configurarla en la sesión actual de PowerShell:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_SECRET_KEY = "pegá-acá-la-clave-generada"
```

Luego prepará la base de datos, creá un usuario administrador y ejecutá el servidor:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrí <http://127.0.0.1:8000/> en el navegador e iniciá sesión con el usuario creado. El panel de administración está en <http://127.0.0.1:8000/admin/>.

La clave configurada en PowerShell se conserva solamente en esa ventana. Si abrís otra, volvé a configurarla antes de ejecutar la aplicación.

## Estructura principal

```text
config/                 Configuración y rutas del proyecto Django
gestion/                Modelos, formularios, vistas y rutas de la aplicación
gestion/migrations/     Migraciones de la base de datos
gestion/templates/      Plantillas HTML
manage.py               Comandos de administración de Django
requirements.txt        Dependencias del proyecto
```

## Datos y publicación

La base SQLite (`db.sqlite3`) es local y puede contener información de prueba o datos personales; no se incluye en el repositorio. Al ejecutar `migrate`, Django crea una base nueva. La carpeta `.venv/`, los archivos temporales de Python y los archivos `.env` también están excluidos mediante `.gitignore`.

No publiques claves secretas, contraseñas ni datos reales de clientes. En GitHub, configurá `DJANGO_SECRET_KEY` como variable de entorno para cada entorno. La configuración actual está orientada al desarrollo local (`DEBUG = True`); antes de desplegar la aplicación públicamente también hay que desactivar el modo debug y configurar `ALLOWED_HOSTS`.

## Estado

Proyecto académico en desarrollo.
