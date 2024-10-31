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

1. Usuario (User)
```python
- role (admin/despachador/supervisor)
- datos personales
- permisos
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
