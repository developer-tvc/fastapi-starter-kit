from app.modules.auth.adapters.models import BlacklistedToken


class BlacklistRepository:

    def __init__(self, db):
        self.db = db

    def add(self, jti: str):
        token = BlacklistedToken(jti=jti)
        self.db.add(token)
        self.db.commit()

    def exists(self, jti: str):

        return (
            self.db.query(BlacklistedToken).filter(BlacklistedToken.jti == jti).first()
            is not None
        )
