# Cómo Actualizar la API Key de Gemini en Render

## Pasos Rápidos:

### 1. Ir al Dashboard de Render
https://dashboard.render.com

### 2. Autenticarse con GitHub
- Click en "GitHub"
- Ingresar credenciales de GitHub
- Autorizar Render

### 3. Encontrar el Servicio
- En el dashboard, buscar "sourcing-evaluator"
- Click para entrar en el servicio

### 4. Ir a Environment Variables
- En el menú lateral, click en "Environment"
- O click en la pestaña "Environment"

### 5. Actualizar GEMINI_API_KEY
- Buscar la variable `GEMINI_API_KEY`
- Reemplazar el valor actual con tu API key (obtén una en https://ai.google.dev)
- Click en "Save"

### 6. Redesplegue
- Render automáticamente redesplegará el servicio
- Esperar 1-2 minutos para que se actualice
- Verificar en la página: el indicador de estado debería pasar de "Deploying" a "Live"

### 7. Probar
- Ir a: https://sourcing-evaluator-1.onrender.com
- Rellenar el formulario y hacer click en "Evaluate Candidates"
- Debería funcionar ahora

## Verificación
Si ves este error en la consola: `"API key not valid. Please pass a valid API key."`
- Significa que la API key aún no se ha actualizado
- Espera unos minutos y recarga la página
- O verifica que la API key esté correcta en Render

## Nota de Seguridad
- NUNCA compartir la API key en repositorios públicos
- NUNCA poner la API key en comentarios o código
- Siempre usar variables de entorno en plataformas de hosting
