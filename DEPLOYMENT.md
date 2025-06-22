# 🚀 Deployment Guide

This guide will help you deploy your Mood-to-Music Recommender to various platforms.

## 📋 Prerequisites

1. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **GitHub Repository**: Your code should be pushed to GitHub (✅ Done!)

## 🎯 Recommended: Render (Free & Easy)

### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account

### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `irfan2809/VibeBeats`
3. Configure the service:
   - **Name**: `vibebeats-mood-music`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### Step 3: Environment Variables
1. Go to "Environment" tab
2. Add environment variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-3 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## 🚂 Alternative: Railway

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project" → "Deploy from GitHub repo"
2. Select your repository
3. Railway will auto-detect it's a Python app

### Step 3: Environment Variables
1. Go to "Variables" tab
2. Add: `OPENAI_API_KEY = your_api_key_here`

### Step 4: Deploy
1. Railway will automatically deploy
2. Get your live URL from the "Deployments" tab

## ⚡ Alternative: Vercel

### Step 1: Sign Up
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Import your GitHub repository
3. Vercel will auto-detect the configuration

### Step 3: Environment Variables
1. Go to "Settings" → "Environment Variables"
2. Add: `OPENAI_API_KEY = your_api_key_here`

### Step 4: Deploy
1. Click "Deploy"
2. Your app will be live in minutes

## 🌐 Alternative: Heroku

### Step 1: Install Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login & Deploy
```bash
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_api_key_here
git push heroku main
```

## 🔧 Local Testing Before Deployment

### Test with Production Settings
```bash
# Set your API key
set OPENAI_API_KEY=your_api_key_here

# Run with production settings
python app.py
```

### Test with Gunicorn
```bash
pip install gunicorn
gunicorn app:app
```

## 📊 Monitoring & Maintenance

### Check Logs
- **Render**: Dashboard → Your Service → Logs
- **Railway**: Project → Deployments → View Logs
- **Vercel**: Dashboard → Your Project → Functions → View Logs

### Environment Variables
Always keep your `OPENAI_API_KEY` secure and never commit it to Git.

### Performance
- Free tiers have limitations
- Consider upgrading for production use
- Monitor API usage to avoid rate limits

## 🆘 Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Check `requirements.txt` includes all dependencies
   - Ensure `gunicorn` is in requirements

2. **"OpenAI API key not found"**
   - Verify environment variable is set correctly
   - Check variable name spelling

3. **"Port already in use"**
   - The app now uses `PORT` environment variable
   - Should work automatically on cloud platforms

4. **"Build failed"**
   - Check build logs for specific errors
   - Ensure Python version compatibility

## 🎉 Success!

Once deployed, your app will be accessible via a public URL. Share it with friends and family to test your Mood-to-Music Recommender!

### Example URLs:
- Render: `https://vibebeats-mood-music.onrender.com`
- Railway: `https://your-app-name.railway.app`
- Vercel: `https://your-app-name.vercel.app`

## 🔄 Updates

To update your deployed app:
1. Make changes to your code
2. Commit and push to GitHub
3. Your cloud platform will automatically redeploy

---

**Need help?** Check the platform-specific documentation or create an issue in your GitHub repository. 