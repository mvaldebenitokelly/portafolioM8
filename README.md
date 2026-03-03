# CosmoStore — Proyecto Módulo 8 (Django + PostgreSQL)

Este proyecto implementa un Ecommerce académico con:

- Catálogo (Category/Product) con **CRUD administrativo**
- Carrito por sesión
- Órdenes persistentes (Order/OrderItem)
- **Imágenes de productos** (MEDIA uploads)
- **Formulario de contacto** (persistente en BD)
- Autenticación (accounts/login/logout) y protección por rol (admin/staff)

## Requisitos

- Python 3.x
- PostgreSQL 14+
- Pillow
- (Windows) PowerShell recomendado

## 1) Preparación (venv)

En la carpeta del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

> Nota: `requirements.txt` incluye Pillow para soporte de imágenes.

## 2) Variables de entorno (.env)

El proyecto usa `.env` para credenciales y settings sensibles.
Si no existe, copia `.env.example` a `.env` y ajusta:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `SECRET_KEY`
- `DEBUG`

## 3) Base de datos

Puedes crear la DB/usuario con el script:

- `scripts/db_setup.sql`

Luego ejecuta migraciones:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 4) Usuario administrador

```powershell
python manage.py createsuperuser
```

## 5) Ejecutar

```powershell
python manage.py runserver
```

Rutas principales:

- Home: `http://127.0.0.1:8000/`
- Contacto: `http://127.0.0.1:8000/contact/`
- Admin: `http://127.0.0.1:8000/admin/`
- Productos (CRUD Admin): `http://127.0.0.1:8000/products/`
- Carrito: `http://127.0.0.1:8000/cart/`

## 6) Imágenes de productos

- En el CRUD o en Admin puedes subir la imagen del producto.
- Se guarda en `media/products/`.
- En desarrollo (DEBUG=True) Django sirve `MEDIA_URL` automáticamente.

## 7) Mensajes de contacto

- El formulario de contacto guarda mensajes en la tabla `ContactMessage`.
- Puedes revisarlos en Django Admin: `ContactMessage`.

## Importante (GitHub)

- **No** subas `venv/`
- **No** subas `.env`
- **No** subas `media/` (uploads)
