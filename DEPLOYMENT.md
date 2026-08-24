# 🚀 Guía de Deployment - Sourcing Evaluator

Elige tu opción preferida. Todas funcionan en 5-10 minutos.

---

## Opción 1️⃣: Render.com (Recomendado)

### Paso 1: Prepara tu API key de Gemini

1. Ve a https://ai.google.dev
2. Click "Get API Key" → "Create API Key in Google Cloud Console"
3. Copia tu API key (se verá así: `AIzaSy...`)

### Paso 2: Sube a GitHub

```bash
cd sourcing-evaluator

# Inicializa Git si no lo has hecho
git init

# Agrega todos los archivos
git add .

# Commit
git commit -m "Initial commit: Sourcing Evaluator"

# Crea un repo en GitHub: https://github.com/new
# Copia la URL del repo

# Empuja el código
git remote add origin https://github.com/TU_USUARIO/sourcing-evaluator.git
git branch -M main
git push -u origin main
```

### Paso 3: Deploy en Render

1. Ve a https://dashboard.render.com
2. Click **"New" → "Web Service"**
3. Conecta tu GitHub:
   - Click "Connect Account"
   - Autoriza a Render
   - Selecciona `sourcing-evaluator` repo
4. Configura:
   - **Name**: `sourcing-evaluator` (o lo que quieras)
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **"Advanced"**
6. En **Environment Variables**, agrega:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `tu_api_key_aqui` (la que copiaste)
7. Click **"Create Web Service"**
8. Espera 2-3 minutos. ¡Listo! 🎉

**Tu URL será**: `https://sourcing-evaluator.onrender.com`

---

## Opción 2️⃣: Railway.app (Más simple)

1. Ve a https://railway.app/new
2. Click **"Deploy from GitHub"**
3. Conecta tu GitHub y selecciona el repo
4. Railway detecta automáticamente la config
5. En el dashboard → **Variables**:
   - Agrega: `GEMINI_API_KEY=tu_api_key`
6. Click **"Deploy"**
7. ¡Listo en 1 minuto! 🚀

**URL**: En el dashboard bajo "Deployments"

---

## Opción 3️⃣: Replit.com (La más fácil)

1. Ve a https://replit.com
2. Click **"Create"** → **"Import from GitHub"**
3. Pega: `https://github.com/TU_USUARIO/sourcing-evaluator`
4. Click **"Import"**
5. En la pestaña **"Secrets"**:
   - Key: `GEMINI_API_KEY`
   - Value: `tu_api_key`
6. Click **"Run"**
7. Se abre automáticamente la URL pública

**URL**: Se genera automáticamente (ej: `https://sourcing-evaluator.replit.dev`)

---

## Opción 4️⃣: Heroku.com (Clásico)

Heroku dejó de ofrecer free tier. Pero si ya tienes créditos:

1. Instala Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. `heroku login`
3. `heroku create sourcing-evaluator`
4. `heroku config:set GEMINI_API_KEY=tu_api_key`
5. `git push heroku main`

---

## Ejecución local (desarrollo)

```bash
# 1. Virtual env
python3 -m venv venv
source venv/bin/activate

# 2. Instala
pip install -r requirements.txt

# 3. Crea .env
echo "GEMINI_API_KEY=tu_api_key" > .env

# 4. Corre
python app.py

# 5. Abre en navegador
# http://localhost:8000
```

---

## Verificación del deployment

Una vez deployado:

```bash
# Prueba health check
curl https://tu-url.onrender.com/api/health

# Output esperado:
# {"status":"ok"}
```

---

## ¿Qué pasa después?

✅ **La app está viva**
- Tu equipo puede ir a la URL y usarla
- Sin instalar nada
- Sin API keys para ellos

✅ **Los datos se guardan**
- Automáticamente en SQLite
- En el servidor de deployment
- Puedes compartir resultados con links

✅ **Límites Gemini free tier**
- 1,500 requests/día
- Suficiente para 150-300 evaluaciones
- Si necesitas más, upgrade en Google AI Studio

---

## Troubleshooting

### "Error: GEMINI_API_KEY not set"
✅ En Render: Settings → Environment Variables → Agrega/Revisa
✅ En Railway: Variables → Checa que esté
✅ Redeploy después de cambiar variables

### "Module not found: google.generativeai"
✅ Verifica que `requirements.txt` esté en el root
✅ Build command debe incluir `pip install -r requirements.txt`

### "App crashes en el deployment"
✅ Checa los logs:
- Render: Dashboard → Logs
- Railway: Logs tab
- Busca "GEMINI_API_KEY" o "ModuleNotFoundError"

### "La app es lenta en Render"
✅ Normal: free tier entra en sleep
✅ Primera request tarda 30s
✅ Luego es instantáneo

---

## ✨ Ya está deployado, ¿ahora qué?

### Comparte con tu equipo
```
Hola equipo, pueden usar esto para evaluar candidatos:
https://tu-url.onrender.com

Solo pegas:
- Descripción del puesto
- Candidatos (nombre + perfil)
- Y la IA hace el screening

Resultados en PDF/CSV incluidos
```

### Customizaciones (opcional)
- Edita `static/style.css` para cambiar colores/logo
- Edita `app.py` para ajustar el prompt de evaluación
- Commit y push, Render redeploya automáticamente

### Monitor en producción
- Render: Dashboard → Metrics (RAM, CPU)
- Railway: Analytics tab
- Logs siempre disponibles

---

¿Preguntas? Revisa README.md o contacta a Alejandro 🚀
