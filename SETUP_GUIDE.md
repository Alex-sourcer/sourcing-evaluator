# 📖 Setup Guide - Detailed Instructions

## Overview

Este proyecto tiene dos formas de ejecutarse:

1. **Local** - Desarrollo / Testing en tu máquina
2. **Cloud** - Deployment en Render/Railway/Heroku (acceso público)

Elige una según tus necesidades.

---

## SETUP LOCAL (Windows/macOS/Linux)

### Prerequisitos

- Python 3.10 o superior
- Git (opcional, para versionado)
- Gemini API key (gratuita)

### Paso 1: Descarga el proyecto

```bash
# Opción A: Si tienes git
git clone https://github.com/TU_USUARIO/sourcing-evaluator.git
cd sourcing-evaluator

# Opción B: Descarga como ZIP
# Ve a GitHub, descarga ZIP, descomprime, entra a la carpeta
cd sourcing-evaluator
```

### Paso 2: Crea un virtual environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

Deberías ver `(venv)` en tu terminal.

### Paso 3: Instala dependencias

```bash
pip install -r requirements.txt
```

Toma ~2 minutos. Espera a ver "Successfully installed".

### Paso 4: Configura variables de entorno

```bash
# Copia el template
cp .env.example .env
```

**Edita `.env`:**
```
GEMINI_API_KEY=AIzaSy_TU_CLAVE_AQUI
PORT=8000
```

### Paso 5: Obtén tu API key de Gemini

1. Ve a https://ai.google.dev
2. Click azul "Get API Key"
3. Click "Create API Key in Google Cloud Console"
4. Selecciona tu proyecto (o crea uno nuevo)
5. Copia la clave (ej: `AIzaSy...`)
6. Pégala en `.env` donde dice `AIzaSy_TU_CLAVE_AQUI`

### Paso 6: Prueba que todo funciona

```bash
python test_health.py
```

Deberías ver checkmarks verdes (✅). Si hay rojo (❌), sigue los pasos del script.

### Paso 7: Inicia la app

```bash
python app.py
```

Verás algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 8: Abre en navegador

```
http://localhost:8000
```

🎉 ¡Funciona!

### Parar la app

En la terminal, presiona `Ctrl+C` (Windows/Linux) o `Cmd+C` (macOS).

---

## SETUP CON DOCKER (opcional)

Si prefieres usar Docker en lugar de Python directo:

### Paso 1: Instala Docker

- Windows/macOS: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt-get install docker.io`

### Paso 2: Crea .env

```bash
echo "GEMINI_API_KEY=tu_clave_aqui" > .env
```

### Paso 3: Corre con Docker Compose

```bash
docker-compose up
```

Abre: `http://localhost:8000`

Para parar: `Ctrl+C`

---

## DEPLOYMENT EN RENDER.COM

### Prerequisitos

- Cuenta en GitHub
- Cuenta en Render.com (gratis)
- Tu código pusheado a GitHub

### Paso 1: Prepara tu repositorio

```bash
# Inicia Git si aún no lo has hecho
git init

# Agrega todos los archivos
git add .

# Primer commit
git commit -m "Initial commit: Sourcing Evaluator"

# Crea un repo en GitHub: https://github.com/new
# Copia la URL (ej: https://github.com/tu_usuario/sourcing-evaluator.git)

# Conecta y empuja
git remote add origin https://github.com/tu_usuario/sourcing-evaluator.git
git branch -M main
git push -u origin main
```

### Paso 2: Crea el Web Service en Render

1. Ve a https://dashboard.render.com
2. Click "New" → "Web Service"
3. Click "Connect Account" (GitHub)
4. Autoriza a Render a acceder a tu GitHub
5. Selecciona el repo `sourcing-evaluator`

### Paso 3: Configura el deployment

Completa estos campos:

| Campo | Valor |
|-------|-------|
| **Name** | `sourcing-evaluator` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |

### Paso 4: Agrega variables de entorno

1. Click "Advanced"
2. En "Environment Variables", click "Add"
3. **Key**: `GEMINI_API_KEY`
4. **Value**: tu_api_key_aqui

### Paso 5: Deployea

Click "Create Web Service"

Render empezará a buildear. Verás logs en la pantalla. Espera a ver:
```
Server running on port 10000
```

### Paso 6: Accede a tu app

Render te dará una URL como:
```
https://sourcing-evaluator.onrender.com
```

