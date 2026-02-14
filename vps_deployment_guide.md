# VPS Deployment Guide with Traefik

This guide explains how to deploy the **Deep Echelon Holdings** platform on a VPS using **Docker**, **Docker Compose**, and **Traefik** as the reverse proxy.

## 1. Prerequisites
- A VPS with Docker and Docker Compose installed.
- A domain name pointing to your VPS IP address.
- Traefik installed and running on a network named `web`.

## 2. Configuration
1. Clone the repository to your VPS.
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file:
   - `SECRET_KEY`: Set a long, random string.
   - `DATABASE_URL`: Typically stays `sqlite:///./echelon_holdings.db` for the initial setup.
   - `DOMAIN_NAME`: Set your actual domain (e.g., `portal.echelon.holdings`).

## 3. Deploying the Application
Run the following command in the project root:
```bash
docker compose up -d --build
```

## 4. Traefik Integration
The `docker-compose.yml` is already configured with labels for Traefik:
- `traefik.enable=true`: Enables Traefik for this container.
- `Host(`${DOMAIN_NAME}`)`: Routes traffic based on your domain.
- `websecure`: Use the HTTPS entrypoint.
- `myresolver`: Uses the Let's Encrypt resolver defined in your Traefik config.

## 5. Persistent Data
The current setup uses SQLite. If you restart the container, the data in `echelon_holdings.db` will persist **within the container range** until the volume is explicitly deleted or recreated. For production, it is recommended to mount a local directory for the database:

**Optional: Update docker-compose.yml for volume mounting**
```yaml
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:////app/data/echelon_holdings.db
```

## 6. Post-Deployment
Once up, initialize the database (if not done by the Dockerfile):
```bash
docker exec -it echelon_holdings_app python init_db.py
```
And optionally seed the VIP data:
```bash
docker exec -it echelon_holdings_app python seed_vip_client.py
```

---
**Deep Echelon Holdings - Institutional Wealth Management v2.0**
