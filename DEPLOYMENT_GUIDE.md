# Deployment Guide - AOM Screening Application

This guide will help you deploy your application to **Render** (backend) and **Vercel** (frontend) so it can be accessed from anywhere, including your phone on cellular data.

## Prerequisites

1. **GitHub Account** - Sign up at https://github.com
2. **Render Account** - Sign up at https://render.com (free tier available)
3. **Vercel Account** - Sign up at https://vercel.com (free tier available)

## Step 1: Push Code to GitHub

### 1.1 Create a new repository on GitHub

1. Go to https://github.com/new
2. Repository name: `aom-screening-app`
3. Description: "Anti-Obesity Medications Screening Application"
4. Set to **Public** or **Private** (both work with free tiers)
5. **DO NOT** initialize with README (we already have code)
6. Click "Create repository"

### 1.2 Push your local code to GitHub

```bash
cd /Users/yawenwang/aom-screening-app

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/aom-screening-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

You'll be prompted for GitHub credentials. If you have 2FA enabled, you'll need to use a Personal Access Token instead of your password.

## Step 2: Deploy Backend to Render

### 2.1 Create Render account and connect GitHub

1. Go to https://render.com
2. Sign up using your GitHub account (easiest option)
3. Authorize Render to access your GitHub repositories

### 2.2 Create a new Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your `aom-screening-app` repository
3. Configure the service:
   - **Name**: `aom-screening-backend`
   - **Region**: Choose closest to your location
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### 2.3 Add Environment Variables

In the Render dashboard for your service, go to "Environment" tab and add:

```
ENVIRONMENT=production
SECRET_KEY=<click "Generate" to create a secure random key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://*.vercel.app,http://localhost:5173
```

### 2.4 Create PostgreSQL Database (Optional - Free 90 days)

1. Click **"New +"** → **"PostgreSQL"**
2. **Name**: `aom-screening-db`
3. **Database**: `aom_screening`
4. **User**: `aom_user`
5. **Region**: Same as your web service
6. **Instance Type**: `Free`
7. Click "Create Database"

### 2.5 Connect Database to Web Service

1. Go back to your web service
2. In "Environment" tab, add:
   ```
   DATABASE_URL=<copy Internal Database URL from your PostgreSQL database>
   ```

### 2.6 Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Wait for deployment to complete (5-10 minutes)
4. **Copy your backend URL**: `https://aom-screening-backend.onrender.com`

> **Note**: Free tier services sleep after 15 minutes of inactivity. First request after sleep takes 30-60 seconds.

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel account

1. Go to https://vercel.com
2. Sign up using your GitHub account
3. Authorize Vercel to access your repositories

### 3.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Select your `aom-screening-app` repository
3. Click "Import"

### 3.3 Configure Build Settings

1. **Framework Preset**: Vite
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`

### 3.4 Add Environment Variables

In the "Environment Variables" section, add:

```
VITE_API_BASE_URL=https://aom-screening-backend.onrender.com/api
```

Replace with your actual Render backend URL from Step 2.6.

### 3.5 Deploy

1. Click "Deploy"
2. Wait for deployment (2-5 minutes)
3. **Copy your frontend URL**: `https://aom-screening-app.vercel.app`

## Step 4: Update Backend CORS

Your frontend URL is now known. Update the backend environment variable:

1. Go to Render dashboard → Your web service
2. Environment tab
3. Update `ALLOWED_ORIGINS` to include your Vercel URL:
   ```
   ALLOWED_ORIGINS=https://aom-screening-app.vercel.app,https://*.vercel.app
   ```
4. Save changes (this will trigger a redeploy)

## Step 5: Test Your Deployment

### From Computer:
Visit: `https://aom-screening-app.vercel.app`

### From Phone (Cellular Data):
Visit the same URL: `https://aom-screening-app.vercel.app`

**First load may take 30-60 seconds** if the backend was sleeping.

## Troubleshooting

### Backend Issues

**Problem**: Backend returns 500 error
- Check Render logs: Dashboard → Your service → Logs
- Verify environment variables are set correctly
- Verify DATABASE_URL is correct

**Problem**: CORS errors
- Verify ALLOWED_ORIGINS includes your Vercel URL
- Check that URLs don't have trailing slashes
- Redeploy after changing CORS settings

**Problem**: Slow first load
- This is normal for free tier - backend sleeps after 15 min
- Consider upgrading to paid tier ($7/mo) for always-on

### Frontend Issues

**Problem**: "Failed to fetch" errors
- Verify VITE_API_BASE_URL is set correctly in Vercel
- Check backend is deployed and accessible
- Open browser console to see exact error

**Problem**: Build fails
- Check Vercel build logs
- Verify all dependencies are in package.json
- Test local build: `cd frontend && npm run build`

## Updating Your Deployment

### Push Updates

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push

# Both Render and Vercel will auto-deploy the changes
```

## Free Tier Limitations

### Render Free Tier:
- ✅ Unlimited projects
- ✅ 750 hours/month free
- ⚠️ Sleeps after 15 min inactivity (30-60s cold start)
- ⚠️ PostgreSQL free for 90 days only

### Vercel Free Tier:
- ✅ Unlimited personal projects
- ✅ 100GB bandwidth/month
- ✅ Always-on (no sleep)
- ✅ Automatic HTTPS
- ✅ Global CDN

## Cost to Upgrade (Optional)

If you need:
- **Always-on backend**: Render $7/month
- **PostgreSQL database**: Render $7/month
- **More bandwidth**: Vercel $20/month Pro

## Security Notes

1. **Never commit .env files** - Already in .gitignore
2. **Use strong SECRET_KEY** - Generate random in Render
3. **HTTPS only in production** - Handled automatically by Render/Vercel
4. **Keep dependencies updated** - Run `pip list --outdated` and `npm outdated` regularly

## Support

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Issues**: Create an issue in your GitHub repository

---

**Your app is now accessible from anywhere in the world!** 🎉

Test URL (after deployment):
- Frontend: `https://aom-screening-app.vercel.app`
- Backend: `https://aom-screening-backend.onrender.com`
- API Docs: `https://aom-screening-backend.onrender.com/docs`
