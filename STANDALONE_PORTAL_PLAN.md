# Standalone Frappe UI Supplier Portal - Implementation Plan

## Overview

Build a standalone Frappe UI (Vue 3) web application for external supplier users that communicates with the existing Frappe instance via REST API. The architecture supports network separation with Apigee gateway in production while maintaining direct connection in development.

## Architecture

```
Development:  [Frappe UI App] → [Direct HTTP] → [Frappe Instance (localhost:8000)]
Production:   [Frappe UI App] → [Apigee Gateway] → [Frappe Instance (Private Network)]
                 (Public)         (Auth/Security)        (Existing Siud App)
```

## Key Design Decisions

- **Framework**: Frappe UI (Vue 3 + TypeScript + Tailwind CSS)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **API**: Environment-based configuration (dev: direct, prod: Apigee)
- **Auth**: Session-based (dev), JWT tokens (prod via Apigee)
- **Type Safety**: Auto-generated TypeScript interfaces from Frappe DocTypes
- **Data Sync**: Build-time (types, validations, reference data) + Runtime (transactional data)
- **Localization**: Hebrew RTL with Rubik font
- **File Storage**: Frappe's built-in file system (`/api/method/upload_file`)
- **User Management**: MVP uses test users; future: permission levels per user

## Project Structure

```
/home/tzvi/frappe/
├── frappe_docker/              # Existing Frappe instance
└── supplier-portal-ui/         # NEW: Standalone UI app
    ├── .env.development        # → http://localhost:8000
    ├── .env.production         # → https://apigee-gateway-url
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    │
    ├── scripts/
    │   ├── generate-types.ts       # DocType → TypeScript interfaces
    │   └── sync-reference-data.ts  # Fetch reference data at build
    │
    ├── src/
    │   ├── api/
    │   │   ├── client.ts           # Base Frappe REST API client
    │   │   ├── auth.ts             # Authentication
    │   │   ├── supplier.ts         # Supplier API calls
    │   │   ├── inquiry.ts          # Inquiry API calls
    │   │   └── reference.ts        # Reference data
    │   │
    │   ├── types/                  # GENERATED TypeScript types
    │   │   ├── supplier.ts
    │   │   ├── supplier-inquiry.ts
    │   │   ├── activity-domain-category.ts
    │   │   ├── inquiry-topic-category.ts
    │   │   └── ...
    │   │
    │   ├── stores/                 # Pinia state management
    │   │   ├── auth.ts             # User, supplier, auth state
    │   │   ├── reference.ts        # Cached reference data
    │   │   └── inquiry.ts          # Inquiry state
    │   │
    │   ├── views/
    │   │   ├── LoginView.vue
    │   │   ├── DashboardView.vue   # Stats + recent inquiries
    │   │   ├── InquiryListView.vue
    │   │   ├── InquiryDetailView.vue
    │   │   ├── InquiryFormView.vue
    │   │   └── ProfileView.vue
    │   │
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── AppHeader.vue
    │   │   │   └── UserMenu.vue
    │   │   ├── inquiry/
    │   │   │   ├── InquiryCard.vue
    │   │   │   ├── InquiryTable.vue
    │   │   │   ├── InquiryForm.vue
    │   │   │   └── StatusBadge.vue
    │   │   └── common/
    │   │       ├── StatCard.vue
    │   │       ├── LoadingSpinner.vue
    │   │       └── EmptyState.vue
    │   │
    │   └── assets/
    │       └── styles/
    │           ├── main.css
    │           └── rtl.css         # Hebrew RTL overrides
    │
    └── public/
        └── data/                   # Static reference data (build-time)
            ├── activity-domains.json
            ├── inquiry-topics.json
            └── supplier-roles.json
```

## API Surface - Whitelisted Methods

All API methods are accessible via `POST /api/method/siud.api.supplier_portal.<method_name>`.

