# 🎯 Complete Guide - Sourcing Evaluator Agent v2.1

## Executive Summary

Has construido un **sistema de screening inteligente de candidatos** que:

✅ Evalúa candidatos con IA (Gemini)  
✅ Genera search queries automáticas  
✅ Proporciona analytics en tiempo real  
✅ Predice conversión (hire probability)  
✅ Exporta datos a CSV/Sheets  
✅ Soporta múltiples usuarios simultáneamente  
✅ Sin costo adicional (Gemini free tier)  

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)              │
│  ┌────────────┬──────────────┬──────────────────────┐  │
│  │ Evaluador  │ Buscador de  │ Dashboard Analytics │  │
│  │            │ Candidatos   │                      │  │
│  │ • Inputs   │ • Auto-gen   │ • KPI Cards         │  │
│  │ • Cards    │   queries    │ • Score bands       │  │
│  │ • Export   │ • Tips       │ • Conversion rates  │  │
│  └────────────┴──────────────┴──────────────────────┘  │
└──────────────────────────┬──────────────────────────────┘
                           │
                     (REST API)
                           │
┌──────────────────────────▼──────────────────────────────┐
│          BACKEND (FastAPI + Python)                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Endpoints:                                        │ │
│  │ • /api/evaluate          → Gemini AI            │ │
│  │ • /api/search-candidates → Generate queries    │ │
│  │ • /api/dashboard/stats   → Analytics           │ │
│  │ • /api/conversion-analytics → Predictions      │ │
│  │ • /api/export-google-sheets → CSV export       │ │
│  │ • /api/candidate-outcome → Track hires         │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
        (API KEY)      (SQLite)      (Gemini)
            │              │              │
     ┌──────▼──┐    ┌──────▼──┐    ┌──────▼──┐
     │  Gemini │    │ Database │    │   AI    │
     │   API   │    │ (Evals)  │    │ Engine  │
     └─────────┘    └──────────┘    └─────────┘
```

---

## 🎯 Features by Tab

### Tab 1: Evaluador de Candidatos

**Input:**
- Job Description
- Lista de candidatos (nombre, perfil, LinkedIn)

**Output (por candidato):**
- Match Score (0-100%)
- Technical Fit (resumen)
- Strengths (lista 3-4)
- Red Flags (lista 2-3)
- Interview Questions (preguntas generadas)
- Recommendation (STRONG YES / YES / MAYBE / NO)
- Reasoning (explicación)

**Actions:**
- 📥 Export CSV
- 📊 Export Sheets
- 🔗 Share link
- ↺ New evaluation

---

### Tab 2: Buscador de Candidatos

**Input:**
- Job Description

**Output:**
- 5-7 LinkedIn search queries optimizadas
- Descripción del candidato ideal
- Tips para la búsqueda

**How it works:**
1. Pega JD
2. IA analiza qué skills, experience, title buscar
3. Genera queries que puedes copiar/pegar en LinkedIn
4. Click en query → Se copia automáticamente

---

### Tab 3: Dashboard Analytics

**KPI Cards:**
- Evaluaciones totales
- Match score promedio
- Usuario más activo
- Strong YES recommendations

**Charts:**
- Recomendaciones (STRONG YES / YES / MAYBE / NO)
- Top usuarios
- Actividad por día (últimos 30 días)
- Evaluaciones por departamento

**Predicción de Conversión:**
- Overall conversion rate
- Score band analysis
- Hire probability by score
- Insights automáticos

---

## 📈 Advanced Features (v2.1)

### 1. Export a Google Sheets

**Botón:** "📊 Sheets" en resultados

**Qué hace:**
- Exporta TODAS las evaluaciones
- Genera CSV descargable
- Incluye: nombre, score, recommendation, department, evaluador
- Abre en Excel/Sheets para análisis

**Casos de uso:**
- Auditar evaluaciones
- Análisis de consistencia
- Reportes a stakeholders
- Correlacionar con outcomes

---

### 2. Predicción de Conversión

**Ubicación:** Dashboard tab → Sección "Predicción de Conversión"

**Cómo funciona:**
1. Sistema registra qué candidatos fueron contratados
2. Aprende patrones (qué scores convierten)
3. Predice para nuevos candidatos

**Output:**
```
Score Band Analysis:
├─ 80-100%: 85% conversion rate
├─ 60-79%:  62% conversion rate
├─ 40-59%:  28% conversion rate
└─ 0-39%:   0% conversion rate

