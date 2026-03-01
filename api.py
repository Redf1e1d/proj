from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import DeveloperSchema, DeveloperResponse, DeveloperUpdate, UserCreate, Token
import models_db
from auth import hash_password, create_access_token, verify_password, get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
from models_db import User                                                    


#Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


developers = []

@app.post("/developers")
def create_developer(dev: DeveloperSchema):
    developers.append(dev)
    return {"status":"created", "developer":dev}  

@app.get("/developers")
def get_developers():
    return developers

@app.post("/developers")
def create_developer(dev: DeveloperSchema, db: Session = Depends(get_db)):
    db_dev = models_db.Developer(**dev.model_dumb())
    db.add(db_dev)
    db.commit()
    db.refresh(db_dev)
    return db_dev
@app.get("/developers/{dev_id}", response_model=DeveloperResponse)
def get_developer(dev_id: int, db: Session = Depends(get_db)):
    db_dev = db.query(models_db.Developer).filter(
        models_db.Developer.id == dev_id
    ).first()

    if not db_dev:
        return {"error": "Developer not found"}

    return db_dev

@app.put("/developers/{dev_id}", response_model = DeveloperResponse)
def update_developer(
    dev_id:int,
    dev_update: DeveloperUpdate,
    db: Session = Depends(get_db)    
):
    db_dev = db.query(models_db.Developer).filter(
        models_db.Developer.id == dev_id
    ).first()

    if not db_dev:
        return {"error": "Developer not found"}
    
    update_data = dev_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_dev, key, value)
    
    db.commit()
    db.refresh(db_dev)

    return db_dev

@app.delete("/developers/{dev_id}")
def delete_developer(dev_id: int, db: Session = Depends(get_db)):
    db_dev = db.query(models_db.Developer).filter(
        models_db.Developer.id == dev_id
    ).first()

    if not db_dev:
        return {"error": "Developer not found"}
    
    db.delete(db_dev)
    db.commit()

    return {"status": "deleted"}

@app.post("/register")
def register(user:UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)

    db_user = models_db.User(
        username=User.username,
        hashed_password=hashed
    )

    db.add(db_user)
    db.commit()

    return {"status": "user created"}

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models_db.User).filter(
        models_db.User.username == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/developers")
def get_developers(
    db:Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(models_db.Developer).all()
