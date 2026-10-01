# VEXOR GAMING

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC.svg)](https://tailwindcss.com/)
[![Alpine.js](https://img.shields.io/badge/Alpine.js-3.x-8BC0D0.svg)](https://alpinejs.dev/)
[![GSAP](https://img.shields.io/badge/GSAP-3.x-88CE02.svg)](https://greensock.com/gsap/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

E-commerce de hardware y periféricos gamer construido con **Django 5.x** y frontend moderno (**Tailwind CSS + Alpine.js + GSAP**). Proyecto de portafolio para demostrar habilidades full-stack.

---

## 🎮 Características (Fase 1)

| Categoría | Detalles |
|-----------|----------|
| **Catálogo** | Productos, categorías, marcas, especificaciones técnicas |
| **Tienda** | Filtros: búsqueda textual, categoría, marca, rango de precio, disponibilidad |
| **Ordenamiento** | Precio ↑/↓, más vendidos, más recientes, mayor descuento |
| **UX** | Paginación con preservación de filtros en URL, galería de imágenes, productos relacionados |
| **Diseño** | Tema gamer (oscuro + acentos neón), tipografía **Orbitron** (display) + **Inter** (body), 100% responsive |
| **Tema** | Modo oscuro/claro con Alpine.js, persistencia en `localStorage`, sin FOUC |
| **Animaciones** | GSAP + ScrollTrigger: hero escalonado, reveal en scroll, micro-interacciones hover |
| **Accesibilidad** | `prefers-reduced-motion`, ARIA labels, focus visible, HTML semántico |
| **Admin** | Inlines para imágenes/especificaciones, filtros, búsqueda, slugs auto-generados |
| **Testing** | Modelos (descuentos, stock) y vistas (home, shop, detail, 404, filtros) |
| **Datos** | 32 productos reales en 8 categorías con marcas, descuentos, stock variado |

---

## 🛠 Stack Tecnológico

| Capa | Tecnología | Versión |
|------|------------|---------|
| Backend | Python, Django | 3.12+, 5.x |
| Database | SQLite (dev) → PostgreSQL (prod) | — |
| Frontend | Django Templates + Tailwind CSS (CLI) | 3.x |
| Interactividad | Alpine.js | 3.x |
| Animaciones | GSAP + ScrollTrigger | 3.x |
| Imágenes | Pillow | — |
| Config | python-decouple (.env) | — |
| Testing | Django TestCase | — |

---

## 📁 Estructura del Proyecto

```
vexor-gaming/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── tailwind.config.js
├── package.json
├── postcss.config.js
├── vexor/                 # Configuración Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── catalog/           # App principal (Fase 1)
│       ├── models.py
│       ├── views.py
│       ├── admin.py
│       ├── urls.py
│       ├── tests.py
│       ├── context_processors.py
│       ├── templatetags/
│       └── migrations/
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── product_card.html
│   └── catalog/
│       ├── home.html
│       ├── shop.html
│       └── product_detail.html
├── static/
│   ├── css/
│   │   ├── input.css
│   │   └── output.css (generado, no versionado)
│   ├── js/
│   │   ├── theme.js
│   │   ├── animations.js
│   │   └── main.js
│   └── img/
├── media/                 # Ignorado en git (subidas de usuarios)
└── fixtures/
    └── initial_data.json  # 32 productos de ejemplo
```

---

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos
- **Python 3.12+**
- **Node.js 18+** (para Tailwind CLI)
- **Git**

### 1. Clonar y crear entorno virtual
```bash
git clone <repo-url>
cd vexor-gaming

# Crear venv
python -m venv venv

# Activar
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (cmd):
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus valores
# Generar SECRET_KEY:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Variables requeridas en `.env`:**
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
# DATABASE_URL=postgres://...  # solo producción
```

### 4. Instalar y compilar Tailwind CSS
```bash
npm install          # instala tailwindcss, autoprefixer, postcss
npm run build        # genera static/css/output.css (minificado)
# Desarrollo con watch:
npm run dev          # recompila al cambiar templates/*.html
```

> ⚠️ **Importante**: `static/css/output.css` está en `.gitignore`. **Siempre ejecuta `npm run build` tras clonar o al cambiar `input.css` / plantillas.**

### 5. Base de datos y datos de ejemplo
```bash
python manage.py migrate
python manage.py loaddata initial_data
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

**URLs:**
- 🌐 Sitio: http://127.0.0.1:8000/
- 🔧 Admin: http://127.0.0.1:8000/admin/

---

## 🔄 Flujo de Desarrollo Diario

```powershell
# Terminal 1 - Tailwind watch mode (recompila CSS al tocar templates)
npm run dev

# Terminal 2 - Django runserver
python manage.py runserver
```

**Cambios en Python:** Django recarga automáticamente (`--reload` por defecto).  
**Cambios en `input.css` / plantillas:** Tailwind CLI regenera `output.css` al instante.

---

## ✅ Verificación Rápida

```bash
# Tests unitarios e integración
python manage.py test apps.catalog

# Linting (opcional, si añades ruff/flake8)
# ruff check .

# Compilación Tailwind (verifica que no hay errores)
npm run build
```

### Tests incluidos
```bash
python manage.py test apps.catalog.tests.ModelTests
python manage.py test apps.catalog.tests.ViewTests
```

**Cobertura:**
- **Modelos**: `has_discount`, `discount_percent`, `in_stock`, `current_price`, slugs únicos
- **Vistas**: Home (200, contexto), Shop (filtros, paginación, orden), Detail (404 si inactivo), 404 custom

---

## 🗺 Roadmap por Fases

| Fase | Estado | Enfoque | Apps Nuevas |
|------|--------|---------|-------------|
| **1** | ✅ Completa | Catálogo y Tienda | `catalog` |
| **2** | 🔄 En progreso | Cuentas, Carrito, Favoritos | `accounts`, `cart`, `wishlist` |
| **3** | ⏳ Planificada | Checkout Simulado y Pedidos | `orders`, `payments` (mock) |
| **4** | ⏳ Planificada | Panel Administrativo Avanzado | `dashboard` (analytics, informes) |
| **5** | ⏳ Planificada | Armador de PC y Comparador | `pcbuilder`, `compare` |
| **6** | ⏳ Planificada | Reseñas, Cupones, Notificaciones, Analíticas | `reviews`, `coupons`, `notifications`, `analytics` |

---

## 🎨 Personalización de Colores (Tailwind)

Edita `tailwind.config.js` → `theme.extend.colors`:

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9',  // Cyan principal
        600: '#0284c7',
      },
      neon: {
        cyan: '#00ffff',
        pink: '#ff00ff',
        green: '#39ff14',
        purple: '#bc13fe',
      },
    },
    fontFamily: {
      orbitron: ['Orbitron', 'sans-serif'],
      inter: ['Inter', 'sans-serif'],
    },
  },
}
```

---

## 📦 Apps Futuras (No incluidas aún)

| App | Descripción |
|-----|-------------|
| `cart` | Carrito persistente (sesión + BD) |
| `orders` | Pedidos, historial, estados, emails |
| `accounts` | Registro, login, perfil, direcciones, 2FA |
| `wishlist` | Lista de deseos con notificaciones de precio |
| `pcbuilder` | Compatibilidad de componentes, validación de builds |
| `compare` | Comparador lado a lado de especificaciones |
| `reviews` | Valoraciones, fotos, compras verificadas |
| `coupons` | Cupones, descuentos por volumen, reglas de negocio |
| `notifications` | Email, push, in-app, preferencias de usuario |
| `dashboard` | Métricas de ventas, usuarios, productos, cohortes |
| `analytics` | Eventos GA4/Plausible, funnel, retención |

---

## 🔒 Seguridad y Buenas Prácticas

- ✅ `SECRET_KEY` y `DEBUG` en `.env` (nunca en código)
- ✅ `ALLOWED_HOSTS` configurado por entorno
- ✅ CSRF, XSS, Clickjacking protection (middleware Django)
- ✅ Password validators habilitados
- ✅ `SECURE_*` settings en producción (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, etc.)
- ✅ Media files servidas por nginx/CDN en producción
- ✅ `prefers-reduced-motion` respetado en todas las animaciones
- ✅ Headers de seguridad (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`)

---

## 🐳 Despliegue (Producción)

### Docker (recomendado)
```dockerfile
# Dockerfile.example
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN npm ci && npm run build:prod
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "vexor.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Variables de producción (`.env.production`)
```env
DEBUG=False
SECRET_KEY=clave-super-secreta-produccion
ALLOWED_HOSTS=vexor-gaming.com,www.vexor-gaming.com
DATABASE_URL=postgres://user:pass@db:5432/vexor
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Checklist pre-deploy
- [ ] `npm run build:prod` (CSS minificado + purge)
- [ ] `python manage.py collectstatic --noinput`
- [ ] `python manage.py check --deploy`
- [ ] Migraciones aplicadas en BD de producción
- [ ] Static files servidos por nginx/CDN (`/static/`)
- [ ] Media files servidos por nginx/CDN (`/media/`)
- [ ] HTTPS forzado + HSTS
- [ ] Backups automáticos de BD

---

## 🤝 Contribuir

1. Fork del repo
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit con mensajes convencionales: `feat: añade filtro por marca`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

**Estándares de código:**
- Python: `black`, `isort`, `ruff` (config en `pyproject.toml` si existe)
- JS/CSS: `prettier` (config en `.prettierrc`)
- Commits: [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📸 Capturas de Pantalla (Placeholder)

| Home | Shop | Product Detail |
|------|------|----------------|
| ![Home](docs/screenshots/home.png) | ![Shop](docs/screenshots/shop.png) | ![Detail](docs/screenshots/detail.png) |

> Añade capturas reales en `docs/screenshots/` para mostrar el UI.

---

## 📝 Licencia

**MIT License** – Libre para uso personal y comercial. Ver `LICENSE` para detalles.

---

## 👨‍💻 Autor

**Manuel Rojas** – Desarrollador Full Stack  
🔗 [Portafolio](#) · [LinkedIn](#) · [GitHub](#)

---

> **¿Problemas?** Revisa la sección [Troubleshooting](#-troubleshooting) o abre un *Issue*.

---

## 🛠 Troubleshooting

| Problema | Solución |
|----------|----------|
| **Estilos no cargan (página sin CSS)** | Ejecuta `npm run build` y verifica que existe `static/css/output.css` |
| **404 en `/static/css/output.css`** | Asegúrate de haber corrido `npm run build` y que `DEBUG=True` en desarrollo |
| **Tailwind no detecta clases nuevas** | Usa `npm run dev` (watch mode) o vuelve a correr `npm run build` |
| **Error `ModuleNotFoundError` al hacer `python manage.py`** | Activa el entorno virtual (`venv\Scripts\Activate.ps1`) |
| **`SECRET_KEY` error** | Copia `.env.example` a `.env` y genera una clave válida |
| **Puerto 8000 ocupado** | `python manage.py runserver 8001` o mata el proceso previo |
| **BD desincronizada** | `python manage.py migrate --run-syncdb` (solo dev) |
| **Fuentes no cargan (Orbitron/Inter)** | Verifica conexión a internet (Google Fonts) o descarga localmente |

---

## 📋 Comandos Útiles (Cheatsheet)

```bash
# Django
python manage.py runserver              # Dev server
python manage.py shell                  # Django shell
python manage.py dbshell                # SQL shell
python manage.py makemigrations         # Crear migraciones
python manage.py migrate                # Aplicar migraciones
python manage.py createsuperuser        # Admin user
python manage.py collectstatic          # Recopilar static (prod)
python manage.py check --deploy         # Verificaciones de prod
python manage.py test                   # Ejecutar tests
python manage.py loaddata initial_data  # Cargar fixtures
python manage.py dumpdata > backup.json # Backup datos

# Tailwind / Node
npm install              # Instalar deps
npm run dev              # Watch mode (dev)
npm run build            # Build minificado (dev/staging)
npm run build:prod       # Build producción (NODE_ENV=production)

# Git
git status
git add -A
git commit -m "feat: descripción"
git push
```

---

*Última actualización: 2026-10-01*