Insight: Score 80+ tiene 3.8x mejor probabilidad de hire
```

**Casos de uso:**
- Optimizar screening criteria
- Priorizar candidatos
- Reportar a CEO/finance
- Identificar score threshold óptimo

---

## 🔄 Workflow Example

### Semana 1: Setup & Evals

```
Lunes:
1. Alejandro: Pega JD de Backend Engineer
2. Agrega 15 candidatos
3. Click "Evaluar"
4. 2 minutos: Resultados
5. Exporta a CSV

Martes:
6. María: Tab "Buscador"
7. Pega mismo JD
8. Genera 7 search queries
9. Va a LinkedIn, busca con queries
10. Agrega 20 nuevos candidatos

Miércoles:
11. Carlos: Tab "Dashboard"
12. Ve stats: "Alejandro evaluó 15, María buscó 20"
13. Match score promedio: 68%
14. Identifica: Score 70+ parece buen threshold
```

### Mes 2: Learning & Optimization

```
Después de entrevistas:
1. TA Manager registra outcomes:
   "Juan (score 78) → CONTRATADO"
   "María (score 65) → NO"
   "Carlos (score 82) → CONTRATADO"

2. Dashboard se actualiza:
   "Conversion rate: 62%"
   "Score 80+: 85% hire probability"
   "Score 60-79: 62% hire probability"

3. Equipo ajusta:
   "Enfocar en score 75+ para maximizar ROI"
```

---

## 📱 Multi-usuario Setup

### Cómo funciona

```
Usuario 1: Evalúa en Background
Usuario 2: Busca en Buscador
Usuario 3: Mira Dashboard
Usuario 4: Exporta datos

TODO SIMULTÁNEAMENTE ✓

Base de datos centralizada:
├─ Todas las evals se guardan
├─ Se muestran en dashboard de todos
├─ Sin conflictos ni race conditions
└─ Analytics se actualizan en vivo
```

### Límites

- **Concurrencia:** Sin límite (FastAPI async)
- **Gemini API:** 1,500 requests/día (free tier)
- **Usuarios:** Sin límite
- **Almacenamiento:** SQLite (escalable a PostgreSQL)

---

## 🚀 Deployment

### Opción 1: Render.com (Recomendado)

```bash
# 1. Sube a GitHub
git push origin main

# 2. Ve a https://dashboard.render.com
# 3. Conecta repo
# 4. Agrega GEMINI_API_KEY
# 5. Deploy

# URL pública:
https://sourcing-evaluator.onrender.com
```

### Opción 2: Railway.app

```bash
# 1. Conecta GitHub
# 2. Agrega GEMINI_API_KEY
# 3. Deploy automático

# URL en dashboard
```

### Opción 3: Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=..." > .env
python app.py
```

---

## 📊 Casos de Uso por Rol

### Sourcer/Talent Acquisition

```
Workflow diario:
1. Tab "Buscador": Genera queries
2. Va a LinkedIn, busca
3. Tab "Evaluador": Batch evaluate
4. Exporta resultados
5. Comparte link con hiring manager
```

### Hiring Manager

```
Workflow:
1. Recibe link de eval
2. Lee resultados
3. Ve score + recomendación
4. Prioriza entrevistas basado en score
```

### TA Manager

```
Workflow:
1. Tab "Dashboard": Mira analytics
2. Ve: "Conversión 62%, Score 70+ es buen threshold"
3. Ajusta criteria
4. Export CSV: Audita evaluaciones
5. Reporta a CEO
```

### CEO/Finance

```
Weekly check:
1. Dashboard: "45 evaluaciones, 62% conversion"
2. ROI: "2.5 horas/semana salvadas en screening"
3. Quality: "Match score promedio 68%"
```

---

## 🔧 Technical Details

### Stack

