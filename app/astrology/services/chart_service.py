from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.astrology.profile.ai_profile_generator import AIProfileGenerator
from app.astrology.profile.profile_builder import ProfileBuilder
from app.astrology.profile.profile_serializer import serialize_profile
from app.astrology.services.chart_generator import ChartGenerator
from app.astrology.services.chart_repository import ChartRepository
from app.core.database import SessionLocal
from app.models.birth_profile import BirthProfile


class ChartService:

    @staticmethod
    def generate_and_save_chart(profile_id):
        db = SessionLocal()

        try:
            profile = (
                db.query(BirthProfile)
                .filter(BirthProfile.id == profile_id)
                .first()
            )

            if not profile:
                return None

            local_dt = datetime.combine(
                profile.birth_date,
                profile.birth_time,
            ).replace(tzinfo=ZoneInfo(profile.timezone))
            utc_dt = local_dt.astimezone(timezone.utc)

            hour_decimal = utc_dt.hour + utc_dt.minute / 60

            chart = ChartGenerator.generate_d1(
                utc_dt.year,
                utc_dt.month,
                utc_dt.day,
                hour_decimal,
                profile.latitude,
                profile.longitude,
            )
            cosmic_profile = ProfileBuilder.build(chart)
            structured_profile = serialize_profile(cosmic_profile)
            ai_profile = AIProfileGenerator.generate(
                chart,
                structured_profile,
            )
            ai_profile["natural_potential_index"] = (
                cosmic_profile.alignment_score
            )

            return ChartRepository.save_chart(
                profile_id=profile.id,
                chart_system="vedic",
                ayanamsa="lahiri",
                chart_json=chart,
                profile_json=ai_profile,
            )
        finally:
            db.close()
