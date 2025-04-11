import socket
import os
from .utils import parse_model_output

def perform_prediction(bp_ratio, pressure_ratio, rated_thrust):
    try:
        with socket.create_connection(("model", os.getenv("MODEL_PORT"))) as s:
            s.sendall(f"{bp_ratio} {pressure_ratio} {rated_thrust}\n".encode())
            raw_output = s.recv(1024)
    except (socket.error, socket.timeout) as e:
        raise Exception(f"Socket error: {str(e)}")
    
    try:
        output = raw_output.decode("utf-8").strip()
    except UnicodeDecodeError as e:
        raise Exception(f"Decode error: {str(e)}")

    return parse_model_output(output)
