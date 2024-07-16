from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("")
print()
print(hashed_password)
print()