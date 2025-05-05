class ParameterValidationError(ValueError):
    """Custom exception for invalid engine operational parameters."""
    pass

# Define reasonable bounds based on typical commercial turbofan engines.
# These ranges might need adjustment based on the specific scope of engines
# your application targets and the units expected by your model/database.
# Units assumed here are conceptual floats as per the model definition.
MIN_THRUST = 0.1       # Thrust must be positive
MAX_THRUST = 1000.0    # Arbitrary upper limit (e.g., kN)
MIN_BP_RATIO = 0.0     # Bypass ratio cannot be negative
MAX_BP_RATIO = 15.0    # Upper range for high-bypass engines
MIN_PRESSURE_RATIO = 1.1 # Overall Pressure Ratio must be > 1
MAX_PRESSURE_RATIO = 60.0 # Upper range for modern engines

def validate_engine_parameters(rated_thrust, bp_ratio, pressure_ratio):
    """
    Validates engine operational parameters (rated_thrust, bp_ratio, pressure_ratio).

    Args:
        rated_thrust (float): The engine's rated thrust.
        bp_ratio (float): The engine's bypass ratio.
        pressure_ratio (float): The engine's overall pressure ratio.

    Raises:
        ParameterValidationError: If any parameter is outside its defined valid range,
                                  containing a descriptive message.
    """
    errors = []
    parameter_details = {
        "Rated Thrust": (rated_thrust, MIN_THRUST, MAX_THRUST),
        "Bypass Ratio": (bp_ratio, MIN_BP_RATIO, MAX_BP_RATIO),
        "Pressure Ratio": (pressure_ratio, MIN_PRESSURE_RATIO, MAX_PRESSURE_RATIO),
    }

    # Check ranges
    if not (MIN_THRUST < rated_thrust <= MAX_THRUST):
        errors.append(f"Rated thrust ({rated_thrust})")
    if not (MIN_BP_RATIO <= bp_ratio <= MAX_BP_RATIO):
        errors.append(f"Bypass ratio ({bp_ratio})")
    if not (MIN_PRESSURE_RATIO < pressure_ratio <= MAX_PRESSURE_RATIO):
        errors.append(f"Pressure ratio ({pressure_ratio})")

    if errors:
        # Construct the error message
        error_message = ", ".join(errors) + " out of valid range."
        # Use the specific message format requested in the issue
        raise ParameterValidationError("Rated thrust, B/P ratio, or pressure ratio are out of valid range.")

    # If all checks pass, the function completes without raising an error.