# 🚀 Quick Deployment Reference

## Step 1: Prepare for Render.com Deployment

### Before deploying, ensure:
- [ ] `.env` file is configured (copy from `.env.example`)
- [ ] `SECRET_KEY` in `.env` is set to a strong random value
- [ ] GitHub repository is updated with all changes
- [ ] `requirements.txt` has all dependencies
- [ ] Database export generated (for backup/migration)

### Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Step 2: Local Production Testing

Test the application locally with Gunicorn (production-like environment):

```bash
python scripts/run_local_production.py
```

Then visit: http://127.0.0.1:8000

---

## Step 3: Deploy to Render.com

### Option A: Via Render Dashboard
1. Go to https://dashboard.render.com/web/new
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: (auto-read from Procfile)
4. Add Environment Variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=<your-secure-key>
   DATABASE_URL=<postgresql://... or leave empty if using DB_* vars>
   ```
5. Click Deploy

### Option B: Via Render CLI
```bash
# Install Render CLI
npm install -g @render-com/cli

# Deploy
render deploy
```

---

## Step 4: Database Migration

### For FreeHostia MySQL Deployment:

1. **Export database:**
   ```bash
   python scripts/export_db_mysql.py
   ```
   Creates: `database_export_sammor96_sammor96_YYYYMMDD_HHMMSS.sql`

2. **Import to FreeHostia:**
   - Access FreeHostia Control Panel
   - Open phpMyAdmin
   - Create database: `sammor96_sammor96_`
   - Import SQL file into new database
   - Update `.env` with database credentials

### For Render PostgreSQL:
- Render creates DATABASE_URL automatically
- Application uses it by default in production

---

## Step 5: Verify Deployment

After deployment:
1. Check Render logs: https://dashboard.render.com
2. Visit your app URL: `https://your-app-name.onrender.com`
3. Test admin login: `/login`
4. Check dashboard: `/dashboard_admin`
5. Monitor logs for errors

---

## Environment Variables Cheat Sheet

| Variable | Value | Notes |
|----------|-------|-------|
| `FLASK_ENV` | `production` | Required for production |
| `SECRET_KEY` | random(32) | Generate with command above |
| `DATABASE_URL` | postgresql://... | Render provides if PostgreSQL |
| `DB_NAME` | sammor96_sammor96_ | If using MySQL |
| `DB_USER` | your_user | MySQL username |
| `DB_PASSWORD` | your_pass | MySQL password |
| `DB_HOST` | host.com | MySQL hostname |
| `DB_PORT` | 3306 | MySQL port (optional) |

---

## Troubleshooting

### App won't start on Render
- Check logs in dashboard
- Verify SECRET_KEY is set
- Ensure DATABASE_URL format is correct
- Confirm Python version in runtime.txt

### Database connection fails
- Verify DB credentials in .env
- Check IP whitelist in database service
- Ensure database exists and is accessible

### Static files not loading
- Verify `app/static/` directory exists
- Check file paths in templates use correct URLs

---

## Files Created for Deployment

```
rbac-flask/
├── Procfile                              # Gunicorn startup config
├── runtime.txt                           # Python version
├── DEPLOYMENT.md                         # Full deployment guide
├── .env.example                          # Environment template
├── database_export_sammor96_sammor96_*.sql  # Database backup
├── scripts/
│   ├── export_db_mysql.py               # Database export tool
│   └── run_local_production.py           # Local production test
└── requirements.txt                      # Dependencies (updated)
```

---

## Next Steps

1. ✅ Local testing with: `python scripts/run_local_production.py`
2. ✅ Push code to GitHub
3. ✅ Connect GitHub to Render dashboard
4. ✅ Configure environment variables in Render
5. ✅ Deploy
6. ✅ Monitor and troubleshoot in Render logs

---

**For detailed information, see DEPLOYMENT.md**
