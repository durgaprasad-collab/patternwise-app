from app.core.database import SessionLocal
from app.models.chart_calculation import ChartCalculation


class ChartRepository:

    @staticmethod
    def save_chart(
    profile_id,
    chart_system,
    ayanamsa,
    chart_json,
    profile_json=None
):
        db = SessionLocal()
        try:
            existing_chart = (
            db.query(ChartCalculation)
            .filter(
                ChartCalculation.profile_id == profile_id,
                ChartCalculation.chart_system == chart_system
            )
            .order_by(
                ChartCalculation.id.desc()
                )
            .first()
            )
            if existing_chart:
                print("\nREPOSITORY RECEIVED:")
                print(profile_json)
                existing_chart.chart_json = chart_json
                existing_chart.profile_json = profile_json
                existing_chart.ayanamsa = ayanamsa
                existing_chart.version += 1

            db.commit()
            db.refresh(existing_chart)

            return existing_chart
            
        finally:
            db.close()
   
    @staticmethod
    def get_latest_chart(profile_id):
        db = SessionLocal()
        try:
            return (
            db.query(ChartCalculation)
            .filter(
                ChartCalculation.profile_id == profile_id
            )
            .order_by(
                ChartCalculation.generated_at.desc()
            )
            .first()
        )
        finally:
            db.close()