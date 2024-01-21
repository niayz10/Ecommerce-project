from typing import Protocol, OrderedDict
import logging
from django.forms import ValidationError
from . import repositories, models
from rest_framework_simplejwt import tokens
from django.core.cache import cache
from django.core.mail import send_mail
from templated_email import send_templated_mail
from django.conf import settings
import random
import uuid


logger = logging.getLogger(__name__)

class UserServiceInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict:
        ...

    def verify_user(self, data:OrderedDict) -> models.CustomUser | None:
        ...

    def create_token(self, data: OrderedDict) -> dict:
        ...

    def verify_token(self, data: OrderedDict) -> dict:
        ...

class UserServiceV1:
    repos: repositories.UserRepositoryInterface = repositories.UserReposotoryV1()


    def create_user(self, data:OrderedDict) -> dict:
        session_id = self._verify_phone_number(data=data)

        return {
            'session_id': session_id,
        }

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        user_data = cache.get(data['session_id'])
        if not user_data:
            raise ValidationError

        if data['code'] != user_data['code']:
            raise ValidationError

        user = self.repos.create_user(data={
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
        # self.send_message_to(user=user)


    def create_token(self, data: OrderedDict) -> dict:
        session_id = self._verify_phone_number(data=data)

        return {
            'session_id': session_id
        }

    def verify_token(self, data: OrderedDict) -> dict:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError

        if session['code'] != data['code']:
            raise ValidationError

        user = self.repos.get_user(data={'phone_number': session['phone_number']})
        access_token = tokens.AccessToken.for_user(user=user)
        refresh_token = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }

    def _verify_phone_number(self, data: OrderedDict) -> str:
        code = self._generate_code()
        session_id = self._generate_session_id()
        session = {'code': code, **data}
        cache.set(session_id, session, timeout=300)
        self.send_sms_to_phone_number(phone_number=data['phone_number'], code=code)

        return session_id

    @staticmethod
    def send_message_to(user: models.CustomUser) -> None:
        #  send_mail(
        #      subject='Welcome!!!',
        #      message='Thank you!!!',
        #      from_email=settings.EMAIL_HOST_USER,
        #      recipient_list=[email],
        #      fail_silently=False,
        #  )
        send_templated_mail(
            template_name='welcome',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            context={
                'email': user.email,
                'phone_number': user.phone_number,
            },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
        )

    @staticmethod
    def send_sms_to_phone_number(phone_number: str, code: str) -> None:
        logger.info(f'send sms code = {code} to phone_number = {phone_number}')

    @staticmethod
    def _generate_code(length: int = 4):
        nums = [str(i) for i in range(10)]
        return ''.join(random.choices(nums, k=length))

    @staticmethod
    def _generate_session_id():
        return str(uuid.uuid4())