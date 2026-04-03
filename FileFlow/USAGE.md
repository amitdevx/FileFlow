# IMPORTANT: How to Use FileFlow

## The Right Way to Access the App

FileFlow has TWO interfaces:

### ❌ WRONG: React App on Port 3000
Don't use `http://localhost:3000` directly - it won't work properly because:
- React needs Flask session cookies
- Login/signup must happen on Flask first
- The React app is meant to be used AFTER logging in

### ✅ CORRECT: Flask App on Port 5000

**Use `http://localhost:5000` - this is the main entry point!**

## Step-by-Step Usage:

1. **Start the servers:**
   ```bash
   cd FileFlow
   ./start.sh
   ```

2. **Open Flask (Port 5000):**
   ```
   http://localhost:5000
   ```

3. **Sign up or login:**
   - Click "Sign Up" to create an account
   - Or "Login" if you have an account
   - Flask handles all authentication

4. **Access the dashboard:**
   - After logging in, go to `http://localhost:5000/dashboard`
   - Or Flask will redirect you automatically

5. **Use the file manager:**
   - All buttons work (Upload, New Folder, Rename, Delete, Download)
   - Double-click folders to navigate
   - Right-click for context menu
   - Keyboard shortcuts work

## Why Two Ports?

- **Port 5000 (Flask)** - Backend API + Authentication + HTML templates
- **Port 3000 (React)** - Development server (proxies to Flask)

The React app on port 3000 is for development only. In production, Flask would serve the built React app.

## If You See Login Prompt on React:

If you accidentally opened `http://localhost:3000`:
1. Close that tab
2. Go to `http://localhost:5000`
3. Login there
4. Access dashboard at `http://localhost:5000/dashboard`

## Alternative: Use React SPA (Advanced)

If you want to use React as a true SPA on port 3000:

1. First, login via Flask at `http://localhost:5000`
2. Then open `http://localhost:3000`
3. The cookies should work across localhost ports
4. Click the Login/Signup buttons in the React app

But this is NOT the recommended workflow!

## Quick Reference

| What | URL | Purpose |
|------|-----|---------|
| **Main App** | http://localhost:5000 | ← USE THIS |
| Login/Signup | http://localhost:5000/login | Authentication |
| Dashboard | http://localhost:5000/dashboard | File Manager |
| React Dev | http://localhost:3000 | Development only |

## Need Help?

The app is designed to work with Flask's traditional session-based authentication.
Always start at `http://localhost:5000`!
