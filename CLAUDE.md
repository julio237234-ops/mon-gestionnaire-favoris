# Bookmark Manager Extension - Project Overview

An AI-powered bookmark manager browser extension with a FastAPI/GraphQL backend and a modern "Soft UI" frontend.

## 🚀 Quick Start
1. **Backend**:
   - Install dependencies: `pip install -r requirements.txt`
   - Run server: `python main.py`
   - API endpoint: `http://localhost:8000/graphql`
   - **Security**: Requires `X-API-KEY` header (default: `votre_cle_api_secrete`).
2. **Extension**:
   - Load `extension/` folder in Chrome (`chrome://extensions`) or Firefox (`about:debugging`).
   - Configure `API_KEY` in `extension/popup.js`.

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, Strawberry (GraphQL), SQLAlchemy (SQLite).
- **Frontend**: HTML5, CSS3 (TailwindCSS), JavaScript (ES6), Lucide/FontAwesome.
- **Testing**: Pytest for backend validation.

## 📂 Project Structure
- `main.py`: FastAPI server with API Key security.
- `models.py`: SQLAlchemy database models.
- `schema.py`: GraphQL schema (Search, Pagination, Validation).
- `test_main.py`: Unit tests for GraphQL endpoints.
- `extension/`:
  - `manifest.json`: Manifest V3 (Chrome/Firefox compatible).
  - `style.css`: Refactored styles.
  - `popup.html`: Modern UI with Search bar & Spinner.
  - `popup.js`: Logic with Debouncing, Favicons & URL validation.

## 🔧 Features
- **Security**: API Key protection on all GraphQL mutations/queries.
- **Search**: Real-time full-text search on names and URLs.
- **UI/UX**: 
  - Favicons displayed for each bookmark.
  - Loading spinner for server synchronization.
  - Custom deletion confirmation modal.
  - Aggressive focus outline removal for "Soft UI" look.
- **Reliability**: Dual-layer URL validation (Frontend Regex + Backend Re).

## 📝 Usage Rules (for AI Agents)
- Always include `X-API-KEY` header in requests.
- Maintain CSS variables in `style.css` for aesthetic consistency.
- Database changes must be reflected in `models.py`, `schema.py`, and `test_main.py`.
- Run `pytest test_main.py` before committing backend changes.
