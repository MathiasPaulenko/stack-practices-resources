"""Phone number parsing, validation and formatting with python-phonenumbers.

Install: pip install phonenumbers
Run:     python format_phone.py
"""

import phonenumbers
from phonenumbers import PhoneNumberFormat, PhoneNumberType

_TYPE_NAMES = {
    getattr(PhoneNumberType, name): name
    for name in dir(PhoneNumberType)
    if name.isupper()
}


def parse_and_format(raw: str, region: str = "US") -> dict:
    """Parse raw input and return the canonical formats plus validity flags."""
    try:
        number = phonenumbers.parse(raw, region)
    except phonenumbers.NumberParseException as exc:
        return {"raw": raw, "error": str(exc)}

    return {
        "raw": raw,
        "possible": phonenumbers.is_possible_number(number),
        "valid": phonenumbers.is_valid_number(number),
        "e164": phonenumbers.format_number(number, PhoneNumberFormat.E164),
        "international": phonenumbers.format_number(number, PhoneNumberFormat.INTERNATIONAL),
        "national": phonenumbers.format_number(number, PhoneNumberFormat.NATIONAL),
        "rfc3966": phonenumbers.format_number(number, PhoneNumberFormat.RFC3966),
        "extension": number.extension or None,
        "type": _TYPE_NAMES.get(phonenumbers.number_type(number), "UNKNOWN"),
    }


if __name__ == "__main__":
    samples = [
        ("(415) 555-2671", "US"),
        ("020 7946 0958", "GB"),
        ("+52 55 1234 5678", "MX"),
        ("+1 555-1234 ext. 42", "US"),
        ("not a number", "US"),
    ]
    for raw, region in samples:
        print(f"{raw!r} [{region}] ->")
        result = parse_and_format(raw, region)
        for key, value in result.items():
            if key != "raw":
                print(f"    {key}: {value}")
        print()
