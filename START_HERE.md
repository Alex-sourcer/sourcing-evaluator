# 🚀 START HERE

Acabas de recibir una web app profesional para evaluar candidatos con IA. Aquí está todo lo que necesitas.

---

## ⏱️ 3 opciones (elige una)

### Opción 1: Correr en tu máquina (10 min, sin hosting)
```bash
bash setup.sh
python app.py
```
→ Abre `http://localhost:8000`

**Leer**: [SETUP_GUIDE.md](SETUP_GUIDE.md) sección "SETUP LOCAL"

---

### Opción 2: Deploy en Render.com (5 min, público + gratis)
```bash
git init && git add . && git commit -m "init"
git push
# Ve a https://dashboard.render.com → Web Service
```
→ Todos pueden acceder por link público

**Leer**: [SETUP_GUIDE.md](SETUP_GUIDE.md) sección "DEPLOYMENT EN RENDER.COM"

---

### Opción 3: Usa Docker (docker-compose up)
```bash
echo "GEMINI_API_KEY=tu_clave" > .env
docker-compose up
```
→ Abre `http://localhost:8000`

**Leer**: [SETUP_GUIDE.md](SETUP_GUIDE.md) sección "SETUP CON DOCKER"

---

## 📋 Checklist de setup

- [ ] Tienes Python 3.10+ instalado (o Docker)
- [ ] Tienes API key de Gemini (https://ai.google.dev)
- [ ] Elegiste una opción arriba
- [ ] Seguiste los pasos

---

## 📚 Archivos importantes

| Archivo | Qué hace |
|---------|----------|
| **app.py** | Backend (FastAPI + Gemini API) |
| **static/** | Frontend (HTML/CSS/JS) |
| **README.md** | Documentación completa |
| **QUICKSTART.md** | Cómo usar la app |
| **SETUP_GUIDE.md** | Instrucciones detalladas |
| **DEPLOYMENT.md** | Todas las opciones de hosting |

---

## 🎯 Qué hace esta app

✅ Pegas un job description  
✅ Agregas candidatos (nombre + perfil)  
✅ IA evalúa en 30-60 segundos  
✅ Ves resultados: Match score, fortalezas, red flags, preguntas  
✅ Exportas a CSV o compartes link  

Eso es todo. Simple y profesional.

---

## 🆘 Stuck?

1. ¿Error? Lee [SETUP_GUIDE.md](SETUP_GUIDE.md) sección "TROUBLESHOOTING"
2. ¿Cómo usar? Lee [QUICKSTART.md](QUICKSTART.md)
3. ¿Más info? Lee [README.md](README.md)

---

## 📊 Estructura del proyecto

```
sourcing-evaluator/
├── app.py                    ← Backend
├── requirements.txt          ← Dependencias Python
├── Procfile                  ← Config para Render
├── .env.example              ← Template de variables
├── setup.sh                  ← Script de setup automático
├── Dockerfile / docker-compose.yml  ← Opción Docker
│
├── static/
│   ├── index.html            ← Interfaz (frontend)
│   ├── style.css             ← Estilos
│   └── script.js             ← Lógica (JavaScript)
│
├── START_HERE.md             ← Este archivo
├── QUICKSTART.md             ← Cómo usar (30 min)
├── SETUP_GUIDE.md            ← Setup detallado (localhost/render)
├── DEPLOYMENT.md             ← Todas las opciones de deploy
└── README.md                 ← Documentación completa
```

---

## 🚦 Quick flow

```
1. GET API KEY
   ↓
2. CHOOSE OPTION (Local/Render/Docker)
   ↓
3. FOLLOW SETUP_GUIDE.md
   ↓
4. APP RUNS ✅
   ↓
5. READ QUICKSTART.md
   ↓
6. START EVALUATING CANDIDATES 🎉
```

---

## 🔥 El truco que hace esto simple

- **API Key**: Solo tú la configuras UNA VEZ
- **Frontend**: Sin login, sin config, sin frío
- **Backend**: Automanejo de evaluaciones y compartir
- **Deploy**: Render/Railway lo hace automático

Tu equipo solo necesita: **Una URL**

---

## 💾 Costos

- Gemini API Free: 1,500 requests/día ✅ $0
- Render Free: Hosting ✅ $0
- Railway Free: Hosting alternativo ✅ $0
- Desarrollo: 0 minutos de pago ✅ $0

**Total para 10 personas**: $0 🎉

---

## 🎓 Aprendiste

- FastAPI backend + Gemini API integration
- Frontend vanilla JavaScript (sin frameworks)
- SQLite para persistencia
- Deployment automático (Git push = deploy)
- Evaluación de candidatos con IA
- Compartir links públicos seguros

---

## 🎯 Próximos pasos (opcional)

Después de que funcione:

1. Personaliza logo/colores en `static/`
2. Ajusta criterios en `app.py` (línea ~80)
3. Integra con tu ATS si lo tienes
4. Agrega autenticación si quieres

---

## 📞 Contacto

**Preguntas o bugs?**
- Email: alexmm930@gmail.com
- GitHub: [tu_usuario]/sourcing-evaluator

---

## ✨ Ready?

### Opción 1 (Local):
```bash
bash setup.sh && python app.py
```

### Opción 2 (Render):
```bash
git push && ve a dashboard.render.com
```

### Opción 3 (Docker):
```bash
docker-compose up
```

**¡Ahora abre la app y evalúa tu primer candidato!**

---

Hecho con ❤️ por Alejandro Mariana Muñoz para Talent Acquisition  
Powered by Google Gemini API
