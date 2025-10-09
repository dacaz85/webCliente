# app/routers/companies.py
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.config import STORAGE_PATH
from app.models import Company, Subfolder
from app.schemas.company import CompanyResponse
from app.schemas.subfolder import SubfolderResponse

router = APIRouter(prefix="/companies", tags=["companies"])

# -------------------------
# GET ALL COMPANIES
# -------------------------
@router.get("/", response_model=list[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

# -------------------------
# GET COMPANY BY ID
# -------------------------
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# -------------------------
# GET ALL SUBFOLDERS
# -------------------------
@router.get("/subfolders", response_model=list[SubfolderResponse])
def list_subfolders(db: Session = Depends(get_db)):
    return db.query(Subfolder).all()

# -------------------------
# GET SUBFOLDER BY ID
# -------------------------
@router.get("/subfolders/{subfolder_id}", response_model=SubfolderResponse)
def get_subfolder(subfolder_id: int, db: Session = Depends(get_db)):
    subfolder = db.query(Subfolder).filter(Subfolder.id == subfolder_id).first()
    if not subfolder:
        raise HTTPException(status_code=404, detail="Subfolder not found")
    return subfolder

# -------------------------
# UPDATE ALL COMPANIES & SUBFOLDERS
# -------------------------
@router.post("/update-all", response_model=dict)
def update_all_companies(db: Session = Depends(get_db)):
    if not os.path.exists(STORAGE_PATH):
        raise HTTPException(status_code=400, detail="Storage path not found")

    for folder_name in os.listdir(STORAGE_PATH):
        folder_path = os.path.join(STORAGE_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Separar número y nombre
        if " " in folder_name:
            number, name = folder_name.split(" ", 1)
        else:
            number, name = folder_name[:4], folder_name[4:]

        relative_company_path = f"{number} {name}"

        # Buscar o crear empresa
        company = db.query(Company).filter(Company.number == number).first()
        if company:
            updated = False
            if company.name != name:
                company.name = name
                updated = True
            if company.path != relative_company_path:
                company.path = relative_company_path
                updated = True
            if updated:
                db.add(company)
        else:
            company = Company(number=number, name=name, path=relative_company_path)
            db.add(company)
            db.flush()  # obtener id para subfolders

        # Gestionar subcarpetas
        for sub_name in os.listdir(folder_path):
            sub_path = os.path.join(folder_path, sub_name)
            if not os.path.isdir(sub_path):
                continue

            relative_sub_path = os.path.join(relative_company_path, sub_name)

            subfolder = db.query(Subfolder).filter(
                and_(Subfolder.company_id == company.id, Subfolder.name == sub_name)
            ).first()

            if subfolder:
                if subfolder.path != relative_sub_path:
                    subfolder.path = relative_sub_path
                    db.add(subfolder)
            else:
                subfolder = Subfolder(company_id=company.id, name=sub_name, path=relative_sub_path)
                db.add(subfolder)

    db.commit()
    return {"msg": "Companies and subfolders updated successfully"}
