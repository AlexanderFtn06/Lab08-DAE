# Documentación de la API REST

**Base URL:** `http://127.0.0.1:8000/api/`

**Formato:** JSON

**Paginación:** PageNumberPagination con `PAGE_SIZE = 5`. Las respuestas de listado incluyen:
- `count`: total de elementos
- `next`: URL de la siguiente página (o `null`)
- `previous`: URL de la página anterior (o `null`)
- `results`: array con los elementos de la página actual

**Permisos:** `AllowAny` (solo para desarrollo; en producción usar `IsAuthenticatedOrReadOnly`)

> **Nota:** Los ids de los ejemplos corresponden a los datos de `seed_quiz`; si se vuelve a ejecutar, los ids cambian (consultar `/api/exams/` y `/api/questions/`).

---

## 1. Tabla principal de endpoints

| Recurso | Dirección | Método | Cuerpo de ejemplo | Respuesta esperada |
|---------|-----------|--------|-------------------|-------------------|
| **Exams** | `/exams/` | GET | — | 200: lista paginada de exámenes |
| **Exams** | `/exams/` | POST | `{"title":"Nuevo Examen","description":"Desc"}` | 201: examen creado con `id`, `title`, `description`, `created_at` |
| **Exams** | `/exams/{id}/` | GET | — | 200: examen con `id`, `title`, `description`, `created_at` |
| **Exams** | `/exams/{id}/` | PATCH | `{"title":"Título actualizado"}` | 200: examen actualizado |
| **Exams** | `/exams/{id}/` | DELETE | — | 204: sin contenido; elimina en cascada sus preguntas y opciones |
| **Questions** | `/questions/` | GET | — | 200: lista paginada de preguntas |
| **Questions** | `/questions/` | POST | `{"exam":5,"statement":"¿Qué es REST?","score":2,"choices":[{"text":"Estilo arquitectónico","is_correct":true},{"text":"Lenguaje","is_correct":false},{"text":"Base de datos","is_correct":false}]}` | 201: pregunta creada con `id`, `exam`, `statement`, `score`, `choices` (array con `id`, `text`, `is_correct`) |
| **Questions** | `/questions/{id}/` | GET | — | 200: pregunta con sus choices anidadas |
| **Questions** | `/questions/{id}/` | PATCH | `{"statement":"¿Qué es REST exactamente?"}` | 200: pregunta actualizada (choices se conservan si no se envían) |
| **Questions** | `/questions/{id}/` | PATCH | `{"choices":[{"text":"A","is_correct":true},{"text":"B","is_correct":false}]}` | 200: reemplaza todas las opciones anteriores por las enviadas (aplica la validación) |
| **Questions** | `/questions/{id}/` | DELETE | — | 204: sin contenido |
| **Choices** | `/choices/` | GET | — | 200: lista paginada de opciones |
| **Choices** | `/choices/` | POST | `{"question":15,"text":"Nueva opción","is_correct":false}` | 201: opción creada con `id`, `question`, `text`, `is_correct` |
| **Choices** | `/choices/{id}/` | GET | — | 200: opción individual |
| **Choices** | `/choices/{id}/` | PATCH | `{"is_correct":true}` | 200: opción actualizada |
| **Choices** | `/choices/{id}/` | DELETE | — | 204: sin contenido |

---

## 2. Filtros, búsqueda y paginación

| Parámetro | Recurso | Descripción | Respuesta esperada |
|-----------|---------|-------------|-------------------|
| `?exam={id}` | `/questions/` | Filtrar preguntas por examen | 200: solo preguntas de ese examen |
| `?search=list` | `/questions/` | Buscar en `statement` (contiene "list") | 200: preguntas cuyo enunciado contiene "list" |
| `?question={id}` | `/choices/` | Filtrar opciones por pregunta | 200: solo opciones de esa pregunta |
| `?is_correct=true` | `/choices/` | Filtrar por correctas/incorrectas | 200: opciones que cumplen la condición |
| `?search=texto` | `/exams/` | Buscar en `title` | 200: exámenes cuyo título contiene el texto |
| `?page=2` | `/questions/` | Segunda página (5 por página) | 200: página 2 de resultados |
| `?page=3` | `/questions/` | Última página (incompleta) | 200: página 3 con resultados restantes |
| `?exam={id}&page=2` | `/questions/` | Filtro combinado con paginación | 200: página 2 de ese examen |
| `?page=99` | `/questions/` | Página que no existe | 404: `{"detail":"Invalid page."}` |

---

## 3. Errores de validación

| Error | Cuerpo enviado | Código | Mensaje exacto |
|-------|----------------|--------|----------------|
| Campo obligatorio ausente (`statement`) | `{"exam":5,"score":1,"choices":[{"text":"A","is_correct":true},{"text":"B","is_correct":false}]}` | 400 | `{"statement":["This field is required."]}` |
| Tipo incorrecto (`exam` como string) | `{"exam":"abc","statement":"Valid","score":2,"choices":[{"text":"A","is_correct":true},{"text":"B","is_correct":false},{"text":"C","is_correct":false}]}` | 400 | `{"exam":["Incorrect type. Expected pk value, received str."]}` |
| Validación: dos opciones correctas | `{"exam":5,"statement":"Q","score":2,"choices":[{"text":"A","is_correct":true},{"text":"B","is_correct":true},{"text":"C","is_correct":false}]}` | 400 | `{"choices":["A question must have exactly one correct choice."]}` |
| Validación: menos de dos opciones | `{"exam":5,"statement":"Q","score":2,"choices":[{"text":"A","is_correct":true}]}` | 400 | `{"choices":["A question needs at least two choices."]}` |
| Recurso inexistente: Exam (GET /exams/999/) | — | 404 | `{"detail":"No Exam matches the given query."}` |
| Recurso inexistente: Question (GET /questions/999/) | — | 404 | `{"detail":"No Question matches the given query."}` |
| Recurso inexistente: Choice (GET /choices/999/) | — | 404 | `{"detail":"No Choice matches the given query."}` |

---

## 4. Decisiones de diseño

- **Opciones anidadas en la pregunta:** las choices viajan dentro de `questions` porque una opción solo tiene sentido como parte de su pregunta; el cliente crea y lee una pregunta con sus opciones en una sola petición.
- **Examen por identificador:** el campo `exam` en `QuestionSerializer` es una clave primaria (PrimaryKeyRelatedField) para evitar repetir los datos del examen en cada pregunta; el cliente obtiene el examen desde `/exams/` si lo necesita.
- **PATCH sin choices conserva las opciones:** al hacer una actualización parcial sin enviar `choices`, las opciones existentes se mantienen con sus mismos IDs.
- **Validación de exactamente una opción correcta:** `validate_choices` en `QuestionSerializer` exige que haya exactamente una choice con `is_correct=true` y al menos dos opciones en total.
- **Limitación conocida:** la regla de exactamente una opción correcta se valida en `/questions/` (opciones anidadas). El recurso `/choices/` no la valida, por lo que modificar `is_correct` desde allí puede dejar una pregunta con cero o dos correctas. La forma recomendada de cambiar las opciones es un PATCH a `/questions/{id}/` enviando `choices`.