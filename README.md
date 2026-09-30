# VEXOR GAMING

E-commerce de hardware y periféricos gamer construido con Django 5.x y frontend moderno (Tailwind CSS + Alpine.js + GSAP). Proyecto de portafolio para demostrar habilidades full-stack.

## 🎮 Características (Fase 1)

- **Catálogo completo**: Productos, categorías, marcas, especificaciones técnicas
- **Tienda con filtros**: Búsqueda por texto, categoría, marca, rango de precio, disponibilidad
- **Ordenamiento**: Precio, más vendidos, más recientes, mayor descuento
- **Paginación** y preservación de filtros en URL
- **Página de producto**: Galería de imágenes, especificaciones, productos relacionados
- **Diseño gamer**: Paleta oscura con acentos neón, tipografía Orbitron, 100% responsive
- **Modo oscuro/claro**: Con Alpine.js, persistencia en localStorage, sin parpadeo (FOUC)
- **Animaciones GSAP**: Hero escalonado, tarjetas al hacer scroll, micro-interacciones en hover
- **Accesibilidad**: `prefers-reduced-motion`, ARIA labels, focus visible, semantic HTML
- **Admin Django**: Inlines para imágenes y specs, filtros, búsqueda, slugs auto-generados
- **Tests**: Modelos (descuentos, stock) y vistas (home, shop, detail, 404, filtros)
- **Fixtures**: 32 productos reales en 8 categorías con marcas, descuentos, stock variado

## 🛠 Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.12+, Django 5.x |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Frontend | Django Templates + Tailwind CSS (CLI) |
| Interactividad | Alpine.js 3.x |
| Animaciones | GSAP 3.x + ScrollTrigger |
| Imágenes | Pillow |
| Config | python-decouple (.env) |
| Testing | Django TestCase |

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
│   │   └── output.css (generado)
│   ├── js/
│   │   ├── theme.js
│   │   ├── animations.js
│   │   └── main.js
│   └── img/
├── media/                 # Ignorado en git
└── fixtures/
    └── initial_data.json  # 32 productos de ejemplo
```

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos
- Python 3.12+
- Node.js 18+ (para Tailwind CLI)
- Git

### 1. Clonar y crear entorno virtual
```bash
git clone <repo-url>
cd vexor-gaming
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env y genera una SECRET_KEY:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Instalar y compilar Tailwind CSS
```bash
npm install
npm run build
# Para desarrollo con watch:
npm run dev
```

### 5. Base de datos y datos de ejemplo
```bash
python manage.py migrate
python manage.py loaddata initial_data
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor
```bash
python manage.py runserver
```

Visita: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## ✅ Verificación Rápida

```bash
# Tests
python manage.py test apps.catalog

# Linting (si configuras ruff/flake8)
# ruff check .

# Verificar Tailwind
npm run build
```

## 🧪 Tests Incluidos

```bash
python manage.py test apps.catalog.tests.ModelTests
python manage.py test apps.catalog.tests.ViewTests
```

Cubren:
- Modelos: `has_discount`, `discount_percent`, `in_stock`, `current_price`, slugs únicos
- Vistas: Home (200, contexto), Shop (filtros, paginación, orden), Detail (404 si inactivo), 404 custom

## 🗺 Roadmap por Fases

| Fase | Enfoque | Apps Nuevas |
|------|---------|-------------|
| **1** ✅ | Catálogo y Tienda | `catalog` |
| **2** 🔄 | Cuentas, Carrito, Favoritos | `accounts`, `cart`, `wishlist` |
| **3** | Checkout Simulado y Pedidos | `orders`, `payments` (mock) |
| **4** | Panel Administrativo Avanzado | `dashboard` (analytics, informes) |
| **5** | Armador de PC y Comparador | `pcbuilder`, `compare` |
| **6** | Reseñas, Cupones, Notificaciones, Analíticas | `reviews`, `coupons`, `notifications`, `analytics` |

## 🎨 Personalización de Colores (Tailwind)

Edita `tailwind.config.js` → `theme.extend.colors`:

```js
primary: { 500: '#0ea5e9', 600: '#0284c7' },  // Cyan principal
neon: {
  cyan: '#00ffff',
  pink: '#ff00ff',
  green: '#39ff14',
  purple: '#bc13fe',
}
```

Fuentes en `theme.extend.fontFamily`:
- `orbitron`: Títulos (display)
- `inter`: Cuerpo de texto

## 📦 Apps Futuras (No incluidas aún)

- `cart` - Carrito de compras con sesión/BD
- `orders` - Pedidos, historial, estados
- `accounts` - Registro, login, perfil, direcciones
- `wishlist` - Lista de deseos
- `pcbuilder` - Compatibilidad componentes, validación
- `compare` - Comparador lado a lado
- `reviews` - Valoraciones, fotos, verificadas
- `coupons` - Cupones, descuentos, reglas
- `notifications` - Email, push, in-app
- `dashboard` - Métricas, ventas, usuarios
- `analytics` - Eventos, funnel, cohortes

## 🔒 Seguridad y Buenas Prácticas

- `SECRET_KEY` y `DEBUG` en `.env` (nunca en código)
- `ALLOWED_HOSTS` configurado por entorno
- CSRF, XSS, Clickjacking protection (Django middleware)
- Password validators habilitados
- `SECURE_*` settings en producción
- Media files servidas por nginx/CDN en prod
- `prefers-reduced-motion` respetado en todas las animaciones

## 📝 Licencia

MIT License - Libre para uso personal y comercial.

## 👨‍💻 Autor

Proyecto de portafolio - Desarrollador Full Stack