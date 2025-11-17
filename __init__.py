# imageAttendance/__init__.py

from .main import run_app
from .db import init_db, insert_attendance, fetch_attendance
from .recognition import recognize_face
from .attendance import mark_attendance
