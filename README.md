# Lab 08 — API REST de cuestionarios con Django REST Framework

Proyecto del **laboratorio de la semana 8** de Desarrollo de Aplicaciones Empresariales (DAE):
implementación de servicios web con Django.

**Autor:** Alexander Faustino

## ¿Qué es este proyecto?

Este repositorio parte del proyecto de cuestionarios del **Lab 03** (modelos `Exam`, `Question` y
`Choice`, con formularios, plantillas y administración) y lo convierte en un **servicio web REST**
con **Django REST Framework (DRF)**.

En el Lab 03 la aplicación solo mostraba páginas HTML. Ahora, además, expone sus datos en **JSON por
HTTP**, de modo que cualquier cliente (un frontend en React, una app móvil, Postman o un script)
puede listar, consultar, crear, modificar y eliminar exámenes, preguntas y opciones.

Las vistas HTML del Lab 03 se conservan intactas en `/quiz/`; la API vive aparte, en `/api/`.


## Puesta en marcha

```bash
git clone https://github.com/AlexanderFtn06/Lab08-DAE.git
cd Lab08-DAE

python -m venv venv
source venv/Scripts/activate        # Git Bash
# venv\Scripts\Activate.ps1         # PowerShell

pip install -r requirements.txt
cp .env.example .env                # variables de entorno (ALLOWED_HOSTS, SECRET_KEY, DEBUG)

cd src
python manage.py migrate
python manage.py seed_quiz          # carga los datos fijos de prueba
python manage.py runserver
```

`settings.py` no contiene credenciales escritas a mano: las lee del archivo `.env`, que no se sube
al repositorio. Si falta `.env`, Django responde `DisallowedHost` porque `ALLOWED_HOSTS` queda vacío.

### Direcciones principales

| Dirección | Qué hay |
|---|---|
| `http://127.0.0.1:8000/api/` | Raíz de la API navegable de DRF |
| `http://127.0.0.1:8000/api/exams/` | Recurso exámenes |
| `http://127.0.0.1:8000/api/questions/` | Recurso preguntas (con opciones anidadas) |
| `http://127.0.0.1:8000/api/choices/` | Recurso opciones |
| `http://127.0.0.1:8000/quiz/` | Vistas HTML del Lab 03 |
| `http://127.0.0.1:8000/admin/` | Administración de Django |

## Estructura del proyecto

```
Lab08-DAE/
├── .opencode/agent/          # agentes de OpenCode (Lab 03 + nuevos del Lab 08)
├── docs/
│   ├── API.md                # tabla de la API (paso 11)
│   └── api.http              # peticiones para REST Client (pasos 8, 9 y 10)
├── src/
│   ├── manage.py
│   ├── config/config/
│   │   ├── settings.py       # INSTALLED_APPS y bloque REST_FRAMEWORK
│   │   └── urls.py           # incluye api/ y quiz/
│   └── quiz/
│       ├── models.py         # Exam, Question, Choice (del Lab 03, sin cambios)
│       ├── serializers.py    # serializadores y validación propia
│       ├── api_views.py      # ModelViewSet de los tres recursos
│       ├── api_urls.py       # DefaultRouter
│       ├── views.py, urls.py, forms.py, templates/   # vistas HTML del Lab 03
│       ├── tests.py          # pruebas del serializador
│       └── management/commands/seed_quiz.py         # datos de prueba
├── .env.example
├── requirements.txt
└── README.md
```

## Modelo de datos

Los modelos vienen del Lab 03 y **no se modificaron** en este laboratorio.

| Modelo | Campos | Relación |
|---|---|---|
| `Exam` | `title`, `description`, `created_at` | Tiene muchas preguntas |
| `Question` | `exam`, `statement`, `score` | Pertenece a un examen; tiene muchas opciones |
| `Choice` | `question`, `text`, `is_correct` | Pertenece a una pregunta |

## Lo que se hizo, paso a paso

### 1. Instalación de Django REST Framework

Se instalaron `djangorestframework` y `django-filter`, y se declararon `rest_framework` y
`django_filters` en `INSTALLED_APPS` junto con la aplicación `quiz`. El `requirements.txt`, que
estaba en UTF-16, se reescribió en UTF-8.

