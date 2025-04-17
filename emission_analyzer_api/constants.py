from enum import Enum

class HTTP_METHOD(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

USER_ID = "user_id"
ENGINE = "engine"
ENGINE_ID = "engine_identification"
ENGINE_TYPE = "engine_type"
BP_RATIO = "bp_ratio"
PRESSURE_RATIO = "pressure_ratio"
RATED_THRUST = "rated_thrust"

class ErrorCode(str, Enum):
    SOCKET_ERROR = "SOCKET_ERROR"
    DECODE_ERROR = "DECODE_ERROR"
    MISSING_FIELD = "MISSING_FIELD"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_METHOD = "INVALID_METHOD"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    ENGINE_NOT_FOUND = "ENGINE_NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"

class SuccessCode(str, Enum):
    ENGINE_UPDATED = "ENGINE_UPDATED"
    ENGINE_ADDED = "ENGINE_ADDED"

class ErrorType(str, Enum):
    PREDICTION_MODEL = "PREDICTION_MODEL"
    DATABASE = "DATABASE"
    CLIENT = "CLIENT"