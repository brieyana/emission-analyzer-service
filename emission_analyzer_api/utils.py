import json

def parse_model_output(s):
    try:
        parsed_output = json.loads(s)

        if "output" in parsed_output:
            parsed_output["output"] = json.loads(parsed_output["output"])
        return parsed_output
    
    except json.JSONDecodeError as e:
        raise Exception(f"Decode error: {str(e)}")
    
def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError as e:
        raise ValueError(f"Decode error: {str(e)}")
    
def validate_keys(data, required_keys, error_message=None):
    missing = [key for key in required_keys if key not in data]

    if missing:
        message = error_message or f"Missing required field(s): {', '.join(missing)}"
        raise ValueError(message)