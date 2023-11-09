from db.models import user_model
from db.models import mission_model
from db.models import user_mission_model

alembic_metadata = [
    user_model.Base.metadata,
    mission_model.Base.metadata,
    user_mission_model.Base.metadata
]
