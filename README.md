# Recon Platform

This project is a minimal prototype of a reconnaissance platform following the ARWAD methodology. It uses FastAPI for the API backend and provides a plugin system for integrating recon tools.

## Project structure

- `api/` – FastAPI application entry point
- `workers/` – worker logic and job queue
- `plugins/` – built-in and external plugins
- `models/` – SQLAlchemy ORM models
- `schemas/` – Pydantic models for API requests/responses
- `utils/` – helper utilities such as plugin loading

## Running

Install requirements and start the API with:

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```
