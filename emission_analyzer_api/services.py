import socket
import os
from .utils import parse_model_output
from .models import *
from .constants import *
from .responses import *

def perform_prediction(bp_ratio, pressure_ratio, rated_thrust):
    try:
        with socket.create_connection(("model", os.getenv("MODEL_PORT"))) as s:
            s.sendall(f"{bp_ratio} {pressure_ratio} {rated_thrust}\n".encode())
            raw_output = s.recv(1024)
    except (socket.error, socket.timeout) as e:
        raise Error(e, ErrorCode.SOCKET_ERROR, ErrorType.PREDICTION_MODEL, 500)
    
    try:
        output = raw_output.decode("utf-8").strip()
    except UnicodeDecodeError as e:
        raise Error(e, ErrorCode.DECODE_ERROR, ErrorType.PREDICTION_MODEL, 500)

    return parse_model_output(output)

def create_user(user_id):
    return User.objects.get_or_create(user_id=user_id)

def get_user(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        raise Error("User not found", ErrorCode.USER_NOT_FOUND, ErrorType.CLIENT, 404)
    

def get_engine(user, engine_id):
    try:
        return Engine.objects.get(user=user, engine_identification=engine_id)
    except Engine.DoesNotExist:
        raise Error("Engine not found", ErrorCode.ENGINE_NOT_FOUND, ErrorType.CLIENT, 404)
    

def get_engines_types():
    try:
        types = []
        for type in EngineType.objects.all():
            types.append(type.type)
        return types
    except:
        raise Error("Database error", ErrorCode.VALIDATION_ERROR, ErrorType.DATABASE, status=400)

def edit_engine(engine, engine_type, data): 
    try:   
        engine.engine_type = engine_type
        engine.bp_ratio = data[BP_RATIO]
        engine.pressure_ratio = data[PRESSURE_RATIO]
        engine.rated_thrust = data[RATED_THRUST]
        engine.save()
        return engine
    except:
        raise Error("Database error", ErrorCode.VALIDATION_ERROR, ErrorType.DATABASE, status=400)
    
def add_engine(data, user, engine_type):
    try:
        engine = Engine.objects.create(
            user=user,
            engine_identification=data[ENGINE][ENGINE_ID],
            engine_type=engine_type,
            rated_thrust=data[ENGINE][RATED_THRUST],
            bp_ratio=data[ENGINE][BP_RATIO],
            pressure_ratio=data[ENGINE][PRESSURE_RATIO]
        )
        return engine
    except:
        raise Error("Database error", ErrorCode.VALIDATION_ERROR, ErrorType.DATABASE, status=400)

def get_engines(user):
    engines = Engine.objects.filter(user=user)

    engines_list = []
    for engine in engines:
        engines_list.append({
            "engine_identification": engine.engine_identification,
            "engine_type": engine.engine_type.type,
            "rated_thrust": float(engine.rated_thrust),
            "bp_ratio": float(engine.bp_ratio),
            "pressure_ratio": float(engine.pressure_ratio)
        })

    return engines_list

def get_engine_type(engine_type):
    try:
        return EngineType.objects.get(type=engine_type)
    except EngineType.DoesNotExist:
        raise Error("Engine Type not found", ErrorCode.VALIDATION_ERROR, ErrorType.CLIENT, 404)