### Authentication & User Info

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_current_user` | None | `{user: {...}, supplier: {...}}` | Get current user info and linked supplier |

### Supplier Profile

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_supplier_profile` | None | `{name, supplier_id, supplier_name, phone, email, address, activity_domains, contact_persons}` | Get full supplier profile |
| `update_supplier_profile` | `supplier_name`, `phone`, `email`, `address` | `{success, message}` | Update supplier profile fields |

### Inquiry Management

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_inquiry_stats` | None | `{total, open, closed, by_status}` | Get inquiry counts |
| `get_inquiries` | `page?`, `page_size?`, `status?`, `date_from?`, `date_to?`, `order_by?` | `{data, total, page, page_size, total_pages}` | Paginated inquiry list |
| `get_inquiry` | `name` | Full inquiry object with attachments | Get single inquiry detail |
| `create_inquiry` | `topic_category`, `description`, `inquiry_context`, `insured_id?`, `insured_name?` | `{success, name, message}` | Create new inquiry |
| `attach_file_to_inquiry` | `inquiry_name`, `file_url` | `{success, message}` | Link uploaded file to inquiry |

### Reference Data

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_reference_data` | None (allows guest) | `{activity_domains[], inquiry_topics[], supplier_roles[], contact_person_roles[], inquiry_statuses[], inquiry_contexts[]}` | All static reference data |

### Reference Data Fields

**activity_domains**: `name`, `category_code`, `category_name`
**inquiry_topics**: `name`, `category_code`, `category_name`, `parent_inquiry_topic_category`
**supplier_roles**: `name`, `role_name`, `role_title_he`
**contact_person_roles**: `name`, `role`
**inquiry_statuses**: `value`, `label`, `type` (open/closed)
**inquiry_contexts**: `value`, `label`

### File Upload

File upload uses Frappe's built-in endpoint:
```
POST /api/method/upload_file
Content-Type: multipart/form-data

file: <binary>
doctype: "Supplier Inquiry"  (optional, set after with attach_file_to_inquiry)
docname: <inquiry_name>      (optional)
```

### API Usage Examples

**Login (Session-based for dev):**
```javascript
POST /api/method/login
{
  "usr": "supplier@example.com",
  "pwd": "password"
}
```

**Get Current User:**
```javascript
POST /api/method/siud.api.supplier_portal.get_current_user
// Returns: { user: {...}, supplier: {...} }
```

**Get Inquiries with Pagination:**
```javascript
POST /api/method/siud.api.supplier_portal.get_inquiries
{
  "page": 1,
  "page_size": 20,
  "status": "פתוחה"
}
```

**Create Inquiry:**
```javascript
POST /api/method/siud.api.supplier_portal.create_inquiry
{
  "topic_category": "שאלות כלליות",
  "description": "תיאור הפנייה...",
  "inquiry_context": "ספק עצמו"
}
```

### Error Responses

All methods return standard Frappe error format:
```json
{
  "exc_type": "PermissionError",
  "exception": "frappe.exceptions.PermissionError",
  "_server_messages": "[\"You are not authorized to access this resource\"]"
}
```

HTTP status codes:
- `200` - Success
- `401` - Not authenticated (AuthenticationError)
- `403` - Not authorized (PermissionError)
- `404` - Resource not found (DoesNotExistError)
- `417` - Validation error (ValidationError)

---

## Critical Implementation Components

### 1. Type Generation System

**Script**: `scripts/generate-types.ts`

- Parse DocType JSON files from `/frappe_docker/development/frappe-bench/apps/siud/siud/siud/doctype/*/`
- Generate TypeScript interfaces for 8 DocTypes:
  - Supplier, Supplier Inquiry (main)
  - Activity Domain Category, Inquiry Topic Category (reference)
  - Contact Person, Supplier Role, Supplier Activity Domain, Contact Person Role (child tables)
- Map Frappe field types → TypeScript types
- Include validation metadata (required, options, field types)
- Run at build time: `npm run generate:types`

### 2. API Communication Layer

**File**: `src/api/client.ts`

- Base Frappe REST API wrapper using Axios
- Environment-aware configuration (reads `VITE_FRAPPE_API_URL` from `.env`)
- Authentication handling:
  - **Dev**: Session cookies via `POST /api/method/login`
  - **Prod**: JWT tokens in `Authorization` header
