# 📦 Deployment Guide - Flask RBAC Application

## Quick Start: Render.com Deployment

### 1. Prerequisites
- GitHub repository with this code
- Render.com account (https://render.com)
- Database prepared (PostgreSQL on Render or MySQL on FreeHostia)

### 2. Steps to Deploy on Render.com

#### Step 1: Create a Web Service
1. Go to https://dashboard.render.com/web/new
2. Connect your GitHub repository
3. Select the branch to deploy

#### Step 2: Configure Environment
- **Name**: Choose a service name
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: Already configured in `Procfile`

#### Step 3: Set Environment Variables
In the Render dashboard, add these environment variables:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-secure-random-key>
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
```

The `DATABASE_URL` will be provided by Render if you create a PostgreSQL database, or use your external MySQL database.

#### Step 4: Deploy
- Click "Deploy"
- Monitor logs in the Render dashboard
- Application will be available at `https://your-app-name.onrender.com`

---

## Alternative: FreeHostia MySQL Deployment

### 1. Prepare Database
1. Export the database using provided SQL dump file
2. Access FreeHostia control panel
3. Import SQL into database `sammor96_sammor96_`

### 2. Configure .env
```
DB_NAME=sammor96_sammor96_
DB_USER=<your_freehostia_user>
DB_PASSWORD=<your_freehostia_password>
DB_HOST=<your_freehostia_host>
SECRET_KEY=<secure-random-key>
```

### 3. Deploy Application
Use your preferred hosting method (cPanel, FTP, etc.)

---

## Local Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File
Copy `.env.example` to `.env` and fill in values

### 3. Run Locally
```bash
python app.py
```
App runs at `http://127.0.0.1:5000`

### 4. Test with Gunicorn (Production-like)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
App runs at `http://127.0.0.1:8000`

---

## Project Structure

```
rbac-flask/
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Procfile              # Render.com deployment configuration
├── runtime.txt           # Python version specification
├── .env.example          # Environment variables template
├── DEPLOYMENT.md         # This file
├── app/
│   ├── __init__.py
│   ├── models.py        # Database models
│   ├── extensions.py    # Flask extensions
│   ├── decorators.py    # Custom decorators
│   ├── auth/            # Authentication routes
│   ├── main/            # Main routes
│   ├── profesor/        # Professor routes
│   ├── templates/       # HTML templates
│   └── static/          # CSS and assets
└── instance/
    └── app.db           # SQLite database (development)
```

---

## Environment Variables Reference

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `FLASK_ENV` | Yes | Flask environment mode | `production` or `development` |
| `SECRET_KEY` | Yes | Session encryption key | `your-secure-random-string` |
| `DATABASE_URL` | Optional* | PostgreSQL connection (Render) | `postgresql://user:pass@host:5432/db` |
| `DB_NAME` | Optional* | MySQL database name | `sammor96_sammor96_` |
| `DB_USER` | Optional* | MySQL username | `sammor96_user` |
| `DB_PASSWORD` | Optional* | MySQL password | `your_password` |
| `DB_HOST` | No | MySQL host | `127.0.0.1` or hostname |
| `DB_PORT` | No | MySQL port | `3306` |

*Either `DATABASE_URL` or `DB_NAME`/`DB_USER` must be provided

---

## Troubleshooting

### Application won't start on Render
1. Check logs in Render dashboard
2. Verify `FLASK_ENV=production` is set
3. Ensure `SECRET_KEY` is not empty
4. Confirm database connection variables are correct

### Database connection errors
- Verify DATABASE_URL format is correct
- For PostgreSQL: `postgresql://user:pass@host:port/dbname`
- For MySQL: Use `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`

### Port issues
- Render uses `$PORT` environment variable (automatically injected)
- Procfile already handles this: `--bind 0.0.0.0:$PORT`
- Local testing: Use port 8000 with Gunicorn

### Static files not loading
- Ensure `app/static/` directory exists
- Check file permissions
- Verify paths in templates

---

## Database Export

To export the current SQLite database to MySQL format for FreeHostia:

```bash
python scripts/export_db_mysql.py
```

This creates a `.sql` file ready for import into FreeHostia's phpMyAdmin.

---

## Support

For issues:
1. Check `DEPLOYMENT.md` (this file)
2. Review Render.com documentation: https://render.com/docs
3. Check Flask documentation: https://flask.palletsprojects.com
4. Review database logs for connection issues

---

**Last Updated**: May 2026
**Compatible with**: Python 3.11+, Gunicorn 22.0.0+
