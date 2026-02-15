# React UI (Tailwind) for POC MF AI

## Run backend
```bash
cd poc-mf-ai/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Run UI
```bash
cd poc-mf-ai/ui/react-ui
cp .env.example .env
npm install
npm run dev
```

Edit `VITE_API_BASE` in `.env` if needed.
