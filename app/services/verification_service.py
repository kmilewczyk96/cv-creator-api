import os

import resend

from random import choice
from string import Template, ascii_uppercase, digits

from api.schemas.user import UserCreateResponse


class VerificationService:
    app_name = os.environ.get('APP_NAME')
    domain = os.environ.get('DOMAIN_NAME')
    resend.api_key = os.environ.get('RESEND_API_KEY')

    @staticmethod
    def generate_verification_code(length=6) -> str:
        """Generates and returns a (by default: 6 character) verification code."""
        characters = ascii_uppercase + digits
        return ''.join(choice(characters) for _ in range(length))

    def send_verification_code(self, recipient: UserCreateResponse):
        with open('/app/app/utils/email_templates/email_verification.html', 'r', encoding='utf-8') as template:
            src = Template(template.read())

        html_content = src.substitute(
            app_name=self.app_name,
            full_name=recipient.full_name,
            verification_code=self.generate_verification_code()
        )
        params: resend.Emails.SendParams = {
            'from': f'noreply@{self.domain}',
            'to': recipient.email,
            'subject': f'Welcome to {self.app_name}',
            'html': html_content,

        }
        return resend.Emails.send(params=params)
