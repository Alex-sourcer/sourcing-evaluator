# 🎯 Mambu Career Framework Integration - Quick Guide

## ¿Qué cambió?

La herramienta ahora evalúa candidatos **contra el Mambu Career Framework** además del Job Description.

### Antes:
```
IA evalúa: "Match Score: 78%, recommendation: YES"
Problem: ¿Pero en qué Level es? ¿IC o TL?
```

### Ahora:
```
IA evalúa: 
- Match Score: 78%
- Mambu Level: 4 (Senior)
- Career Path: IC (Individual Contributor)
- Growth: "Can reach Level 5 in 12-18 months"
```

---

## 🔍 Cómo Funciona

### Mambu Levels (0-8)

| Level | Title | Description |
|-------|-------|-------------|
| **8** | Intern/Entry | Entry-level, learning phase |
| **7** | Associate | Developing independence |
| **6** | Intermediate | Solid technical competency |
| **5** | Experienced | Expert-level skills |
| **4** | Senior | Mastery, drives decisions, mentors |
| **3** | Advanced Senior | Domain expert, technical strategy |
| **2** | Fellow/Director/VP | Strategic leadership |
| **1** | LT | Leadership Team |
| **0** | CEO | Chief Executive Officer |

### Career Paths

- **IC (Individual Contributor)**: Technical leadership, deep expertise path
- **TL (Team Leader)**: People management, organizational leadership path

---

## 📊 Nuevo Output de Evaluación

Cuando evalúas candidatos, ahora ves:

```json
{
  "candidate_name": "Carlos García",
  "match_score": 85,
  "recommendation": "STRONG YES",
  "mambu_level_fit": 4,
  "mambu_career_path": "IC",
  "mambu_level_description": "Expert-level technical skills. Drives architecture decisions. Cross-functional impact. Mentors team members.",
  "growth_potential": "Can reach Level 5 (Advanced Senior) in 12-18 months",
  "strengths": [...],
  "reasoning": "..."
}
```

---

## 🧪 Testing (Esta Semana)

### Test 1: Senior IC
```
Job: "Senior Backend Engineer, Python/FastAPI, 5+ years, leads team"
Candidate: "6 years Python, AWS expert, led team of 4"

Expected Result:
- Level: 4 (Senior) ✅
- Path: IC ✅
- Growth: "Level 5 in 12-18 months" ✅
```

### Test 2: Junior with Growth Potential
```
Job: "Intermediate Python Developer, 2-3 years"
Candidate: "2 years Python, strong fundamentals, learning Docker"

Expected Result:
- Level: 6 (Intermediate) ✅
- Path: IC ✅
- Growth: "Level 5 in 18-24 months" ✅
```

### Test 3: Senior with Wrong Path
```
Job: "Senior Backend Engineer (IC focused)"
Candidate: "8 years backend, great at team management, no hands-on recently"

Expected Result:
- Level: 3-4 ✅
- Path: TL (not IC) ✅
- Note: "Better suited for Manager role than IC" ✅
```

---

## 📈 Impact for Mambu TA

### Para Contratación
```
ANTES:
- "Contratamos Senior Engineers"
- Cost prediction: Unknown (Level 4 = €90k, Level 5 = €150k)

AHORA:
- "Contratamos Level 4 ICs"
- Cost prediction: Precise (aligned with Mambu salary bands)
- Career path: Clear (IC vs TL)
```

### Para Desarrollo
```
ANTES:
- Growth plans: Unclear
- Career path: Subjective

AHORA:
- Growth plans: "Reach Level 5 in 18 months" (data-driven)
- Career path: Validated by IA (IC vs TL)
```

### Para Reportes
```
ANTES:
- "Hired 5 senior engineers"

AHORA:
- "Hired 1 Level 5 IC, 3 Level 4 ICs, 1 Level 3 TL"
- Conversion rates by level visible in Admin Dashboard
- Predictive: "Level 5 candidates: 85% conversion rate"
```

---

## 🚀 Próximos Pasos (No Urgente)

### Fase 2 (Si agrega valor):
- [ ] Selector en UI: "¿Qué Level buscas?" (4, 5, 6...)
- [ ] Selector: "¿IC o TL?"
- [ ] Admin Dashboard: Analytics por Level
- [ ] Predicción: "Level 5 candidates: 85% conversion"

### Fase 3 (Versión avanzada):
- [ ] Import multiple frameworks (no solo Mambu)
- [ ] Custom levels por empresa
- [ ] Multi-language support

---

## ⚠️ Important Notes

### What This Is:
✅ Framework-aware evaluation  
✅ Aligned with Mambu's leveling system  
✅ Growth potential estimation  
✅ IC vs TL path detection

### What This Is NOT:
❌ Replacement for human judgment  
❌ Final hiring decision  
❌ Compensation calculation (use HR salary bands)  
❌ Performance evaluation (for active employees)

---

## 📝 Feedback Loop

**This week:**
1. Evaluate 20+ candidates with new framework
2. See if Mambu Level assessment is accurate
3. Ask hiring managers: "Does the IC/TL assessment match your needs?"
4. Collect data: Which levels convert to hires?

**If helpful:** Invest in UI improvements next month  
**If not:** Keep simple, works fine

---

## 🎯 The Value Proposition

**For You (TA Manager):**
> "I now speak Mambu's language. When I say 'this candidate is Level 4 IC', everyone understands exactly what that means."

**For Hiring Managers:**
> "Clear, consistent evaluation. No more 'Senior means different things in different places'."

**For Mambu Finance:**
> "Predictable costs and career progression aligned with organizational structure."

---

## 📞 Questions?

If the evaluation seems off:
1. Check if the candidate profile is detailed enough
2. Verify the job description mentions expected level
3. Test with a candidate you know well (calibration)

---

**Status:** ✅ Live in production (Render redeploys in 1-2 min)  
**Testing:** Start this week with 1-2 positions  
**Decision:** Mid-month (expand or keep simple?)
