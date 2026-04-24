import math
import base64

def calculate_entropy(data: str) -> float:
    if not data:
        return 0.0
    
    entropy = 0.0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy -= p_x * math.log2(p_x)
    return entropy

def encode_for_dns(secret_data: str) -> str:
    encoded_bytes = base64.urlsafe_b64encode(secret_data.encode('utf-8'))
    return encoded_bytes.decode('utf-8').rstrip('=')
