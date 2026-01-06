import os

def get_env_var(var_name: str) -> str:
    """Get an environment variable or raise an error if not found."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Environment variable {var_name} not found.")
    return value