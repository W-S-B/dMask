from dMask import db, bcrypt
from dMask.models import User, Status

db.create_all()
user = User(username="admin", password=bcrypt.generate_password_hash("8Okcg7R0Im").decode('utf-8'), secret="")
db.session.add(user)
db.session.commit()

status = Status(masks_count=10, passed_people=11, passed_green=1, passed_yellow=5, passed_red=5)
db.session.add(status)
db.session.commit()