- Generic CRUD methods: `getList()`, `getDoc()`, `createDoc()`, `updateDoc()`, `deleteDoc()`
- Whitelisted method caller: `call(method, args)`
- Interceptors for auth token injection and 401 error handling
- CORS handling via Vite proxy in development

**Domain-specific APIs**:
- `src/api/supplier.ts` - Get current supplier, update profile
- `src/api/inquiry.ts` - List, get, create inquiries; get stats
- `src/api/reference.ts` - Fetch reference data

### 3. Authentication Flow

**File**: `src/stores/auth.ts`

- Pinia store for authentication state
- Actions: `login()`, `logout()`, `checkAuth()`
- State: `user`, `supplier`, `isAuthenticated`
- Router guards to protect routes
- User-to-Supplier linking via `User.supplier_link` field

### 4. Data Sync Strategy

**Build-time**:
- **Script**: `scripts/sync-reference-data.ts`
- Fetch Activity Domains, Inquiry Topics, Supplier Roles from Frappe
- Save as JSON to `public/data/`
- Embedded in build artifacts
- Loaded at app startup in reference store

**Runtime**:
- Current supplier details (via API)
- Inquiries list and details (via API)
- User profile (via API)
- Cache in Pinia stores with TTL-based refresh

### 5. Core Views

**DashboardView.vue**:
- Welcome header: "שלום, [supplier_name]"
- 3 stat cards: Total, Open, Closed inquiries
- Quick action buttons (New Inquiry, All Inquiries, Profile)
- Recent inquiries table (last 5)

**InquiryFormView.vue**:
- Topic category dropdown (from reference data)
- Inquiry description (textarea)
- Inquiry context (radio: ספק עצמו / מבוטח)
- Conditional fields: insured ID + name (if context = מבוטח)
- File attachments (Frappe upload API)
- Validation using DocType metadata

**InquiryListView.vue**:
- Table of all inquiries for current supplier
- Filters: status, date range
- Sorting by creation date
- Click to view detail

**ProfileView.vue**:
- Display supplier details
- Edit mode for: supplier_name, phone, email, address
- Call whitelisted method: `siud.www.supplier-profile.update_supplier_profile`

### 6. Hebrew RTL Support

- All templates use `dir="rtl"`
- Tailwind RTL plugin for directional utilities
- Rubik font (Google Fonts)
- Custom RTL overrides in `assets/styles/rtl.css`
- All labels and text in Hebrew

## Implementation Steps

### Phase 1: Foundation ✅ COMPLETED

1. **Project Setup** ✅
   - Create Vite + Vue 3 + TypeScript project: `npm create vite@latest supplier-portal-ui -- --template vue-ts`
   - Install dependencies: `frappe-ui`, `pinia`, `vue-router`, `axios`
   - Configure Tailwind with RTL plugin
   - Create `.env.development` (→ localhost:8000) and `.env.production` (→ Apigee URL)

2. **Type Generation** ✅
   - Write `scripts/generate-types.ts`
   - Parse all 8 DocType JSON files
   - Generate TypeScript interfaces
   - Test with `npm run generate:types`

3. **API Client** ✅
   - Implement `src/api/client.ts`
   - Configure Vite proxy for CORS bypass
   - Created domain-specific API modules (auth.ts, supplier.ts, inquiry.ts, reference.ts)
   - Created reference data sync script

**Phase 1 Deliverables:**
- Project scaffolded at `/home/tzvi/frappe/supplier-portal-ui/`
- 8 TypeScript interfaces generated from DocTypes
- Complete API layer with auth, supplier, inquiry, and reference modules
- Vite proxy configured for CORS bypass
- Basic Vue Router setup with placeholder views
- RTL/Hebrew localization configured
- Run `npm run dev` to start development server at http://localhost:5173

### Phase 2: Authentication & State ✅ COMPLETED