¡Listo! 🎉 Comparte este link con tu equipo.

---

## DEPLOYMENT EN RAILWAY.APP

### Prerequisitos

- Cuenta Railway.app (gratis)
- Código en GitHub

### Paso 1: Ve a Railway

https://railway.app/new

### Paso 2: Deploy from GitHub

1. Click "Deploy from GitHub"
2. Conecta tu GitHub
3. Selecciona el repo

### Paso 3: Configura variables

1. En el dashboard, ve a "Variables"
2. Agrega: `GEMINI_API_KEY=tu_clave`

### Paso 4: Deploy automático

Railway detecta automáticamente `requirements.txt` y el `Procfile`.

Espera a ver "Deployment successful".

### Paso 5: Accede

La URL está en el dashboard bajo "Deployments".

---

## TROUBLESHOOTING

### Python no encontrado

**Error**: `command not found: python3`

**Solución**: Instala Python desde https://python.org

Verifica con: `python3 --version`

### ModuleNotFoundError: No module named 'fastapi'

**Error**: Cuando corres `python app.py`

**Solución**: 
```bash
# Asegúrate de tener el venv activado
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstala
pip install -r requirements.txt
```

### GEMINI_API_KEY error

**Error**: `ValueError: GEMINI_API_KEY environment variable not set`

**Solución**:
```bash
# Verifica que .env existe
ls .env

# Verifica que tiene tu clave
cat .env

# Si no, crea .env correctamente:
echo "GEMINI_API_KEY=AIzaSy_AQUI" > .env
echo "PORT=8000" >> .env
```

### Port 8000 already in use

**Error**: `OSError: [Errno 48] Address already in use`

**Solución**:

**macOS/Linux**:
```bash
# Encuentra qué está usando el puerto
lsof -i :8000

# Mata el proceso
kill -9 <PID>
```

**Windows**:
```bash
# Encuentra
netstat -ano | findstr :8000

# Mata
taskkill /PID <PID> /F
```

O simplemente usa otro puerto en `.env`:
```
PORT=8001
```

### La app es lenta en Render

**Causa**: Free tier entra en "sleep" después de inactividad

**Solución**: 
- Primera request toma 30-60 segundos (spinning up)
- Luego es instantáneo
- Si necesitas mejor performance, upgrade a Render Pro

### Error conectando a Gemini

**Error**: `google.generativeai.types.generation_types.StopCandidateException`

**Causa**: API key inválida o expirada

**Solución**:
1. Ve a https://ai.google.dev
2. Verifica que tu API key está activa
3. Copia una nueva si es necesario
4. Actualiza en `.env` (local) o Render/Railway (en production)

### El formulario no envía

**Causa**: API key no está siendo usada correctamente

**Solución**:
1. Abre DevTools: F12 en navegador
2. Ve a Console
3. Busca errores rojo
4. Verifica que `POST /api/evaluate` devuelve status 200

---

## Verificación rápida después de deploy

### Test local

```bash
# En otra terminal (con la app corriendo)
curl http://localhost:8000/api/health

# Debe devolver:
# {"status":"ok"}
```

### Test en producción

```bash
# Reemplaza con tu URL de Render/Railway
curl https://tu-app.onrender.com/api/health

# Debe devolver:
# {"status":"ok"}
```

---

## Configuración de base de datos

La app usa SQLite automáticamente. El archivo `evaluations.db` se crea la primera vez que se corre.

**Local**: `evaluations.db` está en la carpeta del proyecto

**Render/Railway**: Está en el servidor (persiste entre redeploys)

Si quieres resetear:
```bash
rm evaluations.db
```

La próxima vez que corras la app, se creará una nueva.

---

## Monitoreo en producción

### Render

1. Dashboard → tu app
2. "Metrics" tab: Ver CPU, RAM, requests
3. "Logs" tab: Ver errores en tiempo real

### Railway

1. Dashboard → tu app
2. "Logs" tab: Último output
3. "Metrics" tab: Performance

---

## Siguiente paso

Una vez que todo funciona:

1. Lee **QUICKSTART.md** para aprender a usar
2. Lee **README.md** para más detalles
3. Lee **DEPLOYMENT.md** si necesitas hosting alternativo

¿Problemas? Contacta: alexmm930@gmail.com

---

Versión: 1.0  
Última actualización: 2026-08-23
