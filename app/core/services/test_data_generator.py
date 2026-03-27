from datetime import datetime

from faker import Faker

from app.core.constants import PERMISSIONS, ROLES
from app.core.logging.logger import get_logger
from app.core.security import hash_password
from app.modules.roles.adapters.models import PermissionModel, RoleModel
from app.modules.users.adapters.models import UserModel

fake = Faker()

logger = get_logger(__name__)


def generate_users(db, count: int = 10):

    users = []

    for _ in range(count):

        user = UserModel(
            email=fake.unique.email(),
            password=hash_password("Password@123"),
            full_name=fake.name(),
            is_verified=True,
        )
        db.add(user)
        users.append(user)
        logger.info(f"Created: {user.email}")
    db.commit()
    return users


def generate_roles(db):

    roles = []

    for role_name in ROLES:
        existing = db.query(RoleModel).filter_by(name=role_name["name"]).first()
        if existing:
            logger.info(f"{role_name['name']} exists")
            continue
        role = RoleModel(
            name=role_name["name"],
            description=role_name["description"],
        )
        db.add(role)
        roles.append(role)
        logger.info(f"Created: {role.name}")
    db.commit()
    return roles


def generate_permissions(db):

    permissions = []

    for perm_name in PERMISSIONS:

        existing = db.query(PermissionModel).filter_by(name=perm_name).first()

        if existing:
            logger.info(f"{perm_name} exists")
            continue

        permission = PermissionModel(
            name=perm_name,
        )

        db.add(permission)
        permissions.append(permission)

        logger.info(f"Created: {perm_name}")

    db.commit()
    return permissions


def seed_test_data(db):
    existing_users = db.query(UserModel).count()
    existing_roles = db.query(RoleModel).count()
    existing_permissions = db.query(PermissionModel).count()

    if existing_users > 0 or existing_roles > 0 or existing_permissions > 0:
        logger.info("Test data already exists, skipping...")
        return

    logger.info("Seeding test data...")
    generate_users(db, 10)
    generate_roles(db)
    generate_permissions(db)
