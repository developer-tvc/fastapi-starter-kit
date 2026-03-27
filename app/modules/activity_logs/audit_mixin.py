from datetime import datetime

from sqlalchemy import event
from sqlalchemy.inspection import inspect

from app.modules.activity_logs.adapters.models import ActivityLogModel
from app.modules.activity_logs.constants import LOG_DESCRIPTION, USER_TRACK_FIELD
from app.modules.activity_logs.request_context import current_ip
from app.modules.activity_logs.serializer import serialize_model


class AuditModelMixin:

    @classmethod
    def __declare_last__(cls):

        # CREATE
        @event.listens_for(cls, "after_insert")
        def after_insert(mapper, connection, target):

            model_name = target.__class__.__name__
            label = LOG_DESCRIPTION.get(model_name, model_name.lower())

            session = inspect(target).session
            user = session.info.get("current_user") if session else None

            name = None
            user_id = None

            if user:
                user_id = user.id
                name = user.full_name

            description = None
            if name:
                description = f"{label} created by {name}"

            connection.execute(
                ActivityLogModel.__table__.insert().values(
                    user_id=user_id,
                    action=f"{label} created",
                    object_type=model_name,
                    object_id=target.id,
                    ip_address=current_ip.get(),
                    description=description,
                    new_value=serialize_model(target),
                )
            )

        # UPDATE
        @event.listens_for(cls, "after_update")
        def after_update(mapper, connection, target):

            state = inspect(target)

            old_values = {}
            new_values = {}

            for attr in state.attrs:
                if attr.key not in USER_TRACK_FIELD:
                    continue
                hist = attr.history
                if hist.has_changes():

                    old = hist.deleted[0] if hist.deleted else None
                    new = hist.added[0] if hist.added else getattr(target, attr.key)

                    if old != new:

                        if isinstance(old, datetime):
                            old = old.isoformat()

                        if isinstance(new, datetime):
                            new = new.isoformat()

                        old_values[attr.key] = old
                        new_values[attr.key] = new

            if not new_values:
                return

            model_name = target.__class__.__name__
            label = LOG_DESCRIPTION.get(model_name, model_name.lower())

            session = inspect(target).session
            user = session.info.get("current_user") if session else None

            name = None
            user_id = None

            if user:
                user_id = user.id
                name = user.full_name

            description = None
            if name:
                description = f"{label} updated by {name}"

            connection.execute(
                ActivityLogModel.__table__.insert().values(
                    user_id=user_id,
                    action=f"{label} updated",
                    object_type=model_name,
                    object_id=target.id,
                    ip_address=current_ip.get(),
                    description=description,
                    old_value=old_values,
                    new_value=new_values,
                )
            )

        # DELETE
        @event.listens_for(cls, "after_delete")
        def after_delete(mapper, connection, target):

            model_name = target.__class__.__name__
            label = LOG_DESCRIPTION.get(model_name, model_name.lower())

            session = inspect(target).session
            user = session.info.get("current_user") if session else None

            name = None
            user_id = None

            if user:
                user_id = user.id
                name = user.full_name

            description = None
            if name:
                description = f"{label} deleted by {name}"

            connection.execute(
                ActivityLogModel.__table__.insert().values(
                    user_id=user_id,
                    action=f"{label} deleted",
                    object_type=model_name,
                    object_id=target.id,
                    ip_address=current_ip.get(),
                    description=description,
                )
            )
