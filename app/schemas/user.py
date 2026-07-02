from pydantic import BaseModel, field_validator


class SendOTPRequest(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        return v


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str

    @field_validator('phone_number')
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        return v


class OTPResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    name: str | None = None
    phone_number: str

    class Config:
        from_attributes = True