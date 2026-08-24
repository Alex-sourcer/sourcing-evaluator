# ⚡ Quick Start (5 minutos)

## 1️⃣ Obtén tu API key gratis (2 min)

1. Ve a https://ai.google.dev
2. Click azul **"Get API Key"**
3. Click **"Create API Key in Google Cloud Console"**
4. Copia la clave (se verá como: `AIzaSy...`)
5. ✅ Listo

## 2️⃣ Corre localmente o en la nube

### Opción A: Correr localmente (desarrollo)

```bash
# 1. Entra a la carpeta
cd sourcing-evaluator

# 2. Setup automático (macOS/Linux)
bash setup.sh

# 3. Activa el ambiente
source venv/bin/activate

# 4. Edita .env
nano .env
# Pega tu API key junto a GEMINI_API_KEY=

# 5. Corre
python app.py

# 6. Abre en navegador
# http://localhost:8000 ✅
```

### Opción B: Deployment en Render (5 min)

```bash
# 1. Sube a GitHub
git init
git add .
git commit -m "Sourcing Evaluator"
git remote add origin https://github.com/TU_USER/sourcing-evaluator
git push -u origin main

# 2. Ve a https://dashboard.render.com
# 3. "New Web Service"
# 4. Conecta tu GitHub repo
# 5. Settings:
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn app:app --host 0.0.0.0 --port $PORT
# 6. Environment Variable:
#    - GEMINI_API_KEY = tu_clave_aqui
# 7. "Create Web Service"
# 8. Espera 3 min

# ¡Tu URL está en el dashboard! 🚀
```

### Opción C: Con Docker

```bash
# 1. Crea .env con tu API key
echo "GEMINI_API_KEY=tu_clave" > .env

# 2. Corre
docker-compose up

# 3. Abre
# http://localhost:8000 ✅
```

---

## 🎯 Cómo usar

### Flujo básico (30 segundos)

1. **Pega Job Description**
   - Copia la descripción del puesto
   - Pégala en el primer campo

2. **Agrega Candidatos**
   - Nombre: "Juan García"
   - Perfil: "5 años Python, Django, REST APIs, PostgreSQL"
   - LinkedIn: (opcional)
   - Click "+ Agregar Candidato" para más

3. **Evalúa**
   - Click "Evaluar Candidatos"
   - Espera 30-60 segundos
   - IA analiza automáticamente

4. **Ver Resultados**
   - **Match Score**: 0-100%
   - **Fortalezas**: Lo que destacó
   - **Red Flags**: Gaps o concerns
   - **Questions**: Preguntas para entrevista
   - **Recomendación**: STRONG YES / YES / MAYBE / NO

5. **Compartir o Exportar**
   - **Exportar CSV**: Para tu spreadsheet
   - **Compartir Link**: Equipo puede ver sin acceso

---

## 📊 Ejemplo real

### Input
```
Job Description:
Senior Backend Engineer (Python)
- 5+ years Python, FastAPI/Django
- PostgreSQL, Redis
- AWS, Docker
- Team lead experience preferred

Candidato:
Juan García
5 años en Python, especializado en Django y FastAPI.
Trabajé con PostgreSQL y Redis. 
Experiencia en AWS y Docker.
LinkedIn: linkedin.com/in/juangarcia
```

### Output
```
Match Score: 78%
✅ Strong Technical Fit

Strengths:
→ Solid Python expertise (FastAPI/Django)
→ Hands-on cloud experience (AWS)
→ Database & caching knowledge

Red Flags:
→ No team lead experience mentioned

Interview Questions:
→ Tell us about your biggest leadership moment
→ How do you approach code reviews?
→ What's your DevOps philosophy?

Recommendation: YES
```

---

## 🆘 Troubleshooting rápido

| Problema | Solución |
|----------|----------|
| "API key not found" | Revisa `.env`, agrega tu clave |
| "Port 8000 in use" | `lsof -i :8000` y `kill -9 <PID>` |
| "Module not found" | `pip install -r requirements.txt` |
| "Gemini error" | Checa que la API key sea válida en https://ai.google.dev |
| "App lenta" | Normal en free tier Render. Espera 30s primer request |

---

## 📈 Límites & Costs

- **Gemini API Free**: 1,500 requests/día ✅
- **Render Free Tier**: Gratuito indefinidamente ✅
- **Rails for deploy**: 0€ ✅
- **Total para 10 personas**: **FREE** 🎉

Si necesitas más requests, upgrade Gemini en https://aistudio.google.com (pago por uso).

---

## 🎓 Próximos pasos

### Personalizar
- Edita `static/index.html` para agregar logo
- Edita `static/style.css` para cambiar colores
- Modifica prompt en `app.py` línea ~80 para ajustar criterios

### Escalar
- Upgrade a Render Pro para mejor rendimiento
- Agregar autenticación si quieres restringir acceso
- Integrar con tu ATS (Workable, Lever, etc)

### Monitor
- Render Dashboard: Metrics
- Check logs si hay errores
- API key usage en Google AI Studio

---

## ✅ Checklist de deployment

- [ ] API key de Gemini obtenida
- [ ] Código subido a GitHub (si usas Render)
- [ ] Variables de entorno configuradas
- [ ] Deployment creado
- [ ] URL funciona en navegador
- [ ] Primero que evalúen un candidato (may take 30s)
- [ ] Compartir URL con equipo

---

¿Listo? 🚀

**Opción más simple**: Render + GitHub (5 minutos, 0 config)

Ve a **DEPLOYMENT.md** para pasos detallados.

---

Para ayuda: alexmm930@gmail.com
