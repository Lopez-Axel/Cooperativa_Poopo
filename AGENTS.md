# AGENTS.md

Sistema de Asistencia for Cooperativa Minera Poopó R.L. Two projects in one repo.

## Run commands

```bash
# Backend (port 8000)
cd sistema-asistencia-backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (port 3000)
cd sistema-asistencia-frontend
npm install
npm run dev

# Deploy: Dockerfile at root builds backend only; Railway deploys via railway.toml
```

No test frameworks configured. If adding: backend `pytest + pytest-asyncio`, frontend `vitest`.

## Backend quirks

- **No migrations.** `Base.metadata.create_all(bind=engine)` runs at import time in `main.py:6`. Production risk with PostgreSQL.
- **`redirect_slashes=False`** (`main.py:12`). Routes inconsistently use trailing slashes: `/api/secciones` (no slash) vs `/api/cuadrillas/` (slash). Frontend must match exactly.
- **Old-style `declarative_base()`** in `database.py`, not SQLAlchemy 2.0 `mapped_column`/`DeclarativeMeta`.
- **SQLite by default** (`sqlite:///./cooperativa.db`). Set `DATABASE_URL` env var for PostgreSQL. `check_same_thread` auto-handled in `database.py`.
- **Config required at startup:** `SECRET_KEY` (min 32 chars), `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — raises `ValueError` if missing (`config.py:22-28`).
- **Service/repo singletons** exported from `__init__.py` (e.g., `auth_service = AuthService()`). Services receive `db: Session` as first param. Repos manage `db.add/commit/refresh`. All raise `HTTPException` directly.
- **Protected dependencies** in `utils/dependencies.py`: `get_current_user` (any auth), `get_current_superuser` (admin). `get_current_active_user` defined but never used.
- **JWT**: `python-jose` (not `PyJWT`), HS256, 8h expiry (`ACCESS_TOKEN_EXPIRE_HOURS`). Payload: `sub`, `username`, `is_superuser`, `exp`, `iat`.
- **Password hashing**: `passlib` + `bcrypt`.
- **Upload routes** (`upload.py`) use `async def` (for `UploadFile`); all other routes are sync `def`.
- **Seed data**: `python init_db.py` creates admin user (`admin`/`admin123`) and optionally imports `lista_cooperativistas_agosto.xlsx` (pandas). `python init_coop.py` does incremental import with duplicate checking.

## Frontend quirks

- **`runtimeConfig.apiBaseUrl` (`nuxt.config.js:12`) is defined but ignored.** All stores hardcode the URL from `authStore.apiUrl` which points to `'https://cooperativapoopo-production-450b.up.railway.app'`.
- **`sessionStorage`** for auth tokens, not `localStorage`. Cleared on tab close.
- **Two inconsistent HTTP clients** across stores: `$fetch` (Nuxt built-in) in `auth.js`, `cooperativistas.js`, `users.js`, `devices.js`; native `fetch()` in `attendance.js`, `attendancePeriod.js`, `cuadrillas.js`. `secciones.js` mixes both. Error response reading differs between them.
- **Trailing slashes are required** in API calls (`/api/users/` not `/api/users`). Multiple store comments confirm this.
- **All Pinia stores** use Options API (`state/getters/actions`). No Setup stores.
- **Layout pattern**: `login.vue` uses `layout: false`; dashboard pages use `layout: 'dashboard'` + `middleware: 'auth'`. Admin pages additionally use `middleware: 'admin'`.
- **Soft vs hard DELETE**: `secciones.js` and `cuadrillas.js` use `PUT { is_active: false }`; `attendance.js` and `attendancePeriod.js` hard-delete with confirmation string `'DELETE_PERMANENTLY'`.
- **`Fuse.js` imported** in `cuadrillas.js`/`secciones.js` for fuzzy search but NOT in `package.json` (transitive dependency).
- **Auth plugin**: `app/plugins/auth.client.js` calls `authStore.initFromStorage()` on client boot.
- **All UI text, comments, variable names** in Spanish. Locale: `es-BO`.

## Project conventions

- **File naming**: `snake_case` everywhere (both Python and Vue files).
- **Spanish/English mix**: Models use Spanish (`Seccion`, `Cuadrilla`, `Cooperativista`). Some route/services are English (`attendance`, `auth`, `users`), others Spanish (`secciones`, `cuadrillas`).
- **Code style**: Backend uses old-style `Column`/`Integer`/`String` SQLAlchemy, not `mapped_column`. Pydantic v2 `ConfigDict(from_attributes=True)`. Frontend uses `<script setup>` Composition API with Bulma CSS.
