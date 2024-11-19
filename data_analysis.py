from fastapi import HTTPException
import matplotlib.pyplot as plt
import pandas as pd


def convert_data(activities):
    if not activities:
        raise HTTPException(status_code=404, detail="No activities data provided.")

    data = pd.DataFrame([{
        "date": activity.date,
        "steps_taken": activity.steps_taken,
        "calories_burned": activity.calories_burned,
        "water_intake": activity.water_intake,
        "sleep_hours": activity.sleep_hours
    } for activity in activities])

    if 'date' not in data.columns:
        raise HTTPException(status_code=404, detail="You have not created any activities yet")

    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data


def get_averages(data, period):
    return data.resample(period).mean().tail(2)


def formate_data(data):
    formatted_data = {
        metric: {date.strftime('%Y-%m-%d'): round(value, 2) for date, value in values.items()}
        for metric, values in data.to_dict().items()
    }
    return formatted_data


def visualize_activity(data, period="weekly"):
    metrics = {
        "steps_taken": "Steps Taken",
        "calories_burned": "Calories Burned",
        "water_intake": "Water Intake",
        "sleep_hours": "Sleep Hours",
    }

    plt.figure(figsize=(10, 13))
    num_metrics = len(metrics)

    for i, (key, label) in enumerate(metrics.items(), 1):
        plt.subplot(num_metrics, 1, i)
        if period == "weekly":
            weekly_data = data.tail(7)
            plt.plot(
                weekly_data.index, weekly_data[key],
                marker='d', label=label, color='#23395d', mfc='#23395d',
            )
        elif period == "monthly":
            monthly_data = data.tail(30)
            plt.plot(
                monthly_data.index, monthly_data[key],
                marker='*', label=label, color='#51a687', mfc='#51a687',
            )
        plt.ylabel(label, fontsize=12)
        plt.grid(True)
        plt.legend()

    plt.tight_layout()
    plt.show()
