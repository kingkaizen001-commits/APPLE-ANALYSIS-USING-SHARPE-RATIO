# Bridgaton AI — Get This Project into VS Code (Beginner-Friendly)

If you feel stuck, you're not dumb — setup can be confusing the first time.

## Option A (Recommended): Git clone into VS Code

### 1) Put this repo on GitHub
If your project is not on GitHub yet:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### 2) Clone in VS Code
1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Search **Git: Clone**
4. Paste your repo URL
5. Choose a folder on your PC
6. Click **Open**

## Option B (No Git): Copy folder manually

### Windows
1. Zip this project folder
2. Move zip to your PC
3. Extract it
4. In VS Code: **File → Open Folder** and choose extracted folder

### macOS/Linux
1. Copy the project folder (USB/cloud/shared disk)
2. In VS Code: **File → Open Folder**

## Option C (Use terminal on your PC)

### Windows (PowerShell)
```powershell
cd C:\Users\<you>\Documents
git clone <YOUR_GITHUB_REPO_URL>
cd APPLE-ANALYSIS-USING-SHARPE-RATIO
code .
```

### macOS/Linux
```bash
cd ~/projects
git clone <YOUR_GITHUB_REPO_URL>
cd APPLE-ANALYSIS-USING-SHARPE-RATIO
code .
```

## After it opens in VS Code (run steps)

```bash
python -m venv .venv
```

### Activate venv
- Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

### Install and run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open: `http://localhost:8000/docs`

## If `code .` does not work
In VS Code:
1. `Ctrl+Shift+P`
2. Run: **Shell Command: Install 'code' command in PATH**
3. Restart terminal

## Quick troubleshooting
- "Git not found" → install Git first
- "Permission denied" on activate script (Windows) → run PowerShell as Admin once and run:
  ```powershell
  Set-ExecutionPolicy RemoteSigned
  ```
- "Address already in use" on port 8000 → run:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```
