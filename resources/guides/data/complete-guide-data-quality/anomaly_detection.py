import numpy as np

def detect_row_count_anomalies(current_count, historical_counts, threshold=3.0):
    mean = np.mean(historical_counts)
    std = np.std(historical_counts)
    z = (current_count - mean) / std if std > 0 else 0
    return {"current": current_count, "mean": round(mean, 2), "std": round(std, 2), "z_score": round(z, 2), "is_anomaly": abs(z) > threshold, "direction": "high" if z > 0 else "low"}

def detect_null_rate_anomaly(current_null_rate, historical_rates, threshold=3.0):
    mean = np.mean(historical_rates)
    std = np.std(historical_rates)
    z = (current_null_rate - mean) / std if std > 0 else 0
    return {"current_rate": current_null_rate, "mean_rate": round(mean, 4), "z_score": round(z, 2), "is_anomaly": z > threshold}

if __name__ == "__main__":
    hist = [1200, 1150, 1300, 1250, 1180] * 6
    print(detect_row_count_anomalies(500, hist))
