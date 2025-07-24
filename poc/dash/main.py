# from fastapi import FastAPI, Depends, Request, HTTPException
# from sqlalchemy.orm import Session
# import requests
# import os
# from db import Base, engine, SessionLocal
# from models import User
# from dotenv import load_dotenv

# load_dotenv()
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def verify_clerk_token(request: Request):
#     token = request.headers.get("Authorization")
#     if not token or not token.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing or invalid token")

#     token_value = token.split(" ")[1]
#     resp = requests.get("https://api.clerk.dev/v1/me", headers={
#         "Authorization": f"Bearer {token_value}",
#         "Content-Type": "application/json",
#         "Clerk-Secret-Key": CLERK_SECRET_KEY
#     })

#     if resp.status_code != 200:
#         raise HTTPException(status_code=401, detail="Unauthorized Clerk token")

#     return resp.json()

# @app.get("/")
# def public_route():
#     return {"message": "Public API working!"}

# @app.get("/profile")
# def protected_route(request: Request, db: Session = Depends(get_db), clerk_user=Depends(verify_clerk_token)):
#     # Store or fetch user from DB
#     user_id = clerk_user["id"]
#     email = clerk_user["email_addresses"][0]["email_address"]

#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         user = User(id=user_id, email=email)
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     return {
#         "id": user.id,
#         "email": user.email,
#         "message": "Authenticated via Clerk + stored in Neon DB"
#     }


from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import requests
import os

from db import SessionLocal, Base, engine
from models import User

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files and frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=".")

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_clerk_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token_value = token.split(" ")[1]
    resp = requests.get("https://api.clerk.dev/v1/me", headers={
        "Authorization": f"Bearer {token_value}",
        "Content-Type": "application/json",
        "Clerk-Secret-Key": CLERK_SECRET_KEY
    })

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized Clerk token")

    return resp.json()

@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile")
def protected_route(request: Request, db: Session = Depends(get_db), clerk_user=Depends(verify_clerk_token)):
    user_id = clerk_user["id"]
    email = clerk_user["email_addresses"][0]["email_address"]

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "message": "Authenticated via Clerk + stored in Supabase DB"
    }
