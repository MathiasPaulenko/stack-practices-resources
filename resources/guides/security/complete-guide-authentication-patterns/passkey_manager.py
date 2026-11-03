"""WebAuthn passkey registration and authentication.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
import json
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
)


class PasskeyManager:
    def __init__(self, rp_id: str, rp_name: str, origin: str):
        self.rp_id = rp_id
        self.rp_name = rp_name
        self.origin = origin

    def generate_registration(self, user_id: str, username: str) -> dict:
        options = generate_registration_options(
            rp_id=self.rp_id,
            rp_name=self.rp_name,
            user_id=user_id.encode(),
            user_name=username,
            authenticator_selection={
                "authenticatorAttachment": "platform",
                "userVerification": "required",
            },
        )
        return {
            "options": json.dumps(options.to_dict()),
            "challenge": options.challenge,
        }

    def verify_registration(self, credential: dict, challenge: bytes) -> bool:
        try:
            verification = verify_registration_response(
                credential=credential,
                expected_challenge=challenge,
                expected_origin=self.origin,
                expected_rp_id=self.rp_id,
            )
            # db.store_credential(user_id, verification.credential_id,
            #                     verification.credential_public_key)
            return True
        except Exception:
            return False

    def generate_authentication(self) -> dict:
        options = generate_authentication_options(
            rp_id=self.rp_id, user_verification="required"
        )
        return {
            "options": json.dumps(options.to_dict()),
            "challenge": options.challenge,
        }

    def verify_authentication(
        self,
        credential: dict,
        challenge: bytes,
        stored_public_key: bytes,
        stored_sign_count: int,
    ) -> bool:
        try:
            verification = verify_authentication_response(
                credential=credential,
                expected_challenge=challenge,
                expected_origin=self.origin,
                expected_rp_id=self.rp_id,
                credential_public_key=stored_public_key,
                credential_current_sign_count=stored_sign_count,
            )
            return True
        except Exception:
            return False
