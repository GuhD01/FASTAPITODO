from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Optional

app = FastAPI()

class Activity(BaseModel):
    id: UUID
    name: str
    status: str

class UpdateActivity(BaseModel):
    name: Optional[str]
    status: Optional[str]

# Dummy data for demonstration
activities = {
    UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"): Activity(id=UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"), name="Go jogging", status="pending"),
    UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"): Activity(id=UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"), name="Do homework", status="completed")
}

@app.get("/todo/get")
def get_activities():
    return {"Activities": list(activities.values())}

@app.get("/todo/get/user")
def get_activities_by_user(user_id: UUID):  
    filtered_activities = [activity for activity in activities.values() if activity.id == user_id]
    return {"Activities": filtered_activities}

@app.get("/todo/get/{activity_id}")
def get_activity(activity_id: UUID):
    activity = activities.get(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"Activities": activity}

@app.post("/todo/post")
def add_activity(activity: Activity):
    activities[activity.id] = activity
    return {"Activities": activity}

@app.delete("/todo/delete/{activity_id}")
def delete_activity(activity_id: UUID):
    if activity_id in activities:
        del activities[activity_id]
        return {"Success": True, "Message": "Activity deleted successfully"}
    else:
        return {"Success": False, "Message": "Activity not found"}

@app.put("/todo/put/{activity_id}")
def update_activity(activity_id: UUID, activity_data: UpdateActivity):
    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity_data.name:
        activities[activity_id].name = activity_data.name
    if activity_data.status:
        activities[activity_id].status = activity_data.status
    return {"Success": True, "Message": "Activity updated successfusxlly", "Activities": activities[activity_id]}

