# Quiz App — Lab 08: API REST con Django REST Framework

API REST construida sobre el proyecto de cuestionarios del Lab 03 (modelos Exam, Question, Choice con validación de exactamente una opción correcta).

**Autor:** Alexander Faustino

## ¿Qué hace esta API?

Expone los tres recursos principales como endpoints REST:

| Recurso | Endpoint | Descripción |
|---------|----------|-------------|
| Exams | `/api/exams/` | CRUD de exámenes con preguntas anidadas en el detalle |
| Questions | `/api/questions/` | CRUD de preguntas con choices anidadas y escribibles |
| Choices | `/api/choices/` | CRUD independiente de opciones |

Características:
- Paginación de 5 elementos por página
- Filtrado (`?exam=`, `?question=`, `?is_correct=`)
- Búsqueda (`?search=` en `statement` y `title`)
- Validación de negocio: mínimo 2 choices, exactamente 1 correcta
- Permiso `AllowAny` (solo desarrollo)

## Cómo ejecutarlo

```powershell
cd Lab08-DAE

# 1. Copiar variables de entorno
copy .env.example .env

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
venv\Scripts\python -m pip install -r requirements.txt

# 4. Migrar base de datos
cd src
..\venv\Scripts\python manage.py migrate

# 5. Cargar datos de prueba (idempotente)
..\venv\Scripts\python manage.py seed_quiz

# 6. Levantar servidor
..\venv\Scripts\python manage.py runserver
```

Abrir `http://127.0.0.1:8000/api/` en el navegador o usar el cliente REST.

## Direcciones principales

| Recurso | URL |
|---------|-----|
| API raíz (browsable) | `http://127.0.0.1:8000/api/` |
| Exams | `http://127.0.0.1:8000/api/exams/` |
| Questions | `http://127.0.0.1:8000/api/questions/` |
| Choices | `http://127.0.0.1:8000/api/choices/` |
| Admin Django | `http://127.0.0.1:8000/admin/` |
| App HTML (Lab 03) | `http://127.0.0.1:8000/quiz/` |

## Documentación

- **Tabla completa de la API:** [`docs/API.md`](docs/API.md)
- **Colección REST Client (`.http`):** [`docs/api.http`](docs/api.http) — lista, detalle, crear, actualizar, borrar, filtros, búsqueda, paginación y casos de error

## Estructura del proyecto (resumen)

```
Lab08-DAE/
├── .opencode/agent/           # Agentes de OpenCode
├── docs/
│   ├── API.md                 # Documentación de la API (este archivo)
│   └── api.http               # Peticiones para REST Client (VS Code)
├── src/
│   ├── manage.py
│   ├── config/config/
│   │   ├── settings.py        # REST_FRAMEWORK, INSTALLED_APPS
│   │   └── urls.py            # /api/ → quiz.api_urls
│   └── quiz/
│       ├── models.py          # Exam, Question, Choice (Lab 03)
│       ├── serializers.py     # ModelSerializers con choices anidadas
│       ├── api_views.py       # ModelViewSets + filtros/búsqueda
│       ├── api_urls.py        # DefaultRouter
│       ├── management/commands/seed_quiz.py  # Datos de prueba
│       ├── tests.py           # Tests de serializers (paso 4)
│       ├── views.py           # Vistas HTML (Lab 03, intactas)
│       └── urls.py            # Rutas HTML (Lab 03, intactas)
├── .env / .env.example
├── requirements.txt           # UTF-8, con DRF y django-filter
└── .gitignore
```

## Datos de prueba (seed_quiz)

Ejecuta `..\venv\Scripts\python manage.py seed_quiz` desde `src/` para cargar:

- **2 exámenes:** "Python Basics" (7 preguntas) y "Django ORM" (5 preguntas)
- **12 preguntas** con score 1–3
- **36 opciones** (3 por pregunta, exactamente 1 correcta)
- **4 preguntas** contienen "list" en el enunciado (para probar `?search=list`)

El comando es idempotente: borra datos previos y vuelve a crearlos.