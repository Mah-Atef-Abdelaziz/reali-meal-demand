# REAL.i — Production Deployment Guide

This guide describes how to deploy the **REAL.i Meal Demand AI & Smart Assistant** platform to a production Linux VPS or Cloud Instance (e.g. AWS EC2, GCP Compute Engine, Ubuntu 22.04 LTS).

---

## 1. Database Migrations (PostgreSQL Transition)

### A. Update environment configurations
Set your production PostgreSQL credentials in `backend/.env`:
```env
DATABASE_URL="postgresql+asyncpg://<db_user>:<db_password>@<db_host>:5432/<db_name>"
DATABASE_SYNC_URL="postgresql://<db_user>:<db_password>@<db_host>:5432/<db_name>"
```

### B. Generate & Run migrations
Alembic has been pre-configured in this repository. To run migrations and generate/update schemas:
```bash
# 1. Initialize migration revisions (dynamically autodetects ORM structures)
python -m alembic revision --autogenerate -m "Initial schema"

# 2. Apply migrations to the PostgreSQL database
python -m alembic upgrade head
```

---

## 2. CI/CD Pipeline Configuration
GitHub Actions are configured in `.github/workflows/ci.yml`. This pipeline:
1. **Runs Pytest Backend Unit Tests** on every push/PR.
2. **Runs Next.js Linting & Type Checks**.
3. **Builds & Pushes multi-stage Docker Images** to GitHub Packages (GHCR) or your private container registry.

To deploy via CI/CD, add the following secrets to your GitHub repository (**Settings > Secrets and variables > Actions**):
* `REGISTRY_HOST`: Container registry hostname (defaults to `ghcr.io`).
* `REGISTRY_TOKEN`: Personal Access Token with write permissions to publish package images.

---

## 3. Server Deployment (No-Docker Setup)

If you are deploying directly onto a Linux machine instead of using Docker:

### A. Clone and Set Up Virtual Environment
```bash
cd /var/www
git clone <your-repo-url> reali
cd reali

# Set up backend virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### B. Configure systemd Service for FastAPI
1. Copy the systemd service file:
   ```bash
   sudo cp deployment/reali-backend.service /etc/systemd/system/reali-backend.service
   ```
2. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable reali-backend.service
   sudo systemctl start reali-backend.service
   ```
3. Check backend status:
   ```bash
   sudo systemctl status reali-backend.service
   ```

### C. Build and Serve Next.js Frontend
1. Install Node.js 20 and PM2:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   sudo npm install --global pm2
   ```
2. Build and launch Next.js using PM2 process manager:
   ```bash
   cd /var/www/reali/frontend
   npm ci --legacy-peer-deps
   npm run build
   pm2 start npm --name "reali-frontend" -- start
   pm2 save
   pm2 startup
   ```

### D. Set Up Nginx Reverse Proxy & SSL (HTTPS)
1. Install Nginx and Certbot (Let's Encrypt):
   ```bash
   sudo apt update
   sudo apt install nginx certbot python3-certbot-nginx -y
   ```
2. Copy the Nginx config:
   ```bash
   sudo cp ../deployment/nginx.conf /etc/nginx/sites-available/reali.conf
   sudo ln -s /etc/nginx/sites-available/reali.conf /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   ```
3. Validate Nginx configurations and restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```
4. Obtain and install SSL certificates:
   ```bash
   sudo certbot --nginx -d reali.yourdomain.com
   ```
   *(Certbot will automatically update `nginx.conf` with the SSL configurations.)*
