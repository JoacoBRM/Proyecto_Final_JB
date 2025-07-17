# Sistema de Rutas con Grafos

Un sistema web desarrollado en Flask para calcular rutas óptimas entre ciudades utilizando el algoritmo de Dijkstra.

## 📋 Descripción

Este proyecto implementa una aplicación web que permite a los usuarios calcular las rutas más cortas entre diferentes ciudades. Utiliza teoría de grafos y el algoritmo de Dijkstra para encontrar el camino óptimo, proporcionando una interfaz web intuitiva para la gestión de rutas.

## 🚀 Características

- ✅ Cálculo de rutas óptimas usando algoritmo de Dijkstra
- ✅ Sistema de autenticación de usuarios
- ✅ Interfaz web responsiva
- ✅ Gestión de ciudades y conexiones
- ✅ Base de datos SQLAlchemy
- ✅ Arquitectura modular con blueprints

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask (Python)
- **Base de Datos:** SQLAlchemy
- **Autenticación:** Flask-Login
- **Frontend:** HTML, CSS, JavaScript
- **Algoritmos:** Dijkstra para rutas óptimas

## 📁 Estructura del Proyecto

```
Proyecto_Final_JB/
├── docs/                   # Documentación del proyecto
│   ├── manual-usuario.pdf
│   ├── manual-tecnico.pdf
│   └── diagramas/
├── src/                    # Código fuente
│   ├── app.py             # Aplicación principal
│   ├── config.py          # Configuración
│   ├── extensions.py      # Extensiones Flask
│   ├── models/            # Modelos de base de datos
│   ├── routes/            # Rutas y controladores
│   └── templates/         # Plantillas HTML
└── README.md              # Este archivo
```

## ⚙️ Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/Proyecto_Final_JB.git
   cd Proyecto_Final_JB
   ```
2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```
3. **Instalar dependencias**

   ```bash
   pip install flask flask-sqlalchemy flask-login
   ```
4. **Configurar la base de datos**

   ```bash
   cd src
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

## 🎮 Uso

1. **Ejecutar la aplicación**

   ```bash
   cd src
   python app.py
   ```
2. **Acceder a la aplicación**

   - Abrir navegador en: `http://localhost:4000`
   - Registrarse o iniciar sesión
   - Comenzar a calcular rutas

## 👤 Autor

**Joaquín Bermeo**

- Proyecto Final - Programación IV
- PUCESA - Cuarto Semestre
- Julio 2025

## 📚 Documentación

Para más información detallada, consultar:

- `docs/manual-usuario.pdf` - Guía de uso de la aplicación
- `docs/manual-tecnico.pdf` - Documentación técnica completa

## 📄 Licencia

Este proyecto es desarrollado con fines académicos para la materia de Programación IV.

---

💡 **Nota:** Este sistema utiliza el algoritmo de Dijkstra para garantizar que las rutas calculadas sean siempre las más cortas posibles entre los puntos seleccionados.
