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

**Nota:** No es necesario instalar Python ni PostgreSQL en tu máquina local. Docker se encargará de proporcionar ambos en contenedores aislados.

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
