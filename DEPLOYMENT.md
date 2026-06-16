# Deployment Guide for Air Drawing Web App

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Environment Variables](#environment-variables)

---

## Local Development

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/SnehaKumariArya/air-drawing.git
cd air-drawing
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements-web.txt
```

4. **Run Flask development server:**
```bash
python app.py
```

5. **Access the app:**
Open browser and go to: `http://localhost:5000`

---

## Docker Deployment

### Build and Run Locally

1. **Build Docker image:**
```bash
docker build -t air-drawing:latest .
```

2. **Run container:**
```bash
docker run -p 5000:5000 -v $(pwd)/drawings:/app/drawings air-drawing:latest
```

3. **Access the app:**
Open browser and go to: `http://localhost:5000`

### Using Docker Compose

1. **Start services:**
```bash
docker-compose up --build
```

2. **Stop services:**
```bash
docker-compose down
```

---

## Cloud Deployment

### Option 1: Render (Recommended - Free Tier Available)

1. **Create Render account:**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select `air-drawing` repository

3. **Configure Service:**
   - **Name:** `air-drawing`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements-web.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app`
   - **Plan:** Free or Paid

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Heroku

1. **Install Heroku CLI:**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows - Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku:**
```bash
heroku login
```

3. **Create Heroku app:**
```bash
heroku create air-drawing
```

4. **Deploy:**
```bash
git push heroku main
```

5. **View logs:**
```bash
heroku logs --tail
```

### Option 3: Google Cloud Run

1. **Create Google Cloud project:**
   - Go to https://console.cloud.google.com
   - Create new project

2. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
```

3. **Deploy:**
```bash
gcloud run deploy air-drawing \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 4: AWS (EC2 or ECS)

**EC2 Deployment:**

1. Create EC2 instance (Ubuntu 20.04)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

4. Clone repository and setup:
```bash
git clone https://github.com/SnehaKumariArya/air-drawing.git
cd air-drawing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-web.txt
```

5. Run with gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

6. Setup Nginx as reverse proxy (optional but recommended)

---

## Environment Variables

Create `.env` file for local development:

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py
```

For production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## Important Notes

### Webcam Access

- **Local Development:** Works with local camera
- **Docker:** May need device mapping: `--device /dev/video0:/dev/video0`
- **Cloud (Render/Heroku/GCP/AWS):** **No local webcam access**
  - Users must allow browser camera access
  - HTTPS required for camera access in browser
  - Some cloud platforms may restrict camera/device access

### Browser Compatibility

- Chrome/Chromium: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Edge: ✅ Full support

**Note:** Camera access requires HTTPS in production (except localhost)

### Performance Considerations

1. **Single Worker:** App uses 1 worker by default (for webcam access)
2. **Timeout:** Set to 120 seconds for processing
3. **Memory:** Requires ~200MB+ for MediaPipe and OpenCV
4. **CPU:** Recommend 1-2 vCPU minimum

### Troubleshooting

**Camera not working:**
- Check browser permissions
- Ensure HTTPS in production
- Verify camera hardware

**Slow performance:**
- Check internet speed
- Verify cloud instance specs
- Check browser console for errors

**Port issues:**
- Ensure port 5000 is not in use
- Cloud platforms may auto-assign ports

---

## Monitoring & Logs

### Local Logs
```bash
# View Flask logs
python app.py  # Logs appear in terminal
```

### Docker Logs
```bash
docker logs <container-id>
```

### Render Logs
- View in Render dashboard → Services → Your App → Logs

### Heroku Logs
```bash
heroku logs --tail
```

---

## Quick Start Commands

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-web.txt
python app.py
```

### Docker Local
```bash
docker build -t air-drawing:latest .
docker run -p 5000:5000 air-drawing:latest
```

### Docker Compose
```bash
docker-compose up --build
```

---

## Support

For issues or questions:
- Check GitHub Issues
- Review logs
- Verify browser compatibility
- Test with different cameras/devices
