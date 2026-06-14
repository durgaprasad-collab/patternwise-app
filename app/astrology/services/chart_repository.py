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
            .first()
        )
        if existing_chart:

            existing_chart.chart_json = chart_json
            existing_chart.profile_json = profile_json
            existing_chart.ayanamsa = ayanamsa
            existing_chart.version += 1

            chart_record = existing_chart
        else:
            chart_record = ChartCalculation(
                profile_id=profile_id,
                chart_system=chart_system,
                ayanamsa=ayanamsa,
                chart_json=chart_json,
                profile_json=profile_json,
                version=1
            )

            db.add(chart_record)

        db.commit()
        db.refresh(chart_record)

        return chart_record
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