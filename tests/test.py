from services.database import db

print(db.users.find_one({"api": "01GV2S6CP89DTF548AQWZFYK3P"}, {"username": 1, "_id": 0}))
