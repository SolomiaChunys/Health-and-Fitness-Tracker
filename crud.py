from schemas import DailyActivityCreate, DailyActivityUpdate
from models import DailyActivity, User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date


def create_daily_activity(
        daily_activity: DailyActivityCreate,
        current_user: User,
        db: Session):

    db_check_date = db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id,
        DailyActivity.date == date.today()
    ).first()

    if db_check_date:
        raise HTTPException(status_code=404, detail="Activity for today already created!")

    db_daily_activity = DailyActivity(
        steps_taken=daily_activity.steps_taken,
        calories_burned=daily_activity.calories_burned,
        water_intake=daily_activity.water_intake,
        sleep_hours=daily_activity.sleep_hours,
        user_id=current_user.id,
        date=date.today(),
    )

    db.add(db_daily_activity)
    db.commit()
    db.refresh(db_daily_activity)

    return db_daily_activity


def get_daily_activity_by_date(activity_date: date, current_user: User, db: Session):
    db_daily_activity = db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id,
        DailyActivity.date == activity_date).first()

    if db_daily_activity is None:
        raise HTTPException(status_code=404, detail="No daily activity for this date")
    return db_daily_activity


def get_full_daily_activity(current_user: User, db: Session):
    return db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id
    ).order_by(DailyActivity.id)


def update_daily_activity(
    activity_date: date,
    updated_data: DailyActivityUpdate,
    current_user: User,
    db: Session
):
    db_activity = db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id,
        DailyActivity.date == activity_date
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="No daily activity for this date")

    if updated_data.steps_taken is not None:
        db_activity.steps_taken = updated_data.steps_taken
    if updated_data.calories_burned is not None:
        db_activity.calories_burned = updated_data.calories_burned
    if updated_data.water_intake is not None:
        db_activity.water_intake = updated_data.water_intake
    if updated_data.sleep_hours is not None:
        db_activity.sleep_hours = updated_data.sleep_hours

    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_daily_activity(activity_date: date, current_user: User, db: Session):
    db_activity = db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id,
        DailyActivity.date == activity_date
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="No daily activity for this date")

    db.delete(db_activity)
    db.commit()
    return {"detail": "Activity deleted successfully"}
