from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine
from datetime import date
import data_analysis
import database
import schemas
import models
import auth
import crud


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    auth.register_user(user, db)
    return {"message": "You are successfully registered!"}


@app.post("/login", response_model=schemas.Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/main")
async def protected_route(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


# Create Daily Activity
@app.post('/create/activity', response_model=schemas.DailyActivity)
async def post_daily_activity(
    daily_activity: schemas.DailyActivityCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.create_daily_activity(daily_activity, current_user, db)


# Get All Daily Activities
@app.get('/get/activity', response_model=schemas.DailyActivityList)
async def get_all_daily_activity(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    activities = crud.get_full_daily_activity(current_user, db).all()
    return {"activities": [schemas.DailyActivity.from_orm(activity) for activity in activities]}


# Get Daily Activity By Date
@app.get('/get/activity/detail/{activity_date}', response_model=schemas.DailyActivity)
async def get_daily_activity_by_date(
    activity_date: date,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.get_daily_activity_by_date(activity_date, current_user, db)


# Update Daily Activity
@app.patch('/update/activity/{activity_date}', response_model=schemas.DailyActivity)
async def update_daily_activity(
    activity_date: date,
    updated_data: schemas.DailyActivityUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.update_daily_activity(activity_date, updated_data, current_user, db)


# Delete Daily Activity
@app.delete('/delete/activity/{activity_date}')
async def delete_daily_activity(
    activity_date: date,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.delete_daily_activity(activity_date, current_user, db)


# Get Weekly Analysis
@app.get('/get/analysis/weekly')
async def get_weekly_analysis(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    activities = crud.get_full_daily_activity(current_user, db)
    data = data_analysis.convert_data(activities)
    weekly_averages = data_analysis.get_averages(data, 'W')
    formatted_data = data_analysis.formate_data(weekly_averages)

    return formatted_data


# Get Monthly Analysis
@app.get('/get/analysis/monthly')
async def get_monthly_analysis(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    activities = crud.get_full_daily_activity(current_user, db)
    data = data_analysis.convert_data(activities)
    monthly_averages = data_analysis.get_averages(data, 'ME')
    formatted_data = data_analysis.formate_data(monthly_averages)

    return formatted_data


# Visualize Weekly Analysis
@app.get('/get/analysis/weekly/plot')
async def get_weekly_analysis_plot(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    activities = crud.get_full_daily_activity(current_user, db)
    data = data_analysis.convert_data(activities)
    data_analysis.visualize_activity(data, period="weekly")
    return {"detail": "Weekly plots displayed successfully"}


# Visualize Monthly Analysis
@app.get('/get/analysis/monthly/plot')
async def get_monthly_analysis_plot(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    activities = crud.get_full_daily_activity(current_user, db)
    data = data_analysis.convert_data(activities)
    data_analysis.visualize_activity(data, period="monthly")
    return {"detail": "Monthly plots displayed successfully"}
