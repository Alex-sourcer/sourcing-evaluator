# 🚀 Advanced Features - Sourcing Evaluator Agent

## Tabla de Contenidos

1. [Export a Google Sheets](#export-google-sheets)
2. [Predicción de Conversión](#predicción-de-conversión)
3. [Casos de Uso](#casos-de-uso)
4. [Analytics & ROI](#analytics--roi)

---

## 📊 Export a Google Sheets

### Qué es

Un botón que exporta **TODAS** las evaluaciones a una hoja de cálculo descargable. Incluye:

```
| Candidate Name | Match Score | Recommendation | Technical Fit | Department | Evaluated By | Date |
|---|---|---|---|---|---|---|
| Juan García | 78 | YES | Strong Python/Django skills | Backend | alejandro@mambu | 2026-08-23 |
| María López | 65 | MAYBE | Good skills, no team lead exp | Backend | maria@mambu | 2026-08-23 |
```

### Cómo funciona

1. **En la app**, resultados de evaluación → botón **"📊 Sheets"**
2. **Automáticamente genera CSV** con todos los datos
3. **Descarga se inicia** en tu computadora
4. **Abres en Excel/Sheets** y compartes con tu equipo

### Features

✅ Exporta TODAS las evaluaciones del sistema  
✅ Incluye: nombre, score, recomendación, departamento, evaluador  
✅ Un click → Descarga automática  
✅ Compatible con Excel y Google Sheets  
✅ Puedes hacer pivot tables, análisis, gráficos  

### Ejemplo Real

```
Scenario: Necesitas auditar evaluaciones de la última semana

1. Abres app → Tab Dashboard
2. Ves: "45 evaluaciones totales"
3. Click: "📊 Sheets"
4. ↓ Descarga: sourcing-evaluator-2026-08-23.csv
5. Abres en Excel/Sheets
6. Ves todas las evals con todos los detalles
7. Puedes filtrar por departamento, usuario, score
8. Haces análisis (promedio score, distribución, etc)
```

### Casos de Uso

**TA Manager**
```
"Necesito ver si las evaluaciones son consistentes"
→ Export CSV
→ Análisis en Sheets
→ Identifica: Juan promedia 75%, María promedia 62%
→ Ajusta criterios
```

**Gerente de Producto**
```
"¿Cuántas horas invierte el equipo de TA en screening?"
→ Export CSV
→ Cuenta: 200 evaluaciones/mes
→ 30 minutos por 10 candidatos = 5-10 horas/mes salvadas
→ ROI visible
```

**Legal/Compliance**
```
"Necesitamos auditar que el scoring fue justo"
→ Export CSV
→ Verifica: Todos los backend engineers evaluados con criterios similares
→ Comprueba no hay bias
```

---

## 🎯 Predicción de Conversión

### Qué es

Un **modelo predictivo** que aprende:
- Qué scores de matching **realmente** llevan a contratar
- Patrón: "Si el score es 75+, 60% de chance de hire"
- Patrón: "Si el score es 40-60, solo 20% de chance"

### Cómo funciona

#### Paso 1: Registrar Outcomes (Manual - por ahora)
```
El equipo de TA marca después de entrevistas/hired:
"Juan García (score 78) → CONTRATADO ✓"
"María López (score 65) → NO CONTRATADO ✗"
```

#### Paso 2: El sistema analiza
```
¿Qué tienen en común los contratados vs no contratados?

Contratados:
├─ Score promedio: 76%
├─ Strong YES: 45%
└─ Match profile: Sí, 90%

No Contratados:
├─ Score promedio: 58%
├─ Strong YES: 5%
└─ Match profile: Parcial, 40%
```

#### Paso 3: Predicción
```
Cuando ves nuevo candidato con score 80%:
"Este candidato tiene 85% de probabilidad de ser contratado"

Cuando ves score 45%:
"Este candidato tiene solo 15% de probabilidad"
```

### En el Dashboard

**Sección: "Predicción de Conversión"**

```
┌─────────────────────────────────────┐
│ Conversion Rate: 62%                │
│ Contratados: 45                     │
│ Evaluados: 73                       │
└─────────────────────────────────────┘

Score Band Analysis:
├─ 80-100%: 85% conversion rate (15/18 hired) ⭐⭐⭐
├─ 60-79%:  62% conversion rate (28/45 hired) ⭐⭐
├─ 40-59%:  28% conversion rate (2/8 hired)   ⭐
└─ 0-39%:   0% conversion rate (0/2 hired)    

💡 Insight: Candidatos con score 80+ tienen 3.8x
            mayor probabilidad de ser contratados
```

### Features

✅ Análisis automático de conversión  
✅ Predicción por score band  
✅ Identificar threshold de hiring  
✅ Insights actionables  
✅ Optimizar screening criteria  

### Ejemplo: Cómo funciona el aprendizaje

**Mes 1: Datos iniciales**
```
Usuario evalúa 50 candidatos
├─ 20 con score 70+
├─ 20 con score 50-70
└─ 10 con score <50

Pero aún no sabemos outcomes (si fueron contratados)
```

**Mes 2: Empiezas a registrar outcomes**
```
De los 50 del mes 1:
├─ Score 70+: 16 contratados / 20 evaluados = 80%
├─ Score 50-70: 8 contratados / 20 evaluados = 40%
└─ Score <50: 1 contratado / 10 evaluados = 10%

El sistema aprende: "Score 70+ es predictor fuerte"
```

**Mes 3 en adelante: Predicciones mejoran**
```
Nuevo candidato: score 75%
Sistema dice: "Predicción: 70% de hire probability"
(Basado en histórico: candidatos 70-79 tienen 70% conversion)
```

---

## 📈 Dashboard Conversion Analytics

### KPI Cards

| Métrica | Qué significa | Objetivo |
|---------|---------------|----------|
| **Conversion Rate** | % de evaluados que fueron contratados | >60% |
| **Contratados** | Número absoluto de hires | Crecer mes a mes |
| **Evaluados** | Evaluaciones totales | Indicador de volumen |

### Score Band Analysis

```
┌──────────────┬──────────────┬──────────────┐
│ 80-100%      │ 60-79%       │ <60%         │
├──────────────┼──────────────┼──────────────┤
│ 85% hire     │ 62% hire     │ 15% hire     │
│ 15/18 hired  │ 28/45 hired  │ 3/20 hired   │
└──────────────┴──────────────┴──────────────┘
```

**¿Qué hacer con esto?**

```
Si 80-100% score = 85% hire rate:
✓ Enfócate en candidatos en este band
✓ No pierdas tiempo con <60%

Si 60-79% = 62% hire rate:
✓ Estas son grises, necesitan más evaluación
✓ Entrevista antes de descartar
```

---

## 🎓 Casos de Uso Reales

### Caso 1: Optimizar Screening

**Situación:** Tu equipo de TA evalúa 100 candidatos/mes, pero contrata solo 30

**Acción:**
1. Abre Dashboard → Mira score bands
2. Ve: "Candidatos con score <60% casi nunca se contratan (5%)"
3. Decisión: **Filtro automático a score >60%**
4. Resultado: Ahorras tiempo, misma calidad

**ROI:**
```
Antes: 100 evaluaciones/mes
Después: 70 evaluaciones/mes (sin los <60%)
Ahorro: 30 evaluaciones × 5 minutos = 2.5 horas/mes
```

### Caso 2: Benchmarking de evaluadores

**Situación:** Diferentes miembros del equipo evalúan de forma inconsistente

**Acción:**
1. Ver en Dashboard: "Alejandro: conversión 68%, María: 55%"
2. Investigar: ¿Alejandro es más selectivo? ¿O mejor screening?
3. Si es mejor: Aprender de su método
4. Si es más selectivo: Ajustar criterios para consistencia

### Caso 3: Ajustar JD (Job Description)

**Situación:** Contratas muchos "mediocres" (score 50-60) que no funcionan

**Acción:**
1. Mira Dashboard: "Score 50-60: 30% hire rate"
2. Análisis: Estos candidatos pasaban evaluación pero fracasaban
3. Decisión: Cambiar JD para ser más específico
4. Resultado: Próximos candidatos en 50-60 tendrán mejores chances

### Caso 4: Reportar a Stakeholders

**Presentación a CEO:**
```
"Nuestro sistema de screening tiene 62% conversion rate.
El modelo predice que candidatos con score 80+
tienen 85% de probabilidad de ser contratados.

Estrategia: Enfocarnos en candidatos 75+ para maximizar ROI"
```

---

## 🔄 Workflow Completo

### Semana 1-2: Setup

```
1. Equipo empieza a evaluar con Sourcing Evaluator
   └─ Genera datos de screening

2. Después de entrevistas, TA manager registra outcomes
   "Juan (score 78) → Contratado"
   └─ Empieza feedback loop
```

### Semana 3-4: Primeros insights

```
1. Dashboard muestra patrones iniciales
   "Conversión: 60%"
   "Score 70+: 70% hire rate"

2. Equipo ajusta si es necesario
   "Parece que score 70+ es buen threshold"
```

### Mes 2 en adelante: Predicción efectiva

```
1. Nuevo candidato: score 75%
   Sistema predice: "70% conversion probability"
   
2. Puedes:
   ✓ Priorizar estos candidatos
   ✓ Invertir más en entrevista
   ✓ Esperar menos conversión de score <60%
   
3. Dashboard se mejora constantemente con new data
```

---

## 📊 Métricas Clave

### Para Track

| Métrica | Frecuencia | Acción |
|---------|-----------|--------|
| Conversion Rate | Semanal | Detectar cambios |
| Score Distribution | Mensual | Ver patrón de evaluaciones |
| Evaluations/User | Mensual | Identificar usuarios inactivos |
| Prediction Accuracy | Mensual | ¿Tus predicciones son correctas? |

### Objetivos Típicos

```
Pequeña startup (5 TA hires/mes):
├─ Conversión target: 50-60%
├─ Score promedio: 65%
└─ Evaluations/hire: 12-15

Mediana empresa (30+ TA hires/mes):
├─ Conversión target: 60-70%
├─ Score promedio: 70%
└─ Evaluations/hire: 8-10

Enterprise (100+ TA hires/mes):
├─ Conversión target: 70%+
├─ Score promedio: 75%
└─ Evaluations/hire: 5-8
```

---

## 🚨 Limitations & Considerations

### Conversión tracking es MANUAL (por ahora)

```
Alguien debe decir "Esta persona fue contratada"
No es automático desde LinkedIn/ATS

Solución futuro: Integración con Workable/Lever
```

### Correlación ≠ Causación

```
Si tu conversion rate es bajo:
❌ No significa que tu scoring es malo
✓ Puede ser: mercado, JD, competencia, etc

Usa dashboard como GUÍA, no como verdad absoluta
```

### Necesitas histórico de outcomes

```
Primera semana: No hay suficiente data
Primera mes: Datos iniciales
Después de 2 meses: Predicciones útiles
```

---

## 🔮 Future Roadmap

### Próximas versiones

```
v2.5: Outcome tracking automático
      └─ API connection a ATS

v3.0: Machine learning model
      └─ Predicciones más precisas

v3.5: Integración Slack
      └─ "Este candidato tiene 80% chance de hire"

v4.0: Agente autónomo
      └─ Busca + evalúa + predice 24/7
```

---

## 💡 Pro Tips

### Para maximizar valor

1. **Sé consistente con scoring**
   - Todos usan los mismos criterios
   - Dashboard muestra si hay drift

2. **Registra outcomes religiosamente**
   - Sin outcomes, sin predicciones
   - Takes 10 seconds por candidato

3. **Revisa dashboard mensualmente**
   - Identifica trends early
   - Ajusta estrategia

4. **Usa predicciones para priorizar**
   - Score 80+? Entrevista rápido
   - Score <50? Skip (estadísticamente)

5. **Comparte insights con hiring managers**
   - "Este perfil tiene 75% de chance"
   - Ayuda en decision making

---

## 📞 Questions?

Si tienes dudas sobre cómo usar estas features:
- Email: alexmm930@gmail.com
- Check: FEATURES.md (basic features)
- Check: README.md (general docs)

---

**Version**: 2.1  
**Last Updated**: 2026-08-23  
**Status**: Production Ready ✅

---

## Quick Reference

| Feature | Where | What | Why |
|---------|-------|------|-----|
| **Export Sheets** | Results tab | Button "📊 Sheets" | Audit & analysis |
| **Conversion Analytics** | Dashboard tab | Section "Predicción de Conversión" | Optimize screening |
| **Prediction** | Dashboard tab | Score bands + insights | Data-driven decisions |
| **Outcome Tracking** | (Manual entry) | When someone is hired | Train the model |
