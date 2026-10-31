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

## 📱 Acceso desde Tablets (iPad) y Celulares en Red Local (LAN)

El sistema está optimizado para su uso en computadoras fijas en caja y dispositivos móviles (tablets iPad/Android o teléfonos inteligentes) para meseros y pantallas de cocina KDS dentro de la misma red local (Wi-Fi o cable Ethernet).

### 🚀 Conexión Rápida (Entorno Windows con WSL2)

Cuando el servidor corre sobre Windows con Docker en WSL2, Windows aísla internamente los puertos del sistema virtual. Para permitir que dispositivos externos (como un iPad) se conecten:

1. **Ejecutar el script de habilitación (1 Clic):**
   * En Windows, haz doble clic en `scripts/habilitar_lan.bat` (o el acceso directo en el Escritorio: `Habilitar_iPad_PDV.bat`).
   * El script solicita permisos de Administrador y automáticamente:
     * Detecta la IP interna actual de WSL2 (`wsl hostname -I`).
     * Reenvía los puertos `5173` (Frontend) y `8000` (Backend API).
     * Abre las reglas de entrada correspondientes en el Firewall de Windows.
     * Muestra la dirección IP local a la que debes ingresar.

2. **Abrir en tu iPad o Tablet:**
   * Conecta tu iPad a la misma red Wi-Fi del módem/router.
   * Abre Safari o Chrome e ingresa a:
     ```text
     http://<IP_DE_TU_PC>:5173
     ```
     *(Ejemplo: `http://192.168.1.98:5173`)*

3. **Experiencia de App Nativa a Pantalla Completa en iPad:**
   * En Safari, presiona el botón **Compartir** (icono de cuadrado con flecha hacia arriba) y selecciona **"Agregar a pantalla de inicio"**.
   * Se creará un acceso directo con el icono de Edén Café que abrirá el comandero a pantalla completa sin barra de navegación del navegador.

---

## 👥 Cuentas de Demostración y Roles Preconfigurados

| Colaborador | Rol | PIN de Acceso | Vistas Permitidas |
| :--- | :---: | :---: | :--- |
| **Carlos López** | `mesero` | **`7777`** | Mesas, Comandero Táctil |
| **Ana Gómez** | `mesero` | **`5556`** | Mesas, Comandero Táctil |
| **Chef Roberto Martínez** | `cocina` | **`4444`** | Pantalla Cocina y Barra (KDS) |
| **Valeria Mendoza** | `gerente` | **`2222`** | Todos los módulos + Cortes de Caja |
| **Administrador Edén** | `administrador` | **`1111`** | Control Total del Sistema |

---

## 📖 Carta Digital Pública para Clientes

Los clientes pueden consultar el menú y platillos con fotos y precios escaneando el código QR de su mesa o accediendo directamente a:
```text
http://<IP_DE_TU_PC>:5173/carta
```
*(Esta vista pública es independiente y no requiere inicio de sesión de personal).*