### 2. Configuración del bloque REST_FRAMEWORK

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
}
```

- **Paginación:** 5 elementos por página, pequeño a propósito para ver varias páginas con los datos
  de prueba.
- **Permiso de partida:** `AllowAny`, solo para desarrollo. En producción se usaría
  `IsAuthenticatedOrReadOnly`.
- Los *backends* de filtrado se agregaron en el paso 10.

### 3. Serializadores con ModelSerializer

En `src/quiz/serializers.py` se escribió un serializador por modelo, con la lista de campos
expuestos (`fields`) y los de solo lectura (`read_only_fields`) declarados de forma explícita, sin
usar `"__all__"`.

| Serializador | Campos expuestos | Solo lectura |
|---|---|---|
| `ExamSerializer` | `id`, `title`, `description`, `created_at` | `id`, `created_at` |
| `QuestionSerializer` | `id`, `exam`, `statement`, `score`, `choices` | `id` |
| `ChoiceSerializer` | `id`, `question`, `text`, `is_correct` | `id` |
| `NestedChoiceSerializer` | `id`, `text`, `is_correct` | `id` |

### 4. Cómo viajan las relaciones

- **Las opciones viajan anidadas dentro de la pregunta.** Una opción solo tiene sentido como parte de
  su pregunta, así que el cliente crea y lee una pregunta con todas sus opciones en una sola
  petición. Para eso se usa `NestedChoiceSerializer`, que no incluye el campo `question`.
- **El examen viaja por identificador** (`"exam": 5`), para no repetir los datos del examen en cada
  pregunta. Si el cliente lo necesita, lo consulta en `/api/exams/`.

Como las opciones anidadas no se guardan solas, `QuestionSerializer` implementa `create()` y
`update()` dentro de `transaction.atomic()`:

- `create()` guarda la pregunta y luego sus opciones; si algo falla, no se guarda nada a medias.
- `update()` reemplaza las opciones solo si el cliente las envía. Un **PATCH sin `choices`** cambia
  la pregunta y **conserva las opciones con sus mismos ids**.

Ejemplo de una pregunta tal como la devuelve la API:

```json
{
    "id": 15,
    "exam": 5,
    "statement": "What is a list in Python?",
    "score": 2,
    "choices": [
        {"id": 41, "text": "A mutable ordered sequence", "is_correct": true},
        {"id": 42, "text": "An immutable tuple", "is_correct": false},
        {"id": 43, "text": "A key-value mapping", "is_correct": false}
    ]
}
```

### 5. Validación propia

El modelo por sí solo permitiría guardar una pregunta con cualquier número de opciones correctas.
Por eso `QuestionSerializer` incluye `validate_choices`, que rechaza la pregunta si:

- tiene **menos de dos opciones**: `"A question needs at least two choices."`
- no tiene **exactamente una opción correcta**: `"A question must have exactly one correct choice."`

La validación ocurre antes de tocar la base de datos. En un PATCH sin `choices` no se ejecuta,
porque las opciones existentes no cambian.

### 6. Conjuntos de vistas y enrutador

En `src/quiz/api_views.py` hay un `ModelViewSet` por recurso, que ofrece las cinco operaciones sin
escribirlas a mano. Se registraron en un `DefaultRouter` (`src/quiz/api_urls.py`), incluido desde
`config/urls.py` con el prefijo `api/`.

Los querysets están optimizados para evitar el problema N+1:

```python
Question.objects.select_related("exam").prefetch_related("choices").order_by("id")
Choice.objects.select_related("question").order_by("id")
```

### Preparación: datos de prueba

El comando `python manage.py seed_quiz` borra los datos de `quiz` y carga siempre los mismos:
**2 exámenes** ("Python Basics" con 7 preguntas y "Django ORM" con 5), **12 preguntas** y
**36 opciones**, con exactamente una correcta por pregunta. Se puede repetir sin duplicar datos.

Los ids no se reinician al volver a ejecutarlo: para los ejemplos de este documento, los exámenes
tienen los ids 5 y 6. Si se vuelve a ejecutar, conviene consultar los nuevos ids en `/api/exams/`.

### 7. Recorrido por la API navegable

Se recorrieron las cinco operaciones del recurso preguntas desde la API navegable de DRF. Para crear
se usó la pestaña *Raw data* con JSON, porque el formulario HTML no admite listas anidadas.

| Operación | Método | Dirección | Código |
|---|---|---|---|
| Listar | GET | `/api/questions/` | 200 OK |
| Detalle | GET | `/api/questions/15/` | 200 OK |
| Crear | POST | `/api/questions/` | 201 Created |
| Modificar parcialmente | PATCH | `/api/questions/{id}/` | 200 OK |
| Eliminar | DELETE | `/api/questions/{id}/` | 204 No Content |
| Detalle tras eliminar | GET | `/api/questions/{id}/` | 404 Not Found |

### 8. Cliente HTTP externo

Las mismas operaciones se repitieron con la extensión **REST Client** de VS Code, enviando el cuerpo
en JSON con `Content-Type: application/json`. Las peticiones están en
[`docs/api.http`](docs/api.http). El PATCH y el DELETE usan el id devuelto por el POST mediante la
variable `{{createQuestion.response.body.id}}`.

Los códigos obtenidos (**200, 200, 201, 200, 204 y 404**) coinciden con los de la API navegable, lo
que confirma que la API se comporta igual sin importar el cliente.

### 9. Errores provocados a propósito

| Error | Cuerpo enviado | Código | Mensaje devuelto |
|---|---|---|---|
| Campo obligatorio ausente | Sin `statement` | 400 | `{"statement": ["This field is required."]}` |
| Tipo incorrecto | `"exam": "abc"` | 400 | `{"exam": ["Incorrect type. Expected pk value, received str."]}` |
| Validación de la opción correcta | Dos opciones con `is_correct: true` | 400 | `{"choices": ["A question must have exactly one correct choice."]}` |

Los dos primeros errores los detecta DRF automáticamente a partir del modelo. El tercero viene de
la validación propia del paso 5. Ninguna de las tres peticiones crea datos.

### 10. Filtrado, búsqueda y paginación

| Parámetro | Recurso | Efecto |
|---|---|---|
| `?exam=<id>` | `/api/questions/` | Solo las preguntas de ese examen |
| `?search=<texto>` | `/api/questions/` | Preguntas cuyo enunciado contiene el texto |
| `?question=<id>`, `?is_correct=true` | `/api/choices/` | Filtra opciones |
| `?search=<texto>` | `/api/exams/` | Busca en el título |
| `?page=<n>` | todos los listados | Página de resultados |

Resultados comprobados:

| Dirección | count | next | Código |
|---|---|---|---|
| `/api/questions/?exam=5` | 7 | `?exam=5&page=2` | 200 |
| `/api/questions/?exam=6` | 5 | null | 200 |
| `/api/questions/?search=list` | 6 | `?page=2&search=list` | 200 |
| `/api/questions/?page=3` | 12 | null (2 resultados) | 200 |
| `/api/questions/?page=99` | — | — | 404 `"Invalid page."` |

Con 12 preguntas y 5 por página se generan 3 páginas (5 + 5 + 2). La paginación se combina con los
filtros y la búsqueda: los enlaces `next` y `previous` conservan los parámetros.

### 11. Tabla de la API

La tabla completa (recurso, dirección, método, cuerpo de ejemplo y respuesta esperada) está en
[`docs/API.md`](docs/API.md). Se verificó contra la API real, incluidos los mensajes de error.

## Pruebas

| Tipo | Cómo ejecutarlas |
|---|---|
| API navegable | Abrir `http://127.0.0.1:8000/api/` en el navegador |
| Cliente externo | Abrir `docs/api.http` en VS Code con REST Client y usar *Send Request* |
| Pruebas automáticas | `python manage.py test quiz -v 2` (desde `src/`) |

Las pruebas automáticas usan una base de datos temporal, así que no modifican los datos de
desarrollo.

## Decisiones de diseño y limitación conocida

- **Opciones anidadas en la pregunta y examen por identificador**, como se explica en el paso 4.
- **API separada de las vistas HTML:** los archivos `api_views.py` y `api_urls.py` conviven con
  `views.py` y `urls.py` del Lab 03 sin modificarlos.
- **Limitación conocida:** la regla de exactamente una opción correcta se valida en
  `/api/questions/`. El recurso `/api/choices/` no la valida, así que cambiar `is_correct` desde allí
  puede dejar una pregunta con cero o dos correctas. La forma recomendada de cambiar las opciones es
  un PATCH a `/api/questions/{id}/` enviando `choices`.

## Desarrollo con OpenCode

El laboratorio se desarrolló con **OpenCode**, usando agentes especializados guardados en
`.opencode/agent/`. A los agentes del Lab 03 se sumaron estos:

| Agente | Responsabilidad |
|---|---|
| `django-drf-setup` | Instalar y configurar DRF y django-filter |
| `django-serializers` | Serializadores, relaciones anidadas y validaciones |
| `django-api-views` | ViewSets, router, filtros y búsqueda |
| `django-api-tests` | Pruebas automáticas de la API |
| `django-seed` | Comando de datos de prueba |
| `django-documentation` | `docs/API.md` y `docs/api.http` (actualizado) |

También se corrigió `django-models`, que describía campos que no existen en los modelos reales.
Las capturas, la verificación de cada respuesta y el recorrido por la API se hicieron de forma
manual.

