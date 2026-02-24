from pymongo import MongoClient
import datetime
import random

def seed_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.log_sentinel
    logs_col = db.logs
    
    # Clear existing
    logs_col.delete_many({})
    
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    messages = [
        "User login successful",
        "Failed password attempt",
        "Sensitive file accessed",
        "System reboot initiated",
        "New firewall rule added",
        "Inbound connection from unknown IP",
        "API key rotated",
        "Database backup completed"
    ]
    
    sample_logs = []
    for i in range(50):
        timestamp = (datetime.datetime.now() - datetime.timedelta(hours=random.randint(0, 24))).strftime("%Y-%m-%d %H:%M:%S")
        level = random.choice(levels)
        message = random.choice(messages)
        
        is_suspicious = level in ["ERROR", "CRITICAL"] or "unknown" in message.lower() or "failed" in message.lower()
        
        sample_logs.append({
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "is_suspicious": is_suspicious
        })
    
    logs_col.insert_many(sample_logs)
    print(f"Successfully seeded {len(sample_logs)} logs into MongoDB.")

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"Error seeding data: {e}. Make sure MongoDB is running.")
