# 🤖 AGENTS.md — Directrices para Agentes de IA en Edén Café PDV

Este documento define las directrices arquitectónicas, estándares de desarrollo, buenas prácticas de ciberseguridad y flujos de trabajo que **todo agente de IA** (incluyendo Antigravity) debe seguir rigurosamente al colaborar en este proyecto.

---

## 📌 1. Visión del Proyecto
**Edén Café PDV** es un sistema de Punto de Venta moderno diseñado para restaurantes y cafeterías. 
* **Dispositivos Objetivo:** Computadora de caja fija (PC), tablets y teléfonos celulares de meseros (comanderos táctiles), y pantallas digitales de cocina y barra (KDS).
* **Entorno:** Operación inicial en red local (LAN) con capacidad de transición transparente a la nube vía Docker.
* **Identidad de Marca:** "Edén Café - Comida Tradicional y Café". Paleta natural basada en tonos verdes bosque/oliva (`#486848`), interfaces limpias y optimizadas para interacción táctil rápida.

---

## 🏗️ 2. Stack Tecnológico & Arquitectura

| Capa | Tecnología | Lineamientos Clave |
| :--- | :--- | :--- |
| **Frontend** | Vue 3 + Vite + Tailwind CSS + Pinia | Composition API con sintaxis `<script setup>`. Interfaces touch-friendly (botones con altura mínima de 44px para dedos). |
| **Backend** | Python 3.11+ / FastAPI + Uvicorn | Endpoints asíncronos (`async def`). Tipado estricto con **Pydantic v2** para validación de entrada/salida. |
| **Base de Datos** | PostgreSQL 16 + SQLAlchemy 2.0 | Migraciones manejadas con **Alembic**. Consultas estrictamente parametrizadas mediante el ORM. |
| **Tiempo Real** | WebSockets (FastAPI nativo) | Comunicación instantánea entre comanderos móviles, cocina (KDS) y caja. |
| **Contenedores** | Docker & Docker Compose | Multi-stage build en Frontend (Nginx para servir archivos estáticos, Node.js descartado en producción). |
| **Admin BD** | Adminer (Web) | Accesible en el puerto `8080` vía Docker. |

---

## 🔒 3. Principios de Ciberseguridad Obligatorios

1. **Sin Node.js en Producción:** El contenedor final de frontend usa Nginx Alpine. Node.js solo compila en la etapa de build; no debe exponerse como servidor de aplicaciones en producción.
2. **Cero Secretos en el Repositorio:** Ninguna clave, token JWT o credencial de base de datos debe quemarse en el código. Usar siempre variables de entorno cargadas desde `.env`.
3. **Inyección SQL Imposible:** Prohibido construir sentencias SQL mediante concatenación de strings (`f"SELECT * FROM..."`). Usar siempre la API de SQLAlchemy o consultas parametrizadas.
4. **Validación Exhaustiva con Pydantic:** Todo payload que reciba la API debe contar con su esquema Pydantic para tipado y saneamiento de datos antes de llegar a la lógica de negocio.
5. **Red Interna Aislada:** La base de datos PostgreSQL no debe exponerse a internet público; solo los servicios autorizados en la red interna de Docker pueden acceder a ella.

---

## 💻 4. Estándares de Código

### Frontend (Vue 3)
* Utilizar **Vue 3 Composition API** con `<script setup>`.
* Diseñar siempre pensando en **Mobile-First / Touch-Friendly**:
  * Botones grandes y fáciles de presionar en pantallas táctiles.
  * Estados visuales claros (`active:scale-95`, indicadores de color por estado de mesa u orden).
* Gestionar estados globales (comanda activa, usuario en turno) con **Pinia**.
* Toda vista o componente nuevo debe compilar con `npm run build` sin errores ni advertencias de importación.

### Backend (FastAPI)
* Estructura modular:
  * `app/models/`: Modelos de base de datos SQLAlchemy.
  * `app/schemas/`: Esquemas de validación Pydantic.
  * `app/api/v1/endpoints/`: Controladores de rutas divididos por recurso (mesas, pedidos, pagos, productos).
  * `app/core/`: Configuración y utilidades de seguridad.
* Inyección de dependencias para sesiones de base de datos (`Depends(get_db)`).

---

## 🛠️ 5. Comandos de Verificación antes de cada Commit

Antes de considerar una tarea o cambio completado:
1. **Frontend:** Ejecutar `cd frontend && npm run build` para asegurar que no hay errores de compilación ni módulos faltantes.
2. **Backend:** Asegurar que los esquemas e importaciones en Python no contengan errores de sintaxis o tipos.
3. **Git:** Escribir commits claros siguiendo la convención:
   * `feat: ...` para nuevas funcionalidades.
   * `fix: ...` para correcciones de errores.
   * `refactor: ...` para mejoras de código sin cambio funcional.
   * `docs: ...` para cambios de documentación.

---

## 📱 6. Convenciones de Negocio (Edén Café)
* **Estados de Mesa:** `libre`, `ocupada`, `cuenta` (por cobrar), `reservada`.
* **Estados de Comanda:** `en_cola`, `preparando`, `listo`, `entregado`, `pagado`.
* **Cortes de Caja:** 
  * *Corte X:* Arqueo parcial durante el turno sin cerrar caja.
  * *Corte Z:* Cierre definitivo del turno con reporte de totales por método de pago (Efectivo, Tarjeta, etc.).