4. **Pinia Stores** ✅
   - Created `stores/auth.ts` - authentication state with login/logout, session persistence
   - Created `stores/reference.ts` - static reference data with caching and TTL
   - Created `stores/inquiry.ts` - inquiry state with pagination, stats, and form handling
   - Created `stores/index.ts` - barrel export for all stores

5. **Authentication Flow** ✅
   - Updated `LoginView.vue` to use auth store instead of direct API calls
   - Implemented async router guards with auth store integration
   - Added session persistence via localStorage flag + API verification
   - Added error state handling and display
   - Updated `DashboardView.vue` to display user/supplier info with logout

**Phase 2 Deliverables:**
- 3 Pinia stores (auth, reference, inquiry) with comprehensive state management
- Auth store with login(), logout(), initialize(), checkSession() methods
- Reference store with build-time JSON loading and API fallback
- Inquiry store with pagination, filtering, and form submission
- Router guards using async auth initialization
- Session persistence across page refreshes
- Updated type generation script with proper imports and exports
- Fixed TypeScript verbatimModuleSyntax compatibility
- Production build passes successfully

### Phase 3: Core Features ✅ COMPLETED

6. **Reference Data Sync** ✅ (Completed in Phase 1)
   - `scripts/sync-reference-data.ts` already exists
   - Reference store loads from `public/data/` at startup
   - Falls back to API if static files unavailable

7. **Dashboard** ✅
   - Built `DashboardView.vue` with welcome section, stats cards, quick actions
   - Created `StatCard.vue` component with loading states
   - Fetches inquiry stats from API on mount
   - Displays recent inquiries table with navigation

8. **Inquiry Management** ✅
   - Built `InquiryListView.vue` with filters (status, date range) and pagination
   - Built `InquiryTable.vue` component for reusable table display
   - Built `InquiryDetailView.vue` with full inquiry info, attachments, and response display
   - Built `InquiryFormView.vue` with topic selection, context-dependent fields, file upload
   - File upload using Frappe's upload API with drag-and-drop UI

9. **Profile Management** ✅
   - Built `ProfileView.vue` with supplier details display
   - Editable fields: supplier_name, phone, email, address
   - Read-only display of activity domains and contact persons
   - Inline edit mode with form validation and save functionality

10. **Layout & UI** ✅
    - Built `AppHeader.vue` with navigation and user menu
    - Built `MainLayout.vue` wrapper for authenticated routes
    - Created common components: `LoadingSpinner.vue`, `EmptyState.vue`, `StatusBadge.vue`
    - Responsive design with Tailwind CSS
    - Hebrew RTL styling throughout

**Phase 3 Deliverables:**
- Complete Dashboard with stats, quick actions, and recent inquiries
- Full Inquiry CRUD: list with filters/pagination, detail view, create form with file upload
- Profile view with inline editing and save
- Reusable components: StatCard, LoadingSpinner, EmptyState, StatusBadge, InquiryTable
- App layout with navigation header and responsive mobile support
- All views have loading states, error handling, and empty states
- Production build passes successfully (`npm run build`)

### Phase 4: Polish & Testing ✅ COMPLETED

11. **Testing** ✅
    - Manual testing of all API endpoints
    - Authentication flow tested (login, logout, session persistence)
    - Dashboard with stats and recent inquiries verified
    - Inquiry CRUD operations tested (list, detail, create with attachments)
    - Profile view and editing tested
    - Mobile responsive design verified (Tailwind breakpoints working)

12. **Bug Fixes Applied** ✅
    - Fixed field name mismatches in supplier_portal.py API:
      - Changed `description` → `inquiry_description`
      - Changed `insured_id` → `insured_id_number`
      - Changed `insured_name` → `insured_full_name`
    - Updated inquiry status values to match DocType options:
      - New statuses: פנייה חדשה התקבלה, מיון וניתוב, בטיפול, דורש השלמות / המתנה, נסגר – ניתן מענה, סגור
    - Regenerated reference data with correct status values

**Phase 4 Deliverables:**
- All API endpoints tested and working
- Authentication flow verified with test supplier user
- Inquiry lifecycle tested (create, view, list with filters)
- Profile editing works (note: phone field requires valid format)
- Reference data synced with correct status values
- Production build passes successfully
- Mobile responsive classes verified in all views

