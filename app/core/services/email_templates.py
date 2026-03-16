def password_reset_email(reset_link: str, full_name: str, expire_time: int) -> str:
    return f"""
        Hello {full_name},

        You requested a password reset.

        Click the link below to reset your password:

        {reset_link}

        This link will expire in {expire_time} minutes.

        If you did not request this, please ignore this email.

        Thanks,
        Support Team
        """


def email_verification_template(
    verify_link: str, full_name: str, expire_time: int
) -> str:

    return f"""
        Hello {full_name},

        Please verify your email by clicking the link below:

        {verify_link}

        This link will expire in {expire_time} hours.

        If you did not create this account, please ignore this email.

        Thanks,
        Support Team
        """
