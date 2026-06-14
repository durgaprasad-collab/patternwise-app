from app.core.database import SessionLocal
from app.models.birth_profile import BirthProfile

from app.astrology.services.chart_generator import ChartGenerator
from app.astrology.services.chart_repository import ChartRepository
from app.astrology.profile.ai_profile_generator import AIProfileGenerator
from app.astrology.profile.profile_builder import ProfileBuilder
from app.astrology.profile.profile_serializer import serialize_profile
from app.routes import profile

from zoneinfo import ZoneInfo
from datetime import datetime, timezone 

class ChartService:

    @staticmethod
    def generate_and_save_chart(profile_id):

        db = SessionLocal()
        
        try:

            profile = (
                db.query(BirthProfile)
                .filter(
                    BirthProfile.id == profile_id
                )
                .first()
            )
            print("\n===== PROFILE USED FOR CHART =====")
            print("DATE:", profile.birth_date)
            print("TIME:", profile.birth_time)
            print("LAT:", profile.latitude)
            print("LON:", profile.longitude)
            print("TZ:", profile.timezone)
            print("==================================")
            if not profile:
                return None
            
            local_dt = datetime.combine(
            profile.birth_date,
            profile.birth_time
            ).replace(
            tzinfo=ZoneInfo(profile.timezone)
            )
            print("PROFILE DATE:", profile.birth_date)
            print("PROFILE TIME:", profile.birth_time)
            print("PROFILE TZ:", profile.timezone)
            utc_dt = local_dt.astimezone(
            timezone.utc
            )

           

            year = utc_dt.year
            month = utc_dt.month
            day = utc_dt.day

            hour_decimal = (
                utc_dt.hour +
                utc_dt.minute / 60
            )

            chart = ChartGenerator.generate_d1(
                year,
                month,
                day,
                hour_decimal,
                profile.latitude,
                profile.longitude
            )
            cosmic_profile = ProfileBuilder.build(
                chart
                )
            structured_profile = serialize_profile(
            cosmic_profile
            )   
            structured_profile = serialize_profile(
                cosmic_profile
            )
            print("\nBEFORE AI:=====================================")
            print(cosmic_profile)
            print("=============================================\n" )

            ai_profile = AIProfileGenerator.generate(
            chart,
            structured_profile
            )

            ai_profile["natural_potential_index"] = (
                    cosmic_profile.alignment_score
                )

            print("\nAI PROFILE:===============================")
            print(ai_profile)
            print("==========================================\n")

            print("\nSAVING THIS PROFILE:")
            print(ai_profile)
            print("====================")
            saved_chart = ChartRepository.save_chart(
                profile_id=profile.id,
                chart_system="vedic",
                ayanamsa="lahiri",
                chart_json=chart,
                profile_json=ai_profile
            )
            print("\nSAVING PROFILE:")
            print(ai_profile)
        
            return saved_chart
        finally:
         db.close()