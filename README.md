# VEXOR GAMING / VEXOR GAMING

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC.svg)](https://tailwindcss.com/)
[![Alpine.js](https://img.shields.io/badge/Alpine.js-3.x-8BC0D0.svg)](https://alpinejs.dev/)
[![GSAP](https://img.shields.io/badge/GSAP-3.x-88CE02.svg)](https://greensock.com/gsap/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎮 Features (Fase 1) / Características (Fase 1)

| Category / Categoría | Details / Detalles |
|---|---|
| **Catalog / Catálogo** | Products, categories, brands, technical specifications / Productos, categorías, marcas, especificaciones técnicas |
| **Store / Tienda** | Filters: text search, category, brand, price range, availability / Filtros: búsqueda textual, categoría, marca, rango de precio, disponibilidad |
| **Sorting / Ordenamiento** | Price ↑/↓, best sellers, newest, highest discount / Precio ↑/↓, más vendidos, más recientes, mayor descuento |
| **UX** | Pagination with filter preservation in URL, image gallery, related products / Paginación con preservación de filtros en URL, galería de imágenes, productos relacionados |
| **Design / Diseño** | Gamer theme (dark + neon accents), **Orbitron** font (display) + **Inter** (body), 100% responsive / Tema gamer (oscuro + acentos neón), tipografía **Orbitron** (display) + **Inter** (body), 100% responsive |
| **Theme / Tema** | Dark/light mode with Alpine.js, `localStorage` persistence, no FOUC / Modo oscuro/claro con Alpine.js, persistencia en `localStorage`, sin FOUC |
| **Animations / Animaciones** | GSAP + ScrollTrigger: staggered hero, scroll reveal, hover micro-interactions / GSAP + ScrollTrigger: hero escalonado, reveal en scroll, micro-interacciones hover |
| **Accessibility / Accesibilidad** | `prefers-reduced-motion`, ARIA labels, visible focus, semantic HTML / `prefers-reduced-motion`, ARIA labels, focus visible, HTML semántico |
| **Admin** | Inlines for images/specs, filters, search, auto-generated slugs / Inlines para imágenes/especificaciones, filtros, búsqueda, slugs auto-generados |
| **Testing** | Models (discounts, stock) and views (home, shop, detail, 404, filters) / Modelos (descuentos, stock) y vistas (home, shop, detail, 404, filtros) |
| **Data / Datos** | 32 real products in 8 categories with brands, discounts, varied stock / 32 productos reales en 8 categorías con marcas, descuentos, stock variado |

---

## 🛠 Tech Stack / Stack Tecnológico

| Layer / Capa | Technology / Tecnología | Version / Versión |
|---|---|---|
| Backend | Python, Django | 3.12+, 5.x |
| Database | SQLite (dev) → PostgreSQL (prod) | — |
| Frontend | Django Templates + Tailwind CSS (CLI) | 3.x |
| Interactivity | Alpine.js | 3.x |
| Animations | GSAP + ScrollTrigger | 3.x |
| Images | Pillow | — |
| Config | python-decouple (.env) | — |
| Testing | Django TestCase | — |

---

## 📁 Project Structure / Estructura del Proyecto

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
├── dockerfile/              # Docker configuration / Configuración Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── entrypoint.sh
│   └── .dockerignore
├── vexor/                   # Django settings / Configuración Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── catalog/             # Main app (Phase 1) / App principal (Fase 1)
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
│   │   └── output.css (generated, not versioned / generado, no versionado)
│   ├── js/
│   │   ├── theme.js
│   │   ├── animations.js
│   │   └── main.js
│   └── img/
├── media/                   # Ignored in git (user uploads) / Ignorado en git (subidas de usuarios)
└── fixtures/
    └── initial_data.json    # 32 sample products / 32 productos de ejemplo
```

---

## 🚀 Installation & Setup / Instalación y Puesta en Marcha

### Prerequisites / Prerrequisitos
- **Python 3.12+**
- **Node.js 18+** (for Tailwind CLI / para Tailwind CLI)
- **Git**
- **Docker** (optional, for containerized deployment / opcional, para despliegue contenedorizado)

### 1. Clone & create virtual environment / Clonar y crear entorno virtual
```bash
git clone <repo-url>
cd vexor-gaming

# Create venv / Crear venv
python -m venv venv

# Activate / Activar
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (cmd):
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Python dependencies / Instalar dependencias Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables / Configurar variables de entorno
```bash
cp .env.example .env
# Edit .env with your values / Edita .env con tus valores
# Generate SECRET_KEY / Generar SECRET_KEY:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Required variables in `.env` / Variables requeridas en `.env`:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
# DATABASE_URL=postgres://...  # production only / solo producción
```

### 4. Install & compile Tailwind CSS / Instalar y compilar Tailwind CSS
```bash
npm install          # installs tailwindcss, autoprefixer, postcss / instala tailwindcss, autoprefixer, postcss
npm run build        # generates static/css/output.css (minified) / genera static/css/output.css (minificado)
# Development with watch / Desarrollo con watch:
npm run dev          # recompiles on template changes / recompila al cambiar templates/*.html
```

> ⚠️ **Important / Importante**: `static/css/output.css` is in `.gitignore`. **Always run `npm run build` after cloning or when changing `input.css` / templates.**

### 5. Database & sample data / Base de datos y datos de ejemplo
```bash
python manage.py migrate
python manage.py loaddata initial_data
```

### 6. Create superuser (optional) / Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Run development server / Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

**URLs:**
- 🌐 Site: http://127.0.0.1:8000/
- 🔧 Admin: http://127.0.0.1:8000/admin/

---

## 🔄 Daily Development Workflow / Flujo de Desarrollo Diario

```powershell
# Terminal 1 - Tailwind watch mode (recompiles CSS on template changes)
npm run dev

# Terminal 2 - Django runserver
python manage.py runserver
```

**Python changes:** Django auto-reloads (`--reload` by default) / **Cambios en Python:** Django recarga automáticamente (`--reload` por defecto).  
**`input.css` / template changes:** Tailwind CLI regenerates `output.css` instantly / **Cambios en `input.css` / plantillas:** Tailwind CLI regenera `output.css` al instante.

---

## 🐳 Docker Deployment / Despliegue con Docker

```bash
# From project root / Desde la raíz del proyecto
cd dockerfile
docker-compose up --build
```

**Access at / Acceder en:** http://localhost:8000

The container runs migrations and `collectstatic` automatically on startup via `entrypoint.sh` / El contenedor ejecuta migraciones y `collectstatic` automáticamente al iniciar vía `entrypoint.sh`.

---

## ✅ Quick Verification / Verificación Rápida

```bash
# Unit & integration tests / Tests unitarios e integración
python manage.py test apps.catalog

# Linting (optional, if you add ruff/flake8)
# ruff check .

# Tailwind compilation (verifies no errors) / Compilación Tailwind (verifica que no hay errores)
npm run build
```

### Included Tests / Tests incluidos
```bash
python manage.py test apps.catalog.tests.ModelTests
python manage.py test apps.catalog.tests.ViewTests
```

**Coverage / Cobertura:**
- **Models / Modelos**: `has_discount`, `discount_percent`, `in_stock`, `current_price`, unique slugs / slugs únicos
- **Views / Vistas**: Home (200, context), Shop (filters, pagination, sort), Detail (404 if inactive), Custom 404 / 404 personalizado

---

## 🗺 Roadmap by Phases / Roadmap por Fases

| Phase / Fase | Status / Estado | Focus / Enfoque | New Apps / Apps Nuevas |
|---|---|---|---|
| **1** | ✅ Complete / Completa | Catalog & Store / Catálogo y Tienda | `catalog` |
| **2** | 🔄 In progress / En progreso | Accounts, Cart, Wishlist / Cuentas, Carrito, Favoritos | `accounts`, `cart`, `wishlist` |
| **3** | ⏳ Planned / Planificada | Simulated Checkout & Orders / Checkout Simulado y Pedidos | `orders`, `payments` (mock) |
| **4** | ⏳ Planned / Planificada | Advanced Admin Panel / Panel Administrativo Avanzado | `dashboard` (analytics, reports) |
| **5** | ⏳ Planned / Planificada | PC Builder & Comparator / Armador de PC y Comparador | `pcbuilder`, `compare` |
| **6** | ⏳ Planned / Planificada | Reviews, Coupons, Notifications, Analytics / Reseñas, Cupones, Notificaciones, Analíticas | `reviews`, `coupons`, `notifications`, `analytics` |

---

## 🎨 Color Customization (Tailwind) / Personalización de Colores (Tailwind)

Edit `tailwind.config.js` → `theme.extend.colors` / Edita `tailwind.config.js` → `theme.extend.colors`:

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9',  // Primary Cyan / Cian principal
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

## 📦 Future Apps (Not yet included) / Apps Futuras (No incluidas aún)

| App | Description / Descripción |
|-----|---|
| `cart` | Persistent cart (session + DB) / Carrito persistente (sesión + BD) |
| `orders` | Orders, history, states, emails / Pedidos, historial, estados, emails |
| `accounts` | Register, login, profile, addresses, 2FA / Registro, login, perfil, direcciones, 2FA |
| `wishlist` | Wishlist with price drop notifications / Lista de deseos con notificaciones de precio |
| `pcbuilder` | Component compatibility, build validation / Compatibilidad de componentes, validación de builds |
| `compare` | Side-by-side spec comparison / Comparador lado a lado de especificaciones |
| `reviews` | Ratings, photos, verified purchases / Valoraciones, fotos, compras verificadas |
| `coupons` | Coupons, volume discounts, business rules / Cupones, descuentos por volumen, reglas de negocio |
| `notifications` | Email, push, in-app, user preferences / Email, push, in-app, preferencias de usuario |
| `dashboard` | Sales metrics, users, products, cohorts / Métricas de ventas, usuarios, productos, cohortes |
| `analytics` | GA4/Plausible events, funnel, retention / Eventos GA4/Plausible, funnel, retención |

---

## 🔒 Security & Best Practices / Seguridad y Buenas Prácticas

- ✅ `SECRET_KEY` and `DEBUG` in `.env` (never in code) / `SECRET_KEY` y `DEBUG` en `.env` (nunca en código)
- ✅ `ALLOWED_HOSTS` configured per environment / `ALLOWED_HOSTS` configurado por entorno
- ✅ CSRF, XSS, Clickjacking protection (Django middleware) / CSRF, XSS, Clickjacking protection (middleware Django)
- ✅ Password validators enabled / Password validators habilitados
- ✅ `SECURE_*` settings in production (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, etc.) / `SECURE_*` settings en producción
- ✅ Media files served by nginx/CDN in production / Media files servidas por nginx/CDN en producción
- ✅ `prefers-reduced-motion` respected in all animations / `prefers-reduced-motion` respetado en todas las animaciones
- ✅ Security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`) / Headers de seguridad

---

## 🤝 Contributing / Contribuir

1. Fork the repo / Fork del repo
2. Create a branch: `git checkout -b feature/new-feature` / Crea una rama
3. Commit with conventional messages: `feat: add brand filter` / Commit con mensajes convencionales
4. Push: `git push origin feature/new-feature`
5. Open a Pull Request / Abre un Pull Request

**Code standards / Estándares de código:**
- Python: `black`, `isort`, `ruff` (config in `pyproject.toml` if exists)
- JS/CSS: `prettier` (config in `.prettierrc`)
- Commits: [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📸 Screenshots / Capturas de Pantalla (Placeholder)

| Home | Shop | Product Detail |
|------|------|----------------|
| ![Home](docs/screenshots/home.png) | ![Shop](docs/screenshots/shop.png) | ![Detail](docs/screenshots/detail.png) |

> Add real screenshots in `docs/screenshots/` to showcase the UI / Añade capturas reales en `docs/screenshots/` para mostrar el UI.

---

## 📝 License / Licencia

**MIT License** – Free for personal and commercial use / Libre para uso personal y comercial. See `LICENSE` for details / Ver `LICENSE` para detalles.

---

## 👨‍💻 Author / Autor

**Manuel Rojas** – Full Stack Developer / Desarrollador Full Stack  
🔗 [Portfolio](#) · [LinkedIn](#) · [GitHub](#)

---

> **Issues?** Check [Troubleshooting](#-troubleshooting) or open an *Issue* / **¿Problemas?** Revisa la sección [Troubleshooting](#-troubleshooting) o abre un *Issue*.

---

## 🛠 Troubleshooting

| Problem / Problema | Solution / Solución |
|---|---|
| **Styles not loading (no CSS)** | Run `npm run build` and verify `static/css/output.css` exists / Ejecuta `npm run build` y verifica que existe `static/css/output.css` |
| **404 on `/static/css/output.css`** | Ensure you ran `npm run build` and `DEBUG=True` in dev / Asegúrate de haber corrido `npm run build` y que `DEBUG=True` en desarrollo |
| **Tailwind doesn't detect new classes** | Use `npm run dev` (watch mode) or re-run `npm run build` / Usa `npm run dev` (watch mode) o vuelve a correr `npm run build` |
| **`ModuleNotFoundError` on `python manage.py`** | Activate virtualenv (`venv\Scripts\Activate.ps1`) / Activa el entorno virtual |
| **`SECRET_KEY` error** | Copy `.env.example` to `.env` and generate a valid key / Copia `.env.example` a `.env` y genera una clave válida |
| **Port 8000 in use** | `python manage.py runserver 8001` or kill previous process / `python manage.py runserver 8001` o mata el proceso previo |
| **DB out of sync** | `python manage.py migrate --run-syncdb` (dev only) |
| **Fonts not loading (Orbitron/Inter)** | Check internet (Google Fonts) or download locally / Verifica conexión a internet (Google Fonts) o descarga localmente |

---

## 📋 Useful Commands (Cheatsheet) / Comandos Útiles (Cheatsheet)

```bash
# Django
python manage.py runserver              # Dev server
python manage.py shell                  # Django shell
python manage.py dbshell                # SQL shell
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Admin user
python manage.py collectstatic          # Collect static (prod)
python manage.py check --deploy         # Production checks
python manage.py test                   # Run tests
python manage.py loaddata initial_data  # Load fixtures
python manage.py dumpdata > backup.json # Backup data

# Tailwind / Node
npm install              # Install deps
npm run dev              # Watch mode (dev)
npm run build            # Minified build (dev/staging)
npm run build:prod       # Production build (NODE_ENV=production)

# Docker
cd dockerfile && docker-compose up --build  # Start with Docker
docker-compose down                         # Stop containers
docker-compose logs -f                      # View logs

# Git
git status
git add -A
git commit -m "feat: description"
git push
```

---

## 🔧 Production Deployment Checklist / Checklist pre-deploy

- [ ] `npm run build:prod` (minified CSS + purge)
- [ ] `python manage.py collectstatic --noinput`
- [ ] `python manage.py check --deploy`
- [ ] Migrations applied on production DB / Migraciones aplicadas en BD de producción
- [ ] Static files served by nginx/CDN (`/static/`) / Static files servidos por nginx/CDN
- [ ] Media files served by nginx/CDN (`/media/`) / Media files servidos por nginx/CDN
- [ ] HTTPS enforced + HSTS / HTTPS forzado + HSTS
- [ ] Automated DB backups / Backups automáticos de BD

---

*Last updated / Última actualización: 2026-10-05*