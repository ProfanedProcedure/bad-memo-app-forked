# Repository Instructions for GitHub Copilot Coding Agent

## Repository Overview

This is a **Django-based memo application** intentionally designed as a teaching tool for learning code refactoring and security best practices with GitHub Copilot. The repository contains deliberate bugs, security vulnerabilities, and code smells for educational purposes.

**Important:** This is a teaching repository with intentional security vulnerabilities (e.g., SQL injection, unsafe input handling). Do NOT deploy to production or publicly accessible environments.

### High-Level Details
- **Type:** Django web application (Python)
- **Purpose:** Educational refactoring lab demonstrating common security issues and code quality problems
- **Language:** Python 3.12+ with Django 4.2+
- **Size:** Small (~15 Python files, 4 HTML templates)
- **Database:** SQLite (development)
- **Main Components:**
  - Django app for creating, listing, editing, and deleting memos
  - Tag system with many-to-many relationships
  - Search functionality (intentionally vulnerable)

## Environment Setup and Build Instructions

### Prerequisites
- Python 3.12+ (project uses Python 3.12.3)
- Virtual environment tool (venv)

### Setup Steps (Always follow in order)

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Dependencies: Django>=4.2,<5.0, python-dotenv>=1.0.0

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
   Must run after fresh clone or any model changes.

4. **Load sample data (optional but recommended for testing):**
   ```bash
   python manage.py loaddata memos/fixtures/sample.json
   ```

### Running the Application

```bash
python manage.py runserver
```
Access at: http://127.0.0.1:8000/

### Testing

**Always run tests before and after making changes:**
```bash
python manage.py test
```

Tests are located in `memos/tests/`:
- `test_views.py` - View functionality tests (7 tests)
- `test_models.py` - Model tests

Expected output: All tests should pass (7 tests, ~0.03s)

### Validation Steps

There are no automated linters or CI pipelines configured. Manual validation:
1. Run tests: `python manage.py test`
2. Start server and verify no crashes
3. Test basic functionality: list, create, edit, delete memos
4. Check database migrations: `python manage.py makemigrations --check --dry-run`

## Project Layout and Architecture

### Directory Structure

```
/home/runner/work/bad-memo-app-forked/bad-memo-app-forked/
├── .github/                    # GitHub configuration
│   └── copilot-instructions.md # This file
├── .venv/                      # Virtual environment (excluded from git)
├── memo_project/               # Django project settings
│   ├── settings.py            # Main Django configuration
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI configuration
├── memos/                      # Main Django app
│   ├── migrations/            # Database migrations
│   ├── tests/                 # Test files
│   │   ├── test_models.py
│   │   └── test_views.py
│   ├── fixtures/              # Test data
│   │   └── sample.json
│   ├── models.py              # Memo and Tag models
│   ├── views.py               # View functions (intentionally problematic)
│   ├── utils.py               # Helper functions
│   └── admin.py               # Django admin configuration
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   └── memos/                 # Memo-specific templates
│       ├── memo_list.html
│       ├── memo_detail.html
│       └── memo_form.html
├── static/                     # Static files (CSS, JS, images)
├── tools/                      # Utility scripts
│   └── export_memos.py        # Export script (needs refactoring)
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                   # Setup and overview (in Japanese)
├── BUG_CATALOG.md             # List of intentional bugs (in Japanese)
├── TEACHING_PLAN.md           # Teaching guide (in Japanese)
└── WORKSHEET.md               # Student checklist (in Japanese)
```

### Key Files

- **`memos/views.py`**: Contains all view logic with intentional vulnerabilities:
  - SQL injection in `memo_list()` search (legacy=1 parameter)
  - Missing pagination
  - DELETE method not restricted to POST
  - Duplicated code between create/edit
  
- **`memos/models.py`**: Defines `Memo` and `Tag` models
  - `Memo`: title, body, tags (M2M), created_at, updated_at
  - `Tag`: name (unique)
  - Method `attach_tags_from_csv()` has poor error handling

- **`memos/utils.py`**: Helper functions for input normalization and sorting

- **`memo_project/settings.py`**: Django configuration (SECRET_KEY from .env)

### Known Issues (Intentional for Teaching)

**Security Issues:**
1. ★★★ SQL injection in search (`memo_list()` with `legacy=1` or default search)
2. ★★ DELETE not restricted to POST method
3. ★ Unsafe input in `order_by()` with `unsafe_sort=1`

**Performance Issues:**
1. ★★ No pagination on memo list
2. ★★ N+1 queries (missing `prefetch_related("tags")`)

**Code Quality Issues:**
1. ★★ Duplicated code between `create_memo()` and `edit_memo()`
2. ★★ No Django Form usage (manual validation)
3. ★★ Poor tag handling in `attach_tags_from_csv()`
4. ★ Export script needs improvement

See `BUG_CATALOG.md` for complete list with difficulty ratings.

## Making Changes

### When Working on This Repository

1. **Always activate virtual environment first**
2. **Run tests before making changes** to establish baseline
3. **Make minimal changes** - this is teaching material, preserve intentional issues unless specifically fixing them
4. **Run tests after changes** to verify nothing broke
5. **Test manually** by running the server and exercising changed functionality

### Common Workflows

**Adding a new view:**
1. Add function to `memos/views.py`
2. Add URL pattern to `memos/urls.py` (if exists) or `memo_project/urls.py`
3. Create template in `templates/memos/`
4. Add test to `memos/tests/test_views.py`
5. Run tests

**Modifying models:**
1. Edit `memos/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Update tests if needed
5. Run tests

**Security fixes:**
- Replace raw SQL with ORM queries
- Use parameterized queries if raw SQL is necessary
- Add input validation with allowed lists
- Restrict HTTP methods (use `require_http_methods` decorator)
- Use `get_object_or_404()` instead of `Model.objects.get()`

## Dependencies and Configuration

**Python Dependencies (requirements.txt):**
- Django>=4.2,<5.0
- python-dotenv>=1.0.0

**Environment Variables (.env file, optional):**
- `SECRET_KEY`: Django secret key (has default in settings.py)

**Database:**
- SQLite database stored as `db.sqlite3` (excluded from git)
- Auto-created on first migration

**Static Files:**
- Located in `static/` directory
- No collection/compilation needed for development

## Best Practices for This Repository

1. **Understand the teaching context**: Many "bad practices" are intentional
2. **Don't remove teaching examples** unless explicitly asked
3. **Add comments** when fixing vulnerabilities to explain what was wrong
4. **Write tests** for any new functionality
5. **Keep it simple**: This is teaching material, avoid over-engineering
6. **Document security fixes**: Explain why the original code was problematic
7. **Preserve Japanese documentation**: README, BUG_CATALOG, etc. are in Japanese for the target audience

## Common Pitfalls

1. **Forgetting to activate virtual environment** - commands will fail or use wrong Python
2. **Not running migrations** after model changes - database schema won't match code
3. **Running server without migrations** - will crash on database access
4. **Modifying intentional bugs** without understanding their educational purpose
5. **Adding complex frameworks** - keep solutions simple for teaching clarity
