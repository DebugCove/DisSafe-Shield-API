import uuid


uuid_generated = uuid.uuid4()
uuid_str = str(uuid_generated)

print(f"Generated UUID: {uuid_str}")
print(f"Number of characters: {len(uuid_str)}")
