from datetime import datetime
import uuid

def get_timestamp():
    return datetime.utcnow()

def generate_id():
    return str(uuid.uuid4())
