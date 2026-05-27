import random

OTP_STORE = {}

class OTPService:

    @staticmethod
    def generate(
        email: str
    ):

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        OTP_STORE[email] = otp

        return otp

    @staticmethod
    def verify(
        email: str,
        otp: str
    ):

        return (
            OTP_STORE.get(email)
            == otp
        )