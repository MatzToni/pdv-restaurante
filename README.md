# 🍽️ PDV Restaurante (Punto de Venta)

Sistema moderno de Punto de Venta diseñado para restaurantes, bares y cafeterías. Optimizado para pantallas táctiles de PC en caja y dispositivos móviles (tablets y smartphones) para meseros y cocina.

---

## 🚀 Arquitectura y Tecnologías

* **Frontend:** [Vue 3](https://vuejs.org/) + [Vite](https://vitejs.dev/) + [Tailwind CSS](https://tailwindcss.com/) + [Pinia](https://pinia.vuejs.org/) + [Vue Router](https://router.vuejs.org/).
* **Backend:** [Python FastAPI](https://fastapi.tiangolo.com/) + Uvicorn + WebSockets.
* **Base de Datos:** [PostgreSQL](https://www.postgresql.org/) con SQLAlchemy ORM.
* **Contenedores:** [Docker](https://www.docker.com/) y Docker Compose.

---

## 📂 Estructura del Proyecto

```text
PDV/
├── backend/                  # Servidor de API (FastAPI)
│   ├── app/
│   │   ├── api/v1/          # Endpoints de la API
│   │   ├── core/            # Configuraciones y seguridad
│   │   ├── db/              # Modelos y conexión de base de datos
│   │   └── main.py          # Punto de entrada de FastAPI
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Interfaz de usuario (Vue 3)
│   ├── src/
│   │   ├── views/           # Mesas, Comandero (POS), Cocina (KDS), Caja
│   │   ├── router/          # Enrutamiento de vistas
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── .env.example              # Plantilla de variables de entorno
├── docker-compose.yml        # Orquestación de servicios
└── README.md
```

---

## ⚙️ Puesta en Marcha

### Opción A: Con Docker (Recomendado)

1. Duplica el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```

2. Construye y levanta los servicios:
   ```bash
   docker compose up -d --build
   ```

3. Acceso a los servicios:
   * **Frontend (PDV Web):** `http://localhost:5173` (o la IP de red local para tablets)
   * **Backend API & Swagger Docs:** `http://localhost:8000/api/v1/docs`

---

### Opción B: Ejecución en Desarrollo Local

#### 1. Backend (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

---

## 📱 Acceso desde Tablets y Celulares en Red Local

Para que los meseros tomen pedidos desde sus teléfonos/tablets en la misma red Wi-Fi:
1. Averigua la dirección IP local de la computadora servidora (ejemplo: `192.168.1.50`).
2. Desde el navegador del teléfono, ingresa a: `http://192.168.1.50:5173`.
