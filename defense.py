import logging
from utils import calculate_entropy

logging.basicConfig(
    filename='logs/traffic.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class DNSDefender:
    def __init__(self, entropy_threshold: float = 4.2, length_threshold: int = 25):
        self.entropy_threshold = entropy_threshold
        self.length_threshold = length_threshold
        self.blocked_domains = set()

    def analyze_query(self, query: str) -> dict:
        subdomain = query.split('.')[0]
        entropy = calculate_entropy(subdomain)
        
        is_anomalous = False
        reason = ""

        if entropy > self.entropy_threshold:
            is_anomalous = True
            reason = "High Entropy"
        elif len(subdomain) > self.length_threshold:
            is_anomalous = True
            reason = "Suspicious Length"

        if is_anomalous:
            self._block_domain(query)
            logging.warning(f"BLOCKED: {query} | Reason: {reason} | Entropy: {entropy:.2f}")
            return {"status": "BLOCKED", "query": query, "entropy": entropy, "reason": reason}
        else:
            logging.info(f"ALLOWED: {query}")
            return {"status": "ALLOWED", "query": query, "entropy": entropy, "reason": "Normal Traffic"}

    def _block_domain(self, query: str):
        parts = query.split('.')
        if len(parts) >= 2:
            base_domain = f"{parts[-2]}.{parts[-1]}"
            self.blocked_domains.add(base_domain)
