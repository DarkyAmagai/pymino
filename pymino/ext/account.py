import time

from pymino.ext import entities, utilities

__all__ = ("Account",)


class Account:
    """
    Account class for handling account related requests.
    """

    def __init__(self, session: utilities.RequestHandler) -> None:
        self.session = session

    def register(
        self,
        email: str,
        password: str,
        username: str,
        verificationCode: str,
    ) -> entities.Authenticate:
        """
        Registers a new account.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.

        - `username` - The username of the account.

        - `verificationCode` - The verification code sent to the email.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.request_security_validation(email=email)
        code = input("Enter the code you received: ")
        response = bot.register(email=email, password=password, username=username, verificationCode=code)
        print(response.json())
        ```
        """
        return entities.Authenticate(
            self.session.handler(
                "POST",
                "/g/s/auth/register",
                data={
                    "secret": f"0 {password}",
                    "deviceID": self.session.generate.device_id(),
                    "email": email,
                    "clientType": 100,
                    "nickname": username,
                    "validationContext": {
                        "data": {"code": verificationCode},
                        "type": 1,
                        "identity": email,
                    },
                    "type": 1,
                    "identity": email,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def delete_request(self, email: str, password: str) -> entities.ApiResponse:
        """
        Sends a delete request to the account.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.delete_request(email=email, password=password)
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/account/delete-request",
                data={
                    "secret": f"0 {password}",
                    "deviceID": self.session.generate.device_id(),
                    "email": email,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def delete_request_cancel(self, email: str, password: str) -> entities.ApiResponse:
        """
        Cancels the delete request.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.delete_request_cancel(email=email, password=password)
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/account/delete-request/cancel",
                data={
                    "secret": f"0 {password}",
                    "deviceID": self.session.generate.device_id(),
                    "email": email,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def check_device(self, deviceId: str) -> entities.ApiResponse:
        """
        Checks if the device is valid.

        `**Parameters**`

        - `deviceId` - The device id of the account.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        response = bot.check_device(deviceId=device_id())
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/device",
                data={
                    "deviceID": deviceId,
                    "clientType": 100,
                    "timezone": -310,
                    "systemPushEnabled": True,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def fetch_account(self) -> entities.ApiResponse:
        """
        Fetches the account information.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_account()
        print(response)
        ```
        """
        return entities.ApiResponse(self.session.handler("GET", "/g/s/account"))

    def fetch_profile(self, userId: str) -> entities.UserProfile:
        """
        Fetches the profile information.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_profile()
        print(response)
        ```
        """
        return entities.UserProfile(self.session.handler("GET", f"/g/s/user-profile/{userId}"))

    def set_amino_id(self, amino_id: str) -> entities.ApiResponse:
        """
        Sets the amino id.

        `**Parameters**`

        - `aminoId` - The amino id to set.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.set_amino_id(aminoId="aminoId")
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/account/change-amino-id",
                data={"aminoId": amino_id, "timestamp": int(time.time() * 1000)},
            )
        )

    def fetch_wallet(self) -> entities.Wallet:
        """
        Fetches the wallet information.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_wallet()
        print(response)
        """
        return entities.Wallet(self.session.handler("GET", "/g/s/wallet"))

    def request_security_validation(
        self,
        email: str,
        reset_password: bool = False,
    ) -> entities.ApiResponse:
        """
        Requests a security validation.

        `**Parameters**`

        - `email` - The email of the account.

        - `resetPassword` - Whether to reset the password or not.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        response = bot.request_security_validation(email=email)
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/auth/request-security-validation",
                data={
                    "identity": email,
                    "type": 1,
                    "deviceID": self.session.generate.device_id(),
                    "level": 2 if reset_password else None,
                    "purpose": "reset-password" if reset_password else None,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def activate_email(self, email: str, code: str) -> entities.ApiResponse:
        """
        Activates an email.

        `**Parameters**`

        - `email` - The email of the account.

        - `code` - The code sent to the email.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        response = bot.activate_email(email=email, code=code)
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/auth/activate-email",
                data={
                    "type": 1,
                    "identity": email,
                    "data": {"code": code},
                    "deviceID": self.session.generate.device_id(),
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def verify(self, email: str, code: str, device_id: str) -> entities.ApiResponse:
        """
        Verifies the code sent to the email.

        `**Parameters**`

        - `email` - The email of the account.

        - `code` - The code sent to the email.

        - `deviceId` - The device id.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        response = bot.verify(email=email, code=code, deviceId=deviceId)
        print(response)
        ```
        """
        return entities.ApiResponse(
            self.session.handler(
                "POST",
                "/g/s/auth/check-security-validation",
                data={
                    "type": 1,
                    "identity": email,
                    "data": {"code": code},
                    "deviceID": device_id,
                    "timestamp": int(time.time() * 1000),
                },
            )
        )

    def reset_password(
        self,
        email: str,
        new_password: str,
        code: str,
        device_id: str
    ) -> entities.ResetPassword:
        """
        Resets the password.

        `**Parameters**`

        - `email` - The email of the account.

        - `newPassword` - The new password of the account.

        - `code` - The code sent to the email.

        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.reset_password(email=email, newPassword=newPassword, code=code)
        print(response)
        ```
        """
        return entities.ResetPassword(
            self.session.handler(
                "POST",
                "/g/s/auth/reset-password",
                data={
                    "updateSecret": f"0 {new_password}",
                    "emailValidationContext": {
                        "data": {"code": code},
                        "type": 1,
                        "identity": email,
                        "level": 2,
                        "deviceID": device_id,
                    },
                    "phoneNumberValidationContext": None,
                    "deviceID": device_id,
                },
            )
        )
