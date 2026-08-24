# 🎯 Características - Sourcing Evaluator Agent

## Versión 2.0 - Con Agentic Features

### 📋 Overview

Tu app ahora es un **agente inteligente** con 3 módulos principales:

1. **Evaluador de Candidatos** - Evaluaciones IA
2. **Buscador de Candidatos** - Auto-search en LinkedIn
3. **Dashboard Analytics** - Insights en tiempo real

---

## 🔄 Tab 1: Evaluador de Candidatos

### Features
✅ Pega job description  
✅ Agrega múltiples candidatos (nombre, perfil, LinkedIn)  
✅ IA evalúa automáticamente (Gemini)  
✅ Resultados con:
  - Match Score (0-100%)
  - Technical Fit (resumen)
  - Fortalezas (lista)
  - Red Flags (lista)
  - Interview Questions (preguntas generadas)
  - Recomendación (STRONG YES / YES / MAYBE / NO)
  - Reasoning (explicación)

✅ Exportar a CSV  
✅ Compartir link público  
✅ Historial guardado automáticamente  

### Multi-usuario
- Múltiples personas evalúan **simultáneamente**
- Sin conflictos de datos
- Cada evaluación se guarda con email del usuario
- Base de datos centralizada

---

## 🔍 Tab 2: Buscador de Candidatos (NUEVO)

### Propósito
Genera **LinkedIn search queries automáticamente** basadas en job description.

### Cómo funciona
1. Pegas job description
2. IA analiza y genera:
   - **5-7 search queries optimizadas** para LinkedIn
   - **Descripción del candidato ideal** (perfil)
   - **Tips de búsqueda** (cómo encontrarlos)

### Ejemplo

**Input:**
```
Senior Backend Engineer (Python)
- 5+ años Python/Django
- PostgreSQL, Redis
- AWS, Docker
```

**Output:**
```
Search Queries:
├─ "Python Django FastAPI engineer -junior -senior"
├─ "AWS PostgreSQL Redis backend developer"
├─ "Backend engineer startup scaling experience"
├─ "Technical lead Python 5 years+"
└─ ...

Tips:
├─ Busca en España + Europa
├─ Filtra por "Open to Work"
├─ Revisa recomendaciones de skills
└─ ...

Ideal Profile:
"Ingeniero de backend sénior con 5+ años de experiencia en Python 
(Django, FastAPI), con sólida experiencia en PostgreSQL, Redis y AWS..."
```

### Click to Copy
- Click en cualquier query → se copia automáticamente
- Luego va directamente a LinkedIn y pega

### Casos de uso
- Sourcing rápido por JD
- Generar múltiples search angles
- A/B testing de queries
- Documentar búsquedas para auditoría

---

## 📊 Tab 3: Dashboard Analytics (NUEVO)

### KPI Cards
- **Evaluaciones Totales**: Todas las evals en el sistema
- **Match Score Promedio**: Promedio de todos los scores
- **Usuario Más Activo**: Quién ha evaluado más
- **Strong YES Recommendations**: Candidatos fuertemente recomendados

### Charts & Analytics

#### 1. Recomendaciones (últimas 100 evals)
```
STRONG YES: ███████ 35
YES:        ████████████ 62
MAYBE:      ████ 18
NO:         ██ 10
```

#### 2. Top Usuarios
Ranking de usuarios por cantidad de evaluaciones
```
alejandro@mambu.com:  45 evals
maria@mambu.com:      38 evals
carlos@mambu.com:     28 evals
...
```

#### 3. Actividad por Día (últimos 30 días)
Gráfico de barras visual mostrando evals/día

#### 4. Evaluaciones por Departamento
```
Backend:       34 evals
Product:       28 evals
UX Design:     19 evals
...
```

### Insights Que Puedes Extraer
- "¿Cuál es mi tasa de recomendación?"
- "¿Quién en el equipo evalúa más?"
- "¿Cuándo somos más activos?"
- "¿Cuál es el match score promedio por tipo de rol?"
- "Tendencias de hiring"

---

## 🔒 Multi-usuario & Seguridad

### Arquitectura
```
Usuario 1  User 2  User 3  User 4
   ↓         ↓       ↓      ↓
   └─────────┴───────┴──────┘
          ↓
     1 URL pública (Render.com)
          ↓
   FastAPI + SQLite Database
          ↓
   Gemini API (1 key compartida)
```

### Características Multi-usuario
✅ Soporte simultáneo (sin límites)  
✅ Cada evaluación registra usuario  
✅ Sin bloqueos ni race conditions  
✅ Historial centralizado  
✅ Analytics compartidas  
✅ Share links con seguridad (tokens aleatorios)  

### Límites
- **Gemini Free**: 1,500 evals/día total
- **Usuarios**: Sin límite
- **Evaluaciones simultáneas**: Sin límite
- **Almacenamiento**: SQLite (escalable)

---

## 📱 Casos de Uso

