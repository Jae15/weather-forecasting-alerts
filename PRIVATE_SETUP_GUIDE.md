# Private Setup & GitHub Guide
## Step-by-Step Instructions for Jae Mwangi

**PRIVATE DOCUMENT - FOR JAE MWANGI ONLY**

---

## Table of Contents

1. [Running the Project Locally](#running-the-project-locally)
2. [Pushing to GitHub](#pushing-to-github)
3. [Deploying to Streamlit Cloud](#deploying-to-streamlit-cloud)
4. [Maintaining the Project](#maintaining-the-project)
5. [Troubleshooting](#troubleshooting)

---

## Running the Project Locally

### Step 1: Extract the Project

```bash
# Navigate to where you downloaded the zip file
cd ~/Downloads  # or wherever you saved it

# Extract the zip file
unzip weather_forecasting_project.zip

# Navigate into the project folder
cd enviroweather_projects
```

### Step 2: Set Up Python Environment

```bash
# Check your Python version (need 3.11+)
python3 --version

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt now
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# This will take 5-10 minutes, especially Prophet which compiles C++ code
# You'll see a lot of output - that's normal

# Verify installation
python -c "import pandas, prophet, streamlit; print('✅ All packages installed!')"
```

### Step 4: Run the Analysis Scripts (Optional)

If you want to regenerate all the data and figures from scratch:

```bash
# Step 1: Data preparation & EDA (~2-3 minutes)
python 01_timeseries_forecasting.py

# Step 2: Model training (~5-10 minutes)
python 02_model_building.py

# Step 3: Alert system (~3-5 minutes)
python 03_alert_system.py

# All done! You should see new CSV files and figures generated
```

**Note:** The zip file already includes all generated data and figures, so you can skip this step if you just want to run the dashboard.

### Step 5: Launch the Dashboard

```bash
# Make sure you're in the enviroweather_projects folder
# and your virtual environment is activated (you see (venv) in prompt)

streamlit run app.py

# You should see output like:
#   You can now view your Streamlit app in your browser.
#   Local URL: http://localhost:8501
#   Network URL: http://192.168.x.x:8501

# Your browser should open automatically
# If not, manually go to http://localhost:8501
```

### Step 6: Explore the Dashboard

The dashboard has 4 pages:
1. **📊 Overview** - Project summary and key metrics
2. **📈 Model Performance** - Model comparison and methodology
3. **🔔 Alert System** - Alert timeline and configuration
4. **🔍 Data Explorer** - Interactive data visualization

Click through each page to see your work!

### Step 7: Stop the Dashboard

When you're done:
- Press `Ctrl+C` in the terminal to stop the Streamlit server
- Type `deactivate` to exit the virtual environment

---

## Pushing to GitHub

### Step 1: Create a GitHub Repository

1. Go to https://github.com
2. Log in to your account
3. Click the `+` icon in the top right → "New repository"
4. Fill in:
   - **Repository name**: `weather-forecasting-alerts` (or your preferred name)
   - **Description**: "Time-series forecasting system for agricultural decision support using ARIMA and Prophet models"
   - **Public** (so recruiters can see it)
   - **DO NOT** check "Initialize with README" (we already have one)
5. Click "Create repository"

### Step 2: Initialize Git in Your Project

```bash
# Make sure you're in the enviroweather_projects folder
cd ~/path/to/enviroweather_projects

# Initialize git repository
git init

# Add all files to staging
git add .

# Check what will be committed
git status

# You should see all your files listed in green
```

### Step 3: Make Your First Commit

```bash
# Commit all files
git commit -m "Initial commit: Weather forecasting and alert system project"

# This creates a snapshot of your project
```

### Step 4: Connect to GitHub

```bash
# Replace Jae15 with your actual GitHub username
git remote add origin https://github.com/Jae15/weather-forecasting-alerts.git

# Verify the remote was added
git remote -v

# You should see:
#   origin  https://github.com/Jae15/weather-forecasting-alerts.git (fetch)
#   origin  https://github.com/Jae15/weather-forecasting-alerts.git (push)
```

### Step 5: Push to GitHub

```bash
# Push your code to GitHub
git push -u origin main

# If you get an error about 'main' vs 'master', try:
git branch -M main
git push -u origin main

# You'll be prompted for your GitHub username and password
# For password, use a Personal Access Token (not your actual password)
```

**Creating a Personal Access Token (if needed):**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "Weather Forecasting Project"
4. Check "repo" scope
5. Click "Generate token"
6. **COPY THE TOKEN** - you won't see it again!
7. Use this token as your password when pushing

### Step 6: Verify on GitHub

1. Go to https://github.com/Jae15/weather-forecasting-alerts
2. You should see all your files!
3. The README.md will be displayed automatically
4. Check that the figures folder has all 9 images

### Step 7: Update Your LinkedIn

Now that it's on GitHub, update your LinkedIn profile:

1. Go to your profile → Projects section
2. Add project:
   - **Name**: Weather Forecasting & Agricultural Alert System
   - **URL**: https://github.com/Jae15/weather-forecasting-alerts
   - **Description**: "Built time-series forecasting models (ARIMA, Prophet) achieving 70% better accuracy than baseline methods. Automated alert system generates warnings 27 days in advance for frost, heat, and disease risk, potentially saving $500K annually for 100 farms."

---

## Deploying to Streamlit Cloud

### Step 1: Prepare for Deployment

Make sure these files are in your GitHub repo:
- ✅ `app.py` (the Streamlit app)
- ✅ `requirements.txt` (dependencies)
- ✅ All CSV data files (daily_weather_aetna.csv, etc.)
- ✅ All figures in the figures/ folder

### Step 2: Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign up" or "Sign in"
3. Choose "Continue with GitHub"
4. Authorize Streamlit to access your GitHub repos

### Step 3: Deploy Your App

1. Click "New app" button
2. Select:
   - **Repository**: Jae15/weather-forecasting-alerts
   - **Branch**: main
   - **Main file path**: app.py
3. Click "Deploy!"

### Step 4: Wait for Deployment

- Initial deployment takes 5-10 minutes
- Streamlit will install all dependencies from requirements.txt
- You'll see a log of the installation process
- When done, you'll get a URL like: `https://Jae15-weather-forecasting-alerts.streamlit.app`

### Step 5: Test Your Deployed App

1. Click the URL to open your app
2. Test all 4 pages
3. Make sure visualizations load correctly
4. Try the interactive features

### Step 6: Update Your README

Add the live URL to your README.md:

```bash
# Edit README.md and find this line:
**[🌐 View Interactive Dashboard](https://your-app.streamlit.app)**

# Replace with your actual URL:
**[🌐 View Interactive Dashboard](https://Jae15-weather-forecasting-alerts.streamlit.app)**

# Save, commit, and push:
git add README.md
git commit -m "Add live dashboard URL"
git push
```

### Step 7: Share Your Project

Now you can share:
- **GitHub repo**: https://github.com/Jae15/weather-forecasting-alerts
- **Live dashboard**: https://Jae15-weather-forecasting-alerts.streamlit.app
- Add both to your resume, LinkedIn, and portfolio website

---

## Maintaining the Project

### Making Updates

```bash
# Make changes to your files (e.g., fix a typo in README)

# Check what changed
git status

# Add the changed files
git add README.md  # or git add . for all changes

# Commit with a descriptive message
git commit -m "Fix typo in README"

# Push to GitHub
git push

# If your app is deployed on Streamlit Cloud, it will auto-update!
```

### Common Updates You Might Make

**Update your email/links:**
```bash
# Find and replace in all files
grep -r "your.email@example.com" .
# Then manually update each file
```

**Add new visualizations:**
```bash
# Add new figure to figures/ folder
# Update app.py to display it
git add figures/new_figure.png app.py
git commit -m "Add new visualization"
git push
```

**Update model results:**
```bash
# Re-run analysis scripts
python 01_timeseries_forecasting.py
python 02_model_building.py
python 03_alert_system.py

# Commit new results
git add *.csv figures/
git commit -m "Update model results with latest data"
git push
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'prophet'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall prophet
pip install pystan==2.19.1.1
pip install prophet
```

### Problem: "FileNotFoundError: daily_weather_aetna.csv"

**Solution:**
```bash
# Make sure you're in the right directory
pwd  # Should show .../enviroweather_projects

# If CSV files are missing, regenerate them
python 01_timeseries_forecasting.py
```

### Problem: Streamlit app shows blank page

**Solution:**
```bash
# Check for errors in terminal
# Usually it's a missing file or import error

# Try running Python directly to see the error
python -c "import app"

# Fix the error, then restart
streamlit run app.py
```

### Problem: Git push asks for password but rejects it

**Solution:**
- GitHub no longer accepts passwords for git operations
- You need a Personal Access Token (see Step 5 in "Pushing to GitHub")
- Or set up SSH keys (more advanced)

### Problem: Streamlit Cloud deployment fails

**Solution:**
1. Check the deployment logs for error messages
2. Common issues:
   - Missing files in GitHub repo
   - Wrong file path in deployment settings
   - requirements.txt has wrong package versions
3. Fix the issue, commit, push, and Streamlit will auto-redeploy

### Problem: Dashboard is slow

**Solution:**
```python
# Add caching to app.py for data loading
@st.cache_data
def load_data():
    return pd.read_csv('daily_weather_aetna.csv')
```

---

## Quick Reference Commands

### Virtual Environment
```bash
# Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Running the Project
```bash
# Run analysis (optional)
python 01_timeseries_forecasting.py
python 02_model_building.py
python 03_alert_system.py

# Launch dashboard
streamlit run app.py
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .                    # Add all
git add filename.py          # Add specific file

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline
```

---

## Next Steps

After you have the project running and on GitHub:

1. ✅ **Test everything locally** - make sure dashboard works
2. ✅ **Push to GitHub** - follow steps above
3. ✅ **Deploy to Streamlit Cloud** - get live URL
4. ✅ **Update README** with live URL
5. ✅ **Add to LinkedIn** - Projects section
6. ✅ **Update resume** - include GitHub link
7. ✅ **Practice demo** - be ready to show it in interviews
8. ✅ **Read PRIVATE_INTERVIEW_PREP.md** - prepare talking points

---

## Contact for Help

If you run into issues:

**Jae Mwangi**  
Email: janomwangi@gmail.com  
LinkedIn: https://www.linkedin.com/in/jae-m-9a492636/

**Useful Resources:**
- Git tutorial: https://www.atlassian.com/git/tutorials
- Streamlit docs: https://docs.streamlit.io/
- GitHub docs: https://docs.github.com/

---

**You've got this, Jae! This project is impressive and you should be proud. Follow these steps carefully and you'll have it live on GitHub and deployed in no time.**

