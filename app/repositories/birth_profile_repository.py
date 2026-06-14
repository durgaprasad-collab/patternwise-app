from sqlalchemy.orm import Session

from app.models.birth_profile import BirthProfile


class BirthProfileRepository:

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int
    ):
        return (
            db.query(BirthProfile)
            .filter(
                BirthProfile.user_id == user_id
            )
            .first()
        )