### Caso 1: Screening rápido
```
Alejandro:
├─ Pega JD
├─ Agrega 10 candidatos
├─ Click "Evaluar"
├─ 2 minutos: Resultados
└─ Exporta CSV
```

### Caso 2: Generación de sourcing lists
```
María:
├─ Ve que necesitan 5 ingenieros Python
├─ Pegas JD en "Buscar Candidatos"
├─ Genera 7 search queries
├─ Va a LinkedIn con queries
└─ Empieza inreach
```

### Caso 3: Análisis de calidad
```
Gerente de TA:
├─ Abre Dashboard
├─ Ve: "Strong Yes = 35% de evaluaciones"
├─ Nota: "Alejandro tiene 45 evals, María 38"
├─ Identifica: "El match score promedio es 68%"
└─ Ajusta estrategia
```

### Caso 4: Auditoría de hiring
```
Legal/Compliance:
├─ Ve todas las evaluaciones en el sistema
├─ Filtra por departamento
├─ Verifica: "¿Fue consistente el scoring?"
└─ Descarga reportes CSV
```

---

## 🔧 Configuración por Usuario (Opcional)

Puedes agregar en el formulario de evaluación:

```
Email: alejandro@mambu.com
Departamento: Backend Engineering

[Y estas se guardan en el dashboard]
```

Luego ves en dashboard:
```
Backend Engineering: 45 evaluaciones
  └─ alejandro@mambu.com: 45
```

---

## 📈 Roadmap (Futuro)

### Fase 2
- [ ] Slack integration: `/evaluate candidate description`
- [ ] Auto-send de mejores candidatos por Slack
- [ ] Export a Google Sheets
- [ ] Webhook para integración con ATS

### Fase 3
- [ ] Predicción de conversión (qué scores convierten en hiring)
- [ ] Ranking automático de candidatos
- [ ] Integración con LinkedIn API (si es posible)
- [ ] Historial de cada candidato

### Fase 4
- [ ] Agente autónomo que busca + evalúa 24/7
- [ ] Notificaciones cuando encuentra match
- [ ] Integración con Workable/Lever
- [ ] Custom IA models por cliente

---

## 🚀 Deploy & Escalabilidad

### Render.com (Recomendado)
```
git push → Render redeploya automáticamente
├─ Equipo completo accede vía 1 URL
├─ Database persiste entre deploys
├─ 1,500 evals/día (Gemini free)
└─ Gratis indefinidamente
```

### Con 10 usuarios simultáneos
- Todos pueden evaluar al mismo tiempo
- Historial compartido
- Analytics en vivo
- Sin problemas de performance

---

## 💡 Tips para Máximo Impacto

### Para el Sourcer
1. Usa "Buscar Candidatos" para generar queries
2. Copia queries → LinkedIn
3. Guarda candidatos prometedores
4. Usa "Evaluador" para batch assessment
5. Comparte resultados via link

### Para el Hiring Manager
1. Revisa Dashboard para entender pipeline
2. Ve qué usuarios son más efectivos
3. Monitorea Strong YES ratio
4. Identifica patrones de hiring

### Para el CEO/Finance
1. Dashboard muestra ROI del equipo de TA
2. Compara productividad (evals/usuario)
3. Entiende velocidad de hiring
4. Ve tendencias mes a mes

---

## 🎓 Ejemplos de Prompts

### Buscador
**Input:**
```
Product Manager at B2B SaaS
- 5+ años en software
- Experiencia con productos payment/fintech
- User research + Analytics
```

**Output:**
```
Queries:
├─ "Product Manager fintech payment 5 years"
├─ "B2B SaaS product management user research"
├─ "Payment startup product strategy"
├─ "Analytics-driven product manager"
└─ "Fintech product operations Spain EU"

Tips:
├─ Busca en Europe/Remote
├─ Filtra por "Strategy" skill
├─ Revisa LinkedIn recommendations
└─ ...
```

### Evaluador
**Input:**
```
JD: Senior Backend Engineer (Python)
Candidate: Juan García - 5 años Python, Django, PostgreSQL, AWS
```

**Output:**
```
Match Score: 78%
Technical Fit: Strong alignment with core stack (Python/Django/PostgreSQL)
Strengths:
  • 5 años exactos en Python
  • Experiencia comprobada en Django
  • SQL databases (PostgreSQL)
  • AWS cloud platform
Red Flags:
  • No menciona Redis/caching layer
  • No leadership experience stated
Questions:
  • ¿Experiencia liderando equipos?
  • ¿Cómo approach performance optimization?
  • ¿Cambios en última empresa (qué aprendiste)?
Recommendation: YES
Reasoning: Candidato fuerte con skills técnicos, pero verificar leadership potential.
```

---

## 📞 Support & Feedback

¿Problemas o ideas?
- Email: alexmm930@gmail.com
- GitHub: Issues & PRs bienvenidas

---

**Versión**: 2.0  
**Última actualización**: 2026-08-23  
**Status**: Production Ready ✅