**Test Credentials:**
- Email: `supplier1@test.com`
- Password: `Test123`
- Linked Supplier: `SUP-TEST-001`

### Phase 5: Deployment Prep

13. **Build & Deploy**
    - Optimize Vite build configuration
    - Test production build locally
    - Write deployment documentation
    - Set up hosting (Netlify/Vercel/AWS)

## Development Workflow

### Local Setup

```bash
cd /home/tzvi/frappe
npm create vite@latest supplier-portal-ui -- --template vue-ts
cd supplier-portal-ui
npm install frappe-ui pinia vue-router axios
npm install -D tailwindcss postcss autoprefixer tailwindcss-rtl tsx

# Create environment files
echo "VITE_FRAPPE_API_URL=http://localhost:8000" > .env.development
echo "VITE_AUTH_MODE=session" >> .env.development

# Generate types and reference data
npm run generate:types
npm run generate:reference

# Start dev server
npm run dev
```

### Development Server

- **UI**: http://localhost:5173
- **Frappe API**: http://localhost:8000
- **CORS**: Handled by Vite proxy configuration

### Build Scripts

```json
{
  "scripts": {
    "generate:types": "tsx scripts/generate-types.ts",
    "generate:reference": "tsx scripts/sync-reference-data.ts",
    "prebuild": "npm run generate:types && npm run generate:reference",
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Security Considerations

- **XSS**: Vue auto-escapes template content; use `v-html` only for trusted content
- **CSRF**: Frappe handles CSRF for session-based auth
- **Input Validation**: Client-side for UX; server-side (Frappe) for security
- **File Uploads**: Validate file types and size; use Frappe's upload API
- **Token Storage**: `localStorage` for JWT (prod); HttpOnly cookies (dev)
- **HTTPS**: Enforce in production
- **Rate Limiting**: Handled by Apigee in production

## Future Enhancements (Post-MVP)

- **User Management**: Implement proper external user registration and role-based permissions
- **Notifications**: Email/push notifications for inquiry status changes
- **Multi-language**: Support English and Arabic in addition to Hebrew
- **Offline Support**: Service Worker + IndexedDB for offline drafts
- **Analytics**: Track user behavior and usage metrics
- **Unit Tests**: Vitest + @vue/test-utils
- **E2E Tests**: Playwright or Cypress
- **Accessibility**: WCAG 2.1 compliance, screen reader support

## Dependencies

**Core**:
- `vue@^3.4.0` - Framework
- `vue-router@^4.2.0` - Routing
- `pinia@^2.1.0` - State management
- `frappe-ui@latest` - UI component library
- `axios@^1.6.0` - HTTP client

**Dev**:
- `vite@^5.0.0` - Build tool
- `typescript@^5.3.0` - Type checking
- `tailwindcss@^3.4.0` - Styling
- `tailwindcss-rtl@^0.9.0` - RTL support
- `tsx@^4.7.0` - TypeScript execution (for scripts)

## Critical Files

1. **`src/api/client.ts`** - Core API layer; handles all Frappe communication
2. **`scripts/generate-types.ts`** - Type generation; ensures type safety
3. **`src/stores/auth.ts`** - Authentication state; controls access
4. **`src/views/DashboardView.vue`** - Main view; integration example
5. **`vite.config.ts`** - Build config; environment handling, proxy setup
6. **`scripts/sync-reference-data.ts`** - Reference data sync at build time
7. **`src/views/InquiryFormView.vue`** - Complex form with validation and file upload

## Notes

- **MVP Scope**: Focus on replicating existing portal functionality (dashboard, inquiries, profile)
- **User Management**: Deferred to post-MVP; use test users initially
- **Apigee Integration**: Architecture supports it; activate in production by changing `.env.production`
- **Schema Evolution**: Re-run `npm run generate:types` when DocTypes change
- **File Uploads**: Use Frappe's `/api/method/upload_file` endpoint
- **Permissions**: Frappe's existing `has_website_permission()` logic applies
