from datetime import time
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SchoolCertificationTokenGeneration(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.school_certificate)


school_certification_token = SchoolCertificationTokenGeneration()
