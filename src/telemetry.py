import time
import logging
import json
from functools import wraps

# Setup structured logging configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("ML_Telemetry")

def track_ml_metrics(node_name: str):
    """Decorator to measure agent node execution latency and log structured audit data."""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            
            # Execute the underlying agent node logic
            response, token_meta = await func(*args, **kwargs)
            
            end_time = time.perf_counter()
            latency_ms = round((end_time - start_time) * 1000, 2)
            
            # Formulate structural audit footprint log
            audit_log = {
                "event": "AGENT_NODE_EXECUTION",
                "node_name": node_name,
                "latency_ms": latency_ms,
                "model_utilized": token_meta.get("model", "unknown"),
                "prompt_tokens": token_meta.get("prompt_tokens", 0),
                "completion_tokens": token_meta.get("completion_tokens", 0),
                "total_tokens": token_meta.get("total_tokens", 0)
            }
            
            # Output structured JSON audit trail to simulated log collector
            logger.info(json.dumps(audit_log, indent=2))
            return response, audit_log
            
        return async_wrapper
    return decorator