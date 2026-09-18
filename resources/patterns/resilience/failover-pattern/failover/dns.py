# failover/dns.py — DNS-based failover for multi-region
import dns.resolver
import time

class DNSFailover:
    """DNS-based failover: updates DNS records to point to standby.
    Slower propagation but works across regions."""

    def __init__(self, domain, primary_ip, standby_ip,
                 dns_server, ttl=60):
        self.domain = domain
        self.primary_ip = primary_ip
        self.standby_ip = standby_ip
        self.dns_server = dns_server
        self.ttl = ttl
        self._active_ip = primary_ip

    def check_and_failover(self, health_url):
        """Check primary health and update DNS if needed."""
        import requests
        try:
            resp = requests.get(health_url, timeout=5)
            if resp.status_code == 200:
                if self._active_ip != self.primary_ip:
                    self._update_dns(self.primary_ip)
                    self._active_ip = self.primary_ip
                    print(f"DNS failback to primary: {self.primary_ip}")
                return True
        except Exception:
            pass

        # Primary is down — fail over
        if self._active_ip == self.primary_ip:
            self._update_dns(self.standby_ip)
            self._active_ip = self.standby_ip
            print(f"DNS failover to standby: {self.standby_ip}")

        return False

    def _update_dns(self, ip):
        """Update DNS A record (implementation depends on DNS provider)."""
        # Example: AWS Route 53 API call
        # change_route53_record(self.domain, ip, self.ttl)
        print(f"Updating DNS: {self.domain} -> {ip} (TTL: {self.ttl}s)")

    def resolve_current(self):
        """Check what IP the domain currently resolves to."""
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(self.domain, "A")
        return [rdata.address for rdata in answers]


if __name__ == "__main__":
    fo = DNSFailover(
        domain="api.example.com",
        primary_ip="203.0.113.10",
        standby_ip="203.0.113.20",
        dns_server="ns1.example.com",
        ttl=60,
    )
    print(fo.resolve_current())
