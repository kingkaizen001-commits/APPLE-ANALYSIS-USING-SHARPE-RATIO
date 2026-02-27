# Bridgaton AI — Testing Phase Playbook

## 0) Goal
Prove that the backend works end-to-end before deeper model quality work.

## 1) Phase A: Offline checks (fast)
Run:

```bash
make check
```

Expected:
- App compiles
- Structural smoke checks pass

## 2) Phase B: Start runtime stack

### Option 1 (local Python API)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Option 2 (full stack with worker + redis + postgres)
```bash
docker compose up --build
```

## 3) Phase C: Runtime API sanity checks
In a second terminal:

```bash
python scripts/api_sanity_check.py --base-url http://localhost:8000/api/v1 --api-key change-me
```

Expected:
- Public endpoints return 200
- Protected endpoint without key returns 401
- Protected endpoints with key return 200
- Script prints: `PASS: api sanity checks complete`

## 4) Phase D: Manual spot checks
- Open API docs: `http://localhost:8000/docs`
- Verify response headers include `x-request-id`
- Validate Celery worker logs task submissions from:
  - `POST /forecast/async`
  - `POST /ml/train`

## 5) Exit Criteria
- `make check` passes
- `api_sanity_check.py` passes
- No 5xx errors during endpoint walkthrough
- Async task submissions accepted and visible in worker logs
