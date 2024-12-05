# Dashboard de Control Escolar TSJ

## Descripción del Problema
La gestión y análisis de datos académicos es una tarea clave en instituciones 
educativas. Sin embargo, la falta de herramientas interactivas y escalables 
complica el análisis y la toma de decisiones basadas en datos. Este proyecto 
propone una solución para centralizar y visualizar datos de matrícula.

## Solución Propuesta
La solución incluye:
- **Backend**: Un API REST con Flask para procesar datos de matrícula 
utilizando principios de programación funcional.
- **Frontend**: Un dashboard interactivo construido con Dash y Plotly.
- **Concurrencia**: Uso de asyncio y aiohttp para realizar múltiples 
solicitudes al backend en paralelo.

## Pasos para Instalar y Ejecutar el Sistema

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/gerardoavila87/TSJ-Dashboard
   cd TSJ-Dashboard

2. **Instalar dependencias**:
- **Backend:**
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

- **Frontend:**
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

- **Ejecutar el backend:**
bash
Copiar código
cd backend
python app.py

- **Ejecutar el frontend:**
bash
Copiar código
cd frontend
python app.py

**Acceder al sistema:**
Backend: http://127.0.0.1:5001
Frontend: http://127.0.0.1:5002

