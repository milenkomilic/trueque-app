# TruequeApp

**TruequeApp** es una aplicación web diseñada para facilitar el intercambio de bienes y servicios entre usuarios de manera eficiente, promoviendo la sostenibilidad y la economía circular. Inspirada en la simplicidad de aplicaciones como Tinder, esta plataforma permite a los usuarios realizar trueques locales, conectar con su comunidad y reducir el desperdicio a través de una interfaz intuitiva y funcional.

## Instalación

### Requisitos Previos
- Python 3.x
- SQL Server instalado y configurado
- Git

### Pasos
1. **Clonar el repositorio**:
```bash
   git clone https://github.com/milenkomilic/trueque-app.git
   cd trueque-app
```

2. **Crear un entorno virtual**:
```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
   pip install -r requirements.txt
```

4. **Configurar la base de datos**:
- Crea una base de datos en SQL Server llamada django_sqlserver.
- Usa las credenciales: user: sa, password: 123456.
- Actualiza el archivo de configuración de Django (settings.py) con los detalles de tu base de datos.

5. **Ejecutar migraciones**:
```bash
   python manage.py makemigrations
   python manage.py migrate
```

6. **Iniciar el servidor**:
```bash
   python manage.py runserver
```
- Accede a la aplicación en: http://127.0.0.1:8000/trueque/

### Usabilidad
- Registro: Crea una cuenta y confirma tu email.
- Inicio de sesión: Usa tu nombre de usuario o email y contraseña.
- Recuperar contraseña: Solicitar recuperación via email.
- Publicar un ítem: Sube un bien o servicio que deseas intercambiar.
- Explorar el mercado: Busca ítems disponibles y haz una oferta.
- Chat: Coordina el trueque con otros usuarios a través del sistema de mensajería.
- Finalizar trueque: Acepta o rechaza ofertas para completar el intercambio.

### Objetivos
- Simplicidad en el intercambio: Proporcionar una experiencia fluida y accesible para realizar trueques.
- Sostenibilidad: Promover la reducción de residuos y la economía circular mediante el intercambio de bienes.
- Conexión comunitaria: Crear un espacio digital que fortalezca los lazos entre usuarios locales.

### Características Principales
- Sistema de autenticación: Registro, inicio de sesión, recuperación de contraseña y confirmación de email.
- Perfiles de usuario: Personalización y edición de datos personales.
- Gestión de trueques: Creación de anuncios, envío y cancelación de ofertas, y comunicación directa vía chat.
- Mercado de ítems: Visualización de ofertas disponibles (excluyendo las propias).
- Notificaciones: Alertas en tiempo real sobre trueques iniciados o respondidos.
- Seguridad: Bloqueo de inicio de sesión tras intentos fallidos y recuperación segura de contraseñas.

### Tecnologías Utilizadas
- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript, Bootstrap 4.1
- Base de datos: SQL Server
- Herramientas de desarrollo: Azure DevOps, GitHub
- Documentación: BPMN, Lucidchart

### Estructura del proyecto
```bash
   trueque-app/
   ├── truequeapp/           # Aplicación principal de Django
   │   ├── migrations/       # Migraciones de la base de datos
   │   ├── models.py         # Modelos (CustomUser, Item, Trade, ChatMessage)
   │   ├── forms.py          # Formularios personalizados
   │   ├── views.py          # Lógica de las vistas
   │   └── templates/        # Plantillas HTML
   ├── manage.py             # Script de gestión de Django
   ├── requirements.txt      # Dependencias del proyecto
   └── README.md             # Este archivo
```
