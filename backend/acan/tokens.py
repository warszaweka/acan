from django.contrib.auth.tokens import \
    PasswordResetTokenGenerator as TokensPasswordResetTokenGenerator


class EmailVerifyTokenGenerator(TokensPasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) + str(user.is_active))


class PasswordResetTokenGenerator(TokensPasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) + user.password +
                str(user.last_login))


email_verify_token = EmailVerifyTokenGenerator()
password_reset_token = PasswordResetTokenGenerator()
