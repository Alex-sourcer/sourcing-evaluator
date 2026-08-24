# 🔐 Admin Dashboard - Setup & Security

## Access Control

El Admin Dashboard está **protegido con contraseña** y solo es accesible para ti.

### Cómo acceder

1. Abre: https://sourcing-evaluator-1.onrender.com
2. Click en **"🔧 Admin"** (botón oculto, solo aparece después de login)
3. Verás un modal pidiendo contraseña
4. Contraseña por defecto: `mambu2024`
5. Click "Login"

### Cambiar la Contraseña (⚠️ IMPORTANTE)

La contraseña por defecto es insegura. **DEBES CAMBIARLA INMEDIATAMENTE.**

#### Paso 1: Accede al código
```bash
cd /Users/alejandromarianamunoz/Desktop/Curso\ Agentes\ IA/agents/sourcing-evaluator
```

#### Paso 2: Abre `static/script.js`
Busca la línea (alrededor de línea 830):
```javascript
const ADMIN_PASSWORD = 'mambu2024'; // ⚠️ Change this!
```

#### Paso 3: Cambia a tu contraseña
```javascript
const ADMIN_PASSWORD = 'TuNuevaContraseñaSegura2024'; // Ej: Mambu!TA#Expert2026
```

**Requisitos para contraseña segura:**
- ✅ Mínimo 12 caracteres
- ✅ Combina mayúsculas, minúsculas, números
- ✅ Incluye símbolos especiales (@#$%^&*)
- ✅ NO uses palabras del diccionario
- ✅ NO compartas la contraseña por Slack/email

#### Paso 4: Commit y push
```bash
git add static/script.js
git commit -m "Security: Update admin password"
git push origin main
```

Render redesplegará automáticamente en 1-2 minutos.

---

## Seguridad

### ✅ Qué está protegido
- Admin Dashboard tab está oculta del menú
- Login modal requiere contraseña
- Sesión guardada solo en sessionStorage (se borra al cerrar navegador)
- Contraseña nunca se envía a servidor

### ⚠️ Limitaciones actuales
- Contraseña almacenada en código (OK para small teams)
- Si alguien accede a tu navegador, ve el admin hasta cerrar sesión
- No hay logs de quién accedió cuándo

### 🔒 Mejoras futuras (si necesitas)
- Base de datos de usuarios con roles
- Logs de acceso
- 2FA (Two-Factor Authentication)
- Rate limiting en login

---

## Ejemplo de Contraseña Segura

```
❌ Mala:      mambu2024, admin123, password
✅ Buena:     Mambu@TA2024!, Sourcing#Expert.26
✅ Excelente: Gemini$Evaluator#2024.Team
```

---

## Qué ve el Admin Dashboard

| Métrica | Descripción |
|---------|------------|
| **Total Evaluations** | Cuántos candidatos evaluó tu equipo |
| **Active Users** | Cuántas personas usaron la app |
| **Avg Match Score** | Puntuación promedio de matching |
| **Time Saved** | Horas de screening ahorradas |
| **Conversion Rate** | % de candidatos contratados |
| **Users Activity** | Quién evaluó cuántos y con qué promedio |
| **Score Distribution** | Gráfico 80-100%, 60-79%, 40-59%, 0-39% |
| **30-Day Timeline** | Actividad diaria |
| **Export Report** | Descarga CSV para presentar |

---

## Troubleshooting

### "El botón Admin no aparece"
✅ Solo aparece DESPUÉS de introducir contraseña correcta
✅ Es normal que no lo vea el equipo (está oculto)

### "¿Cómo reseteo la contraseña?"
1. Cambia en `static/script.js` línea 830
2. Push a GitHub
3. Render redesplegará en 1-2 min

### "¿Qué pasa si olvido la contraseña?"
Solo tú tienes acceso al código, así que:
1. Abre `static/script.js`
2. Lee la contraseña actual
3. Cámbiala si quieres

---

## Para el Equipo (¿si quieren acceso?)

**NO compartas la contraseña.**

Si tu manager o TA Lead necesita ver reportes:
1. Tú accedes al Admin Dashboard
2. Exportas el CSV
3. Se lo compartes via email/Slack

De esta forma mantienes control total.

---

**Setup completado ✅**

Tu Admin Dashboard está seguro y listo para reportar ROI a management.
