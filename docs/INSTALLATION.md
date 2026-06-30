# Guía de Instalación - Free My Life

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- 500MB de espacio en disco

## Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/qlelskme-create/free-my-life.git
cd free-my-life
```

### 2. Crear Entorno Virtual

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env con tus valores
nano .env
```

**Valores importantes a configurar:**

```
SECRET_KEY=tu-clave-secreta-muy-larga
ENCRYPTION_KEY=32-caracteres-minimo-para-encripcion
FLASK_ENV=development  # o production
DATABASE_URL=sqlite:///security_system.db
```

### 5. Inicializar Base de Datos

```bash
python
>>> from app import create_app
>>> app = create_app('development')
>>> with app.app_context():
...     from auth import db
...     db.create_all()
>>> exit()
```

### 6. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Instalación en Producción

### Usando Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app('production')
```

### Con Nginx

Crear archivo `/etc/nginx/sites-available/free-my-life`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Activar la configuración:

```bash
sudo ln -s /etc/nginx/sites-available/free-my-life /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Uso Básico

1. **Registrarse**: Ve a `/register` y crea una nueva cuenta
2. **Iniciar Sesión**: Usa tus credenciales en `/login`
3. **Dashboard**: Accede al panel de control
4. **Configurar 2FA**: Ve a Configuración y habilita autenticación de dos factores
5. **Usar Encriptación**: Encripta tus datos sensibles
6. **Monitorear Firewall**: Supervisa tu actividad de red

## Solución de Problemas

### Error: "No module named 'flask'"

```bash
pip install -r requirements.txt
```

### Error: "Database locked"

```bash
# Eliminar base de datos y recrear
rm security_system.db
python app.py
```

### Puerto 5000 ya está en uso

```bash
# Cambiar puerto
python app.py --port 5001
```

## Obtener Ayuda

- Consulta la [Documentación](README.md)
- Abre un [Issue](https://github.com/qlelskme-create/free-my-life/issues)
- Lee la [Guía de Usuario](USER_GUIDE.md)