| Layer | Tech |
|-------|------|
| Frontend | HTML5 + CSS + Vanilla JS |
| Backend | FastAPI (Python) |
| Database | SQLite (local) → PostgreSQL (prod) |
| AI | Gemini API (Google) |
| Hosting | Render.com / Railway.app |

### Key Endpoints

```
POST /api/evaluate
  Body: {job_description, candidates[], user_email?, department?}
  Response: {success, results[], evaluation_id, share_token}

POST /api/search-candidates
  Body: {job_description, candidates[]}
  Response: {success, data: {search_queries[], ideal_profile, tips[]}}

GET /api/dashboard/stats
  Response: {total_evals, avg_score, by_user, by_dept, etc}

GET /api/conversion-analytics
  Response: {conversion_rate, by_score_band, insights}

POST /api/export-google-sheets
  Response: {records[], count}

POST /api/candidate-outcome
  Body: {candidate_name, match_score, hired}
  Response: {success, outcome_id}
```

### Database Schema

```sql
evaluations:
  ├─ id, job_description, candidates, results
  ├─ created_at, share_token
  ├─ user_email, department

candidate_searches:
  ├─ id, job_description, search_results
  ├─ created_at, user_email

candidate_outcomes:
  ├─ id, candidate_name, match_score
  ├─ hired, hired_at, evaluation_id, created_at

google_sheets_exports:
  ├─ id, spreadsheet_id, exported_at
  ├─ record_count, user_email
```

---

## 📈 Analytics You Can Extract

### From Dashboard
- Conversion rate by score band
- Evaluator productivity
- Department hiring patterns
- Top performing scores

### From Export CSV
- Candidate pool quality
- Evaluator consistency
- Time to evaluate
- Success correlation with score

### From Predictions
- Optimal score threshold
- Hire probability by profile
- Investment ROI (evals that convert)

---

## 🎓 Best Practices

### For Evaluators
1. Be consistent with criteria
2. Include all required fields
3. Be specific in "profile" field
4. Review red flags carefully

### For TA Managers
1. Check dashboard weekly
2. Register outcomes religiously
3. Share insights with team
4. Adjust criteria based on data

### For Scaling
1. Start with 1-2 evaluators
2. Establish consistent criteria
3. Track outcomes for 2+ months
4. Use predictions to optimize

---

## 🔮 Future Roadmap

### v2.5 (Next)
- [ ] Slack integration
- [ ] Auto-notify top candidates
- [ ] Google Sheets API (real-time sync)

### v3.0
- [ ] ATS integration (Workable/Lever)
- [ ] LinkedIn auto-apply
- [ ] Advanced ML model

### v4.0
- [ ] Autonomous agent (24/7 sourcing)
- [ ] Deep learning for predictions
- [ ] Full pipeline automation

---

## ❓ Troubleshooting

### "API key not working"
```
1. Check GEMINI_API_KEY in .env
2. Go to https://ai.google.dev
3. Generate new key if needed
4. Restart app
```

### "No conversion data showing"
```
Reason: Need to register outcomes first
Solution: 
1. Use /api/candidate-outcome to log hires
2. Wait 2+ weeks for data
3. Then predictions appear
```

### "Dashboard slow"
```
Reason: Too much data in SQLite
Solution:
1. Archive old data
2. Upgrade to PostgreSQL
3. Add indexes
```

---

## 📞 Support

**Questions?**
- Email: alexmm930@gmail.com
- Docs: README.md | FEATURES.md | ADVANCED_FEATURES.md

**Issues?**
- GitHub Issues (if public)
- Slack (if internal)

---

## 📋 Checklist: Launch

- [ ] Get Gemini API key
- [ ] Deploy to Render/Railway
- [ ] Test health endpoint
- [ ] Run test_features.py
- [ ] Invite team to URL
- [ ] Start evaluating
- [ ] Register outcomes (Week 2+)
- [ ] Check dashboard (Week 3+)
- [ ] Optimize based on predictions (Month 2+)

---

**Version:** 2.1 (Complete)  
**Last Updated:** 2026-08-23  
**Status:** Production Ready ✅  

**Created for:** Mambu Talent Acquisition  
**By:** Alejandro Mariana Muñoz  
**Email:** alexmm930@gmail.com  
