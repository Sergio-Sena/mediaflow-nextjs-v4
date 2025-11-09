import json
import time
from datetime import datetime

class Logger:
    def __init__(self, lambda_name, correlation_id=None):
        self.lambda_name = lambda_name
        self.correlation_id = correlation_id or str(int(time.time() * 1000))
        self.start_time = time.time()
    
    def _log(self, level, message, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "lambda": self.lambda_name,
            "correlation_id": self.correlation_id,
            "message": message,
            "duration_ms": int((time.time() - self.start_time) * 1000)
        }
        log_entry.update(kwargs)
        print(json.dumps(log_entry))
    
    def info(self, message, **kwargs):
        self._log("INFO", message, **kwargs)
    
    def error(self, message, **kwargs):
        self._log("ERROR", message, **kwargs)
    
    def warn(self, message, **kwargs):
        self._log("WARN", message, **kwargs)
    
    def metric(self, metric_name, value, unit="Count"):
        self._log("METRIC", f"Metric: {metric_name}", metric_name=metric_name, value=value, unit=unit)
