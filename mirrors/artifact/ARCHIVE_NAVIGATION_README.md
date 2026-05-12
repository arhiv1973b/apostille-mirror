# Archive Navigation & 404 Handling System

**Status:** ✅ COMPLETE | Generated: 29.03.2026

---

## 📋 Overview

This system provides:

1. **Universal HTML Template** (`layout/wrapper.html`) - SSG wrapper for static content delivery
2. **Automatic Index Generation** (`archive_sync.sh`) - Creates index.html for all directories
3. **404 Error Handler** (`404.html`) - Intelligent error navigation with sitemap links
4. **Complete Sitemap** (`sitemap.html`) - Full archive structure and search

---

## 🎯 Key Components

### 1. Layout Template (`layout/wrapper.html`)
- Universal wrapper for all pages
- Breadcrumb navigation
- Directory browsing
- File listing
- Responsive design

**Usage:**
```html
<!-- Include or reference from any directory -->
<link rel="stylesheet" href="/layout/wrapper.html">
```

### 2. Archive Synchronization (`archive_sync.sh`)
- Scans all directories (max depth 4)
- Generates `index.html` automatically
- Prevents overwriting existing indices
- Logs generation results

**Run:**
```bash
bash archive_sync.sh
```

### 3. Error Handler (`404.html`)
- Shows current path
- Provides quick navigation buttons
- Links to sitemap
- Suggests archive structure

**Triggered by:** Invalid URL paths on GitHub Pages

### 4. Sitemap (`sitemap.html`)
- Complete file listing
- Searchable content
- Directory tree visualization
- Quick access to key documents

**Location:** `/sitemap.html`

---

## 📁 Directory Structure

```
apostille-legal-case/
├── layout/
│   └── wrapper.html            ← Universal template
├── docs/
│   ├── evidence/
│   ├── legal/
│   └── diplomacy/
├── evidence/
│   ├── identity/
│   ├── audit/
│   └── (85+ PDF files)
├── bot_audit/
├── instant_access_texts/
│
├── index.html                   ← Main portal (generated)
├── 404.html                     ← Error handler (generated)
├── sitemap.html                 ← Archive map (generated)
├── archive_sync.sh              ← Synchronization script
├── _config.yml                  ← GitHub Pages config
└── _headers                     ← Security headers
```

---

## 🔄 Automatic Index Generation

The `archive_sync.sh` script:
1. Traverses repository recursively
2. Skips hidden dirs (.git, node_modules)
3. Creates `index.html` for each directory
4. Replaces placeholders (timestamp, file count)

**Result:** Every directory becomes browsable

---

## 🛡️ Error Handling

### 404 → Navigation Flow

```
User requests invalid path
         ↓
GitHub Pages returns 404.html
         ↓
404 page shows:
├─ Current path
├─ Quick navigation buttons
├─ Archive structure
└─ Links to sitemap
         ↓
User can navigate to content
```

### 404 Features
- ✅ Shows attempted path
- ✅ Quick access buttons (6 main dirs)
- ✅ Archive structure hints
- ✅ Link to sitemap

---

## 🔍 Sitemap Features

### Navigation
- 📍 Complete file tree
- 🔍 Search functionality
- 📊 Archive statistics
- 💡 Navigation tips

### Quick Links
- Root resources
- Main collections
- Legal documents
- Deployment files
- Evidence & proofs

---

## 🔐 Data Integrity

✅ **No file content modified** - Only navigation layer added
✅ **No file deletion** - All original files preserved
✅ **No file moving** - Structure unchanged
✅ **Pure HTML/CSS/JS** - No backend required

---

## 📊 Implementation Checklist

- [x] `layout/wrapper.html` created
- [x] `archive_sync.sh` written
- [x] `404.html` configured
- [x] `sitemap.html` generated
- [x] `_config.yml` updated
- [x] Security headers configured
- [x] Breadcrumb navigation added
- [x] Mobile responsiveness ensured
- [x] Search functionality included
- [x] Error handling active

---

## 🚀 Deployment

### Local Testing
```bash
# Make script executable
chmod +x archive_sync.sh

# Generate indices
./archive_sync.sh

# View results
open 404.html
open sitemap.html
```

### GitHub Pages
```bash
git add layout/ 404.html sitemap.html archive_sync.sh
git commit -m "infrastructure: add archive navigation layer and 404 handling"
git push origin master
```

### Configuration
GitHub Pages will automatically:
1. Serve `404.html` for missing pages
2. Process `_config.yml` settings
3. Apply security headers from `_headers`
4. Generate dynamic indices

---

## ✅ Verification

### Test Cases

1. **Valid path:** `/evidence/` → Shows directory with links
2. **Invalid path:** `/invalid/path/` → Shows 404 with navigation
3. **Root:** `/` → Shows main index with collections
4. **Sitemap:** `/sitemap.html` → Shows complete file tree
5. **Search:** Sitemap search bar filters content

---

## 📞 Support

If you encounter 404s:
1. Check `/sitemap.html` for directory listing
2. Navigate using `/404.html` quick buttons
3. Use search in sitemap
4. Verify file exists in `/evidence/` or `/docs/`

---

**Status:** ✅ Complete | Ready for production

Generated: 29.03.2026 | All 404 errors now redirect to intelligent navigation system.
