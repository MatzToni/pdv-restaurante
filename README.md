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
│   ├── public/              # Assets estáticos y manifiesto PWA
│   │   ├── logo.png         # Icono corporativo
│   │   └── manifest.json    # Manifiesto PWA (Modo Standalone, colores)
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

## 📱 Acceso e Instalación en Tablets (iPad / Android) y Celulares

El sistema está desarrollado con arquitectura **PWA (Progressive Web App)** y diseño **Mobile-First / Touch-Friendly**, optimizado para ejecutarse en computadoras fijas en caja y dispositivos móviles de meseros o pantallas de cocina (KDS) en la red local (LAN).

### ⚙️ Arquitectura PWA Integrada
* **Manifiesto Web (`frontend/public/manifest.json`):** Configurado con el esquema oficial de Edén Café (tema verde bosque `#486848`, orientación responsiva y modo `standalone`).
* **Soporte Nativo iOS/iPadOS (`frontend/index.html`):** Metaetiquetas de pantalla completa (`apple-mobile-web-app-capable`), barra de estado translúcida (`apple-mobile-web-app-status-bar-style`), icono corporativo (`apple-touch-icon`) y ajuste seguro de pantalla (`viewport-fit=cover`).
* **Optimización de Caché (`frontend/nginx.conf`):** Reglas para que los cambios en el manifiesto, icono y HTML se actualicen sin requerir borrado manual de caché en los dispositivos.

---

### 🚀 Conexión en Red Local (Windows + Docker en WSL2)

Cuando el servidor opera sobre Windows con Docker en WSL2, Windows aísla internamente los puertos del subsistema virtual. Para habilitar el acceso a dispositivos en la misma red Wi-Fi:

1. **Habilitar acceso con 1 Clic:**
   * En Windows, haz doble clic en `scripts/habilitar_lan.bat` (o en el acceso directo del Escritorio: `Habilitar_iPad_PDV.bat`).
   * El script solicita permisos de Administrador y automáticamente:
     * Detecta la IP interna actual de WSL2 (`wsl hostname -I`).
     * Configura el reenvío de puertos `5173` (Frontend) y `8000` (Backend API).
     * Habilita las reglas de entrada en el Firewall de Windows.
     * Muestra en pantalla la dirección IP local de tu PC (ejemplo: `192.168.1.98`).

2. **Conectar el iPad o Tablet:**
   * Asegúrate de que el dispositivo esté conectado a la misma red Wi-Fi que la computadora.
   * Abre el navegador y visita:
     ```text
     http://<IP_DE_TU_PC>:5173
     ```
     *(Ejemplo: `http://192.168.1.98:5173`)*

---

### 📲 Instalación como App Nativa (Sin App Store)

#### En iPad / iPhone (Safari):
1. Abre la URL en **Safari**.
2. Presiona el botón **Compartir** (icono de cuadrado con flecha hacia arriba ⬆️).
3. Selecciona la opción **"Agregar a pantalla de inicio"** (*Add to Home Screen*).
4. Confirma el nombre **"Edén Café"** y pulsa **Agregar**.
5. Abre la aplicación desde el icono nuevo en la pantalla de inicio: se ejecutará a pantalla completa, con icono corporativo y sin barras de navegación de Safari.

#### En Tablets / Celulares Android (Chrome):
1. Abre la URL en **Google Chrome**.
2. Presiona el botón de menú (tres puntos verticales `⋮`) en la esquina superior derecha.
3. Toca en **"Instalar aplicación"** o **"Agregar a la pantalla principal"**.
4. Pulsa **Instalar**. La app quedará integrada en el cajón de aplicaciones de Android.

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
