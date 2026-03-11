def password_reset_email(reset_link: str) -> str:
    return f"""
        Hello,

        You requested a password reset.

        Click the link below to reset your password:

        {reset_link}

        This link will expire in 30 minutes.

        If you did not request this, please ignore this email.

        Thanks,
        Support Team
        """

def email_verification_template(verify_link: str):

    return f"""
        Hello,

        Please verify your email by clicking the link below:

        {verify_link}

        This link will expire in 24 hours.

        If you did not create this account, please ignore this email.

        Thanks,
        Support Team
        """