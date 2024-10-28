# 🚚 Proyecto Sistema Web de Despacho

Este proyecto consta de un backend desarrollado con Django y un frontend desarrollado con Next.js.

---

## 🛠️ Backend

Este es un proyecto de backend desarrollado con Django, utilizando Docker para la infraestructura y PostgreSQL como base de datos.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- [Docker](https://www.docker.com/products/docker-desktop)

También necesitarás:

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
```

Esto aplicará todas las migraciones de Django a la base de datos.

## 🔐 Creación de un Superusuario (Opcional)

Para acceder a la interfaz de administración de Django, puedes crear un superusuario con:

```
docker-compose exec web python manage.py createsuperuser
```

Sigue las instrucciones en la terminal para crear el usuario.

## 🌐 Acceso a la Aplicación

- La aplicación estará disponible en: http://localhost:8000
- La interfaz de administración de Django: http://localhost:8000/admin

## 🐋 Comandos Útiles de Docker

- Para detener los contenedores:
  ```
  docker-compose down
  ```

- Para inicializar el contenedor sin construir:
  ```
  docker-compose up
  ```

- Para ver los logs en tiempo real:
  ```
  docker-compose logs -f
  ```

## ⚙️ Notas Adicionales

- Asegúrate de que los puertos 8000 y 5432 estén disponibles en tu máquina.
- Si encuentras problemas, verifica que Docker Desktop esté corriendo y que hayas iniciado sesión.
- Para cambios en el código, puede ser necesario reconstruir los contenedores con `docker-compose up --build`.

## 🖥️ Frontend (Next.js)

### 📋 Requisitos Previos

Asegúrate de tener instalado:

- [Node.js](https://nodejs.org/) (versión 14 o superior)
- [npm](https://www.npmjs.com/) (normalmente viene con Node.js)

### 🔧 Configuración del Frontend

1. Navega a la carpeta del frontend:

   ```
   cd Proyecto-sistema-web-de-despacho/frontend/nextjsdespacho
   ```

2. Instala las dependencias:

   ```
   npm install
   ```

3. Crea un archivo `.env` en la carpeta `nextjsdespacho` con el siguiente contenido:

   ```
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/
   ```

   Esto configura la URL del backend para que el frontend pueda comunicarse con él.

### ▶️ Ejecutar el Frontend

1. Para iniciar el servidor de desarrollo de Next.js, ejecuta:

   ```
   npm run dev
   ```

2. El frontend estará disponible en `http://localhost:3000`

### ⚙️ Construcción para Producción

Si deseas construir la aplicación para producción:

1. Ejecuta el comando de construcción:

   ```
   npm run build
   ```

2. Para iniciar la versión de producción:

   ```
   npm start
   ```

## 🖇️ Ejecutando el Proyecto Completo

Para ejecutar tanto el backend como el frontend:

1. Inicia el backend siguiendo las instrucciones de la sección "Backend".
2. En una nueva terminal, inicia el frontend como se describe en la sección "Frontend".
3. Accede al frontend en `http://localhost:3000` y al backend en `http://localhost:8000`.

## 📌 Notas Adicionales

- Asegúrate de que el backend esté en funcionamiento antes de iniciar el frontend para una correcta comunicación entre ambos.
- Si cambias la configuración del backend, asegúrate de actualizar la variable `NEXT_PUBLIC_BACKEND_URL` en el archivo `.env` del frontend.

## 📁 Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
Proyecto-sistema-web-de-despacho/
├── backend/
│   ├── django_backend/
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   ├── requirements.txt
│   │   └── [otros archivos y carpetas de Django]
│   ├── .env.dev
│   └── docker-compose.yml
├── frontend/
│   └── nextjsdespacho/
│       ├── .env
│       ├── tailwind.config.js
│       └── [otros archivos y carpetas de Next.js]
└── README.md
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
3. Realiza tus cambios y haz commit de ellos (`git commit -m 'Add some AmazingFeature'`).
4. Haz push a la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

Por favor, asegúrate de actualizar las pruebas según corresponda y de seguir las convenciones de código del proyecto.
