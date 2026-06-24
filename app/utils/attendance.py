from app.models import AttendanceSchedule
from app.utils.timezone import nigeria_now


def get_current_checkpoint(unit_id):

    now_time = nigeria_now().time()

    schedule = AttendanceSchedule.query.filter(

        AttendanceSchedule.unit_id == unit_id,

        AttendanceSchedule.is_active == True,

        AttendanceSchedule.open_time <= now_time,

        AttendanceSchedule.close_time >= now_time

    ).first()

    return schedule