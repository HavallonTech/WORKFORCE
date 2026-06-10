from flask_login import current_user
from flask import request

from app import db
from app.models import AuditLog
from datetime import datetime
from zoneinfo import ZoneInfo

def nigeria_now():

    return datetime.now(
        ZoneInfo("Africa/Lagos")
    )


def log_audit(
    module,
    action,
    details=""
):

    try:

        audit = AuditLog(

            user_id=current_user.id
            if current_user.is_authenticated
            else None,

            username=current_user.username
            if current_user.is_authenticated
            else "SYSTEM",

            module=module,

            action=action,

            details=details,

            ip_address=request.headers.get(
                "X-Forwarded-For",
                request.remote_addr
            ),

            browser=request.user_agent.browser,

            device=request.user_agent.platform,

            operating_system=request.user_agent.os
        )

        db.session.add(
            audit
        )

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            f"Audit Log Error: {e}"
        )