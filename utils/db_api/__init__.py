from .models import Filter, User, Subscribe, LastJob, Tutorial
from .base import session, metadata

metadata.create_all()
