import datetime
import os
import resend

from random import choice
from string import Template, ascii_uppercase, digits

from fastapi import (
    HTTPException,
    status,
)
from pydantic import EmailStr
from sqlmodel import select

from core.db import SessionDep
from core.models import (
    User,
    VerificationCode,
)


class VerificationService:
    # TODO: move OS variables to settings.
    app_name = os.environ.get('APP_NAME')
    domain = os.environ.get('DOMAIN_NAME')
    resend.api_key = os.environ.get('RESEND_API_KEY')

    def __init__(self, session: SessionDep):
        self.session = session

    def generate_new_verification_code(self, length=6) -> VerificationCode:
        """Generates and returns a (by default: 6 character) verification code."""
        characters = ascii_uppercase + digits
        verification_code = VerificationCode(
            code=''.join(choice(characters) for _ in range(length)),
            created=datetime.datetime.now(),
            expires=datetime.timedelta(minutes=60) + datetime.datetime.now()
        )
        self.session.add(instance=verification_code)
        return verification_code

    def send_verification_code(self, verification_code: VerificationCode):
        with open('/app/app/utils/email_templates/email_verification.html', 'r', encoding='utf-8') as template:
            src = Template(template.read())

        html_content = src.substitute(
            app_name=self.app_name,
            full_name=verification_code.user.full_name,
            verification_code=verification_code.code,
        )
        params: resend.Emails.SendParams = {
            'from': f'noreply@{self.domain}',
            'to': verification_code.user.email,
            'subject': f'Welcome to {self.app_name}',
            'html': html_content,

        }
        return resend.Emails.send(params=params)

    def verify_email(self, email: EmailStr, code: str):
        sql = select(User).where(User.email == email)
        user: User = self.session.exec(statement=sql).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User with this email no longer exists!'
            )

        if (
            not user.verification_code or
            user.verification_code.code != code.upper() or
            user.verification_code.expires <= datetime.datetime.now()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Code has expired or is invalid!',
            )

        self.session.delete(user.verification_code)
        user.is_verified = True
        self.session.commit()
