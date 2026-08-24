# Sourcing Evaluator Agent

Herramienta de evaluación inteligente de candidatos usando Gemini API. Diseñada para equipos de TA que necesitan hacer screening rápido y profesional de candidatos.

## Características

✨ **Frontend moderno y responsive**
- Interfaz limpia y profesional
- Funciona en móvil, tablet y desktop
- Sin configuraciones complicadas

🤖 **Evaluación con IA**
- Usa Google Gemini API (gratis)
- Match score automático (0-100%)
- Análisis de fortalezas y red flags
- Recomendaciones de entrevista

💾 **Historial y compartir**
- Guarda automáticamente evaluaciones
- Genera links para compartir con el equipo
- Exporta resultados a CSV

## Instalación local (desarrollo)

### Requisitos
- Python 3.10+
- pip

### Pasos

1. **Clona o descarga el proyecto**
```bash
cd sourcing-evaluator
```

2. **Crea un entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# o en Windows: venv\Scripts\activate
```

3. **Instala dependencias**
```bash
pip install -r requirements.txt
```

4. **Configura variables de entorno**
```bash
cp .env.example .env
```

Edita `.env` y agrega tu API key de Gemini:
```
GEMINI_API_KEY=tu_api_key_aqui
PORT=8000
```

> **Cómo obtener tu API key gratis de Gemini:**
> 1. Ve a https://ai.google.dev/
> 2. Click en "Get API Key"
> 3. Click en "Create API Key in Google Cloud Console"
> 4. Selecciona tu proyecto o crea uno nuevo
> 5. Copia la API key en `.env`

5. **Ejecuta la aplicación**
```bash
python app.py
```

Abre tu navegador en `http://localhost:8000`

## Deployment en Render.com (5 minutos)

### Pasos

1. **Sube el código a GitHub**
```bash
git init
git add .
git commit -m "Initial commit: Sourcing Evaluator"
git remote add origin https://github.com/TU_USUARIO/sourcing-evaluator
git push -u origin main
```

2. **Crea un nuevo Web Service en Render**
   - Ve a https://dashboard.render.com
   - Click en "New" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Nombre del servicio: `sourcing-evaluator`

3. **Configura el deployment**
   - **Environment**: Python 3.10+
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

4. **Agrega variables de entorno**
   - Click en "Environment"
   - Agrega:
     - Key: `GEMINI_API_KEY`
     - Value: `tu_api_key_aqui`

5. **Deploy**
   - Click en "Deploy Web Service"
   - Espera 2-3 minutos
   - Accede a tu app en `https://sourcing-evaluator.onrender.com`

### ¿Y si Render me pide tarjeta?
Render ofrece un free tier sin tarjeta para pequeños proyectos. Si te lo pide:
- Usa Railway.app (similar setup)
- O Replit.com (¡aún más simple!)

## Deployment en Railway.app (alternativa)

1. **Sube a GitHub** (igual que arriba)

2. **Ve a Railway.app**
   - Click en "Deploy on Railway"
   - O ve a https://railway.app/new

3. **Conecta GitHub y selecciona el repo**

4. **Agrega variable de entorno**
   - En el dashboard, ve a "Variables"
   - Agrega: `GEMINI_API_KEY=tu_api_key_aqui`

5. **Deploy automático**
   - Railway detecta el Procfile
   - Deploy en 1-2 minutos
   - URL en el dashboard

## Uso

### Flujo básico

1. **Pega la job description** en el primer campo
2. **Agrega candidatos** con su nombre y perfil (LinkedIn es opcional)
3. **Click en "Evaluar Candidatos"**
4. **Espera 30-60 segundos** mientras Gemini evalúa
5. **Ver resultados** con:
   - Match Score (0-100%)
   - Technical Fit
   - Fortalezas
   - Red Flags
   - Preguntas de entrevista
   - Recomendación final
   - Razonamiento

### Acciones disponibles

- **Exportar CSV**: Descarga los resultados en formato spreadsheet
- **Compartir**: Genera un link para que tu equipo vea los resultados
- **Nueva Evaluación**: Limpia el formulario para la siguiente ronda

## Límites

- **Gemini API Free Tier**: 1,500 requests/día
- Cada evaluación es ~1 request por candidato
- Suficiente para 150-300 evaluaciones diarias

Si necesitas más volumen, simplemente sube a plan pago de Gemini.

## Estructura del proyecto

```
sourcing-evaluator/
├── app.py                 # Backend FastAPI
├── requirements.txt       # Dependencias Python
├── Procfile               # Config para Render/Heroku
├── .env.example          # Template de variables
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Este archivo
└── static/
    ├── index.html        # Frontend HTML
    ├── style.css         # Estilos
    └── script.js         # Lógica JavaScript
```

## Base de datos

Los resultados se guardan automáticamente en `evaluations.db` (SQLite).
- Cada usuario puede generar un link compartible
- No hay expirción de evaluaciones
- El archivo se sincroniza en el servidor de Render

## Troubleshooting

### "Error: GEMINI_API_KEY not found"
- Verifica que `.env` tenga la API key
- En Render, ve a Settings → Environment Variables
- Guarda cambios y redeploy

### "Port 8000 already in use"
```bash
lsof -i :8000  # Identifica el proceso
kill -9 <PID>  # Lo mata
```

### Gemini devuelve JSON inválido
- Algunos perfiles de candidatos muy largos pueden causar parsing issues
- Reduce el texto del perfil a max 500 caracteres por candidato

### La app es lenta en la primera carga
- Free tier de Render entra en "sleep" después de inactividad
- Primera request tarda 30 segundos
- Luego es instantáneo

## API Endpoints

```
POST   /api/evaluate              - Evalúa candidatos
GET    /api/evaluation/{id}       - Obtiene una evaluación guardada
GET    /api/share/{token}         - Obtiene evaluación por share link
GET    /api/health                - Health check
GET    /static/*                  - Archivos estáticos
```

## Seguridad

- La API key nunca se expone al frontend
- Los datos están encriptados en tránsito (HTTPS)
- Los links de compartir son tokens aleatorios (imposibles de adivinar)
- No hay autenticación necesaria (asumimos uso interno)

## Roadmap

- [ ] Autenticación de usuarios
- [ ] Búsqueda de candidatos en LinkedIn
- [ ] Integración con ATS (Workable, Lever, etc.)
- [ ] Guardado de templates de JD
- [ ] Análisis de tendencias por mes
- [ ] Webhooks para notificaciones

## Licencia

MIT - Úsalo, modifícalo, compártelo.

## Soporte

¿Problemas? Checa:
1. API key válida en `.env`
2. Render/Railway correctamente configurado
3. Conexión a internet
4. La app está funcionando (Dashboard en Render)

---

**Creado por**: Alejandro Mariana Muñoz  
**Email**: alexmm930@gmail.com  
**Powered by**: Google Gemini API
