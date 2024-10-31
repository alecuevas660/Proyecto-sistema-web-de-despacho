# 🚚 Sistema de Despacho de Productos Caimán

Sistema web desarrollado con Django para la gestión y despacho de productos a supermercados, optimizando el proceso de distribución desde el almacén central hasta los puntos de venta.

## 📋 Requisitos del Sistema

### Gestión de Inventario y Almacén
- Control de stock en almacén central
- Registro y actualización de productos
- Gestión de ubicaciones en almacén
- Alertas de stock bajo
- Trazabilidad de productos

### Gestión de Despachos
- Generación de órdenes de despacho
- Asignación de rutas de entrega
- Seguimiento en tiempo real
- Control de estados de envío
- Confirmación de entregas

### Gestión de Supermercados
- Registro de supermercados
- Puntos de entrega
- Horarios de recepción
- Contactos autorizados
- Historial de pedidos

## 🛠️ Tecnologías Utilizadas

- Django 5.1.2
- Bootstrap 5.3
- SQLite
- Python-decouple
- Font Awesome

## 💻 Estructura de Base de Datos

### Modelos Principales:

<<<<<<< HEAD
1. Usuario (User)
```python
- role (admin/despachador/supervisor)
- datos personales
- permisos
=======
1. Una cuenta de Docker (puedes crearla en [Docker Hub](https://hub.docker.com/))
2. Iniciar sesión en Docker Desktop
3. Clonar este repositorio en tu máquina local

**Nota:** Es necesario instalar postgres antes de instalar y configurar Docker.

--##Paso a paso para instalar docker.

## Windows

1. **Descargar el instalador:**
   - Visita [PostgreSQL Windows Installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
   - Selecciona la última versión estable para Windows
   - Elige la versión de 64 bits

2. **Ejecutar el instalador:**
   - Ejecuta el archivo .exe descargado
   - Sigue el asistente de instalación
   - Selecciona los componentes a instalar (mantén todos por defecto):
     - PostgreSQL Server
     - pgAdmin 4
     - Stack Builder
     - Command Line Tools

3. **Configuración durante la instalación:**
   - Elige el directorio de instalación (por defecto: C:\Program Files\PostgreSQL\[version])
   - Establece una contraseña para el usuario postgres
   - Selecciona el puerto (por defecto: 5432)
   - Selecciona la configuración regional

4. **Verificar la instalación:**
   - Busca "pgAdmin 4" en el menú inicio
   - O abre SQL Shell (psql)

5. **Agregar PostgreSQL al PATH (opcional):**
   - Panel de Control > Sistema > Configuración avanzada del sistema
   - Variables de entorno > Path
   - Agregar: C:\Program Files\PostgreSQL\[version]\bin

### macOS:

   #### Usando Homebrew (recomendado)
   1. **Instalar Homebrew si no está instalado:**
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```

   2. **Instalar PostgreSQL:**
      ```bash
      brew install postgresql
      ```

   3. **Iniciar el servicio:**
      ```bash
      brew services start postgresql
      ```

### Linux (Ubuntu):

      1. **Actualizar el sistema:**
         ```bash
         sudo apt update
         sudo apt upgrade
         ```

      2. **Instalar PostgreSQL:**
         ```bash
         sudo apt install postgresql postgresql-contrib
         ```

      3. **Verificar la instalación:**
         ```bash
         sudo systemctl status postgresql
         ```

      4. **Iniciar el servicio:**
         ```bash
         sudo systemctl start postgresql
         sudo systemctl enable postgresql
         ```

         ### Verificación de la instalación:

         1. **Verificar versión de PostgreSQL:**
            ```bash
            psql --version
            ```

         2. **Conectar a PostgreSQL:**
            ```bash
            psql -U postgres
            ```

         ### Comandos útiles de PostgreSQL:

         ```sql
         -- Listar bases de datos
         \l

         -- Conectar a una base de datos
         \c nombre_base_datos

         -- Listar tablas
         \dt

         -- Salir
         \q
         ```

         ### Notas importantes:

         1. **Windows**:
            - Guarda la contraseña que estableces durante la instalación
            - Considera agregar PostgreSQL al PATH del sistema

         2. **macOS**:
            - Si usas Homebrew, el servicio se puede iniciar automáticamente al arranque
            - La contraseña inicial puede variar según el método de instalación

         3. **Linux**:
            - El usuario postgres se crea automáticamente
            - Puede ser necesario configurar la autenticación en pg_hba.conf

         4. **Seguridad**:
            - Cambia la contraseña del usuario postgres
            - Configura adecuadamente los permisos de acceso
            - Realiza copias de seguridad regularmente
---

## 🔧 Configuración de Variables de Entorno

1. Navega a la carpeta del backend:

   ```
   cd Proyecto-sistema-web-de-despacho/backend
   ```

2. Crea un archivo `.env.dev` con el siguiente contenido:

   ```
   DEBUG=1
   SECRET_KEY=clavesecreta
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=djangobackend
   SQL_USER=postgresuser
   SQL_PASSWORD=postgrespassword
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   ```

   **Importante:** Estas son las credenciales que se usarán para acceder a la base de datos PostgreSQL en el contenedor Docker. No es necesario que coincidan con ninguna instalación local de PostgreSQL.

## ▶️ Ejecutar el Proyecto con Docker

1. Desde la carpeta del backend, ejecuta el siguiente comando para construir y levantar el proyecto:

   ```
   docker-compose up --build
   ```

   Este proceso puede tardar unos minutos la primera vez que se ejecuta.

2. Una vez que veas mensajes indicando que el servidor está corriendo, el proyecto estará listo para usar.

## 📂 Migraciones de Base de Datos

Después de que los contenedores estén corriendo, abre una nueva terminal y ejecuta:

```
docker-compose exec web python manage.py migrate
>>>>>>> 8d3b3d20315f866485f05a85632cd4c98ef7c1b3
```

2. Producto (Producto)
```python
- código
- nombre
- descripción
- stock
- categoría
```

3. Despacho (Despacho)
```python
- número de orden
- fecha_creación
- estado
- supermercado_destino
- productos
```

4. Supermercado (Supermercado)
```python
- nombre
- dirección
- contacto
- horarios_recepción
```

## 📁 Estructura del Proyecto

```
DespachoDjango/
├── apps/
│   ├── users/          # Gestión de usuarios
│   ├── inventario/     # Control de productos
│   └── despachos/      # Gestión de envíos
├── core/               # Configuración del proyecto
├── static/            
│   ├── css/
│   ├── js/
│   └── img/
├── templates/        
│   ├── base.html
│   ├── despachos/
│   └── inventario/
├── media/           
├── requirements/    
├── manage.py
└── .env
```

## 🚀 Funcionalidades Principales

### Módulo de Despacho
- Creación de órdenes de despacho
- Asignación de rutas
- Seguimiento de envíos
- Confirmación de entregas
- Reportes de despacho

### Módulo de Inventario
- Control de stock
- Registro de movimientos
- Alertas de inventario
- Gestión de productos
- Ubicaciones en almacén

### Módulo de Supermercados
- Gestión de clientes
- Puntos de entrega
- Horarios de recepción
- Historial de pedidos
- Contactos autorizados

## 📊 Reportes y Estadísticas

- Dashboard de despachos diarios
- Eficiencia de entregas
- Niveles de inventario
- Rendimiento por ruta
- Estadísticas por supermercado

## 🔐 Seguridad

- Autenticación por roles
- Registro de actividades
- Validación de datos
- Protección CSRF
- Backups automáticos

## 👥 Roles del Sistema

1. Administrador
   - Gestión completa del sistema
   - Reportes y estadísticas
   - Configuración general

2. Despachador
   - Creación de órdenes
   - Seguimiento de envíos
   - Confirmación de entregas

3. Supervisor
   - Control de inventario
   - Aprobación de despachos
   - Gestión de rutas

## 🔧 Instalación y Configuración

1. Clonar el repositorio:
```bash
git clone <url-repositorio>
cd DespachoDjango
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements/base.txt
```

4. Configurar .env:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Migraciones:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## ⚙️ Desarrollo

```bash
python manage.py runserver
```

Accesos:
- Sistema: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin
