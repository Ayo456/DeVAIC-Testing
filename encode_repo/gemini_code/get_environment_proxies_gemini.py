import os
import urllib.request

def get_environment_proxies() -> dict[str, str | None]:
    raw_proxies = urllib.request.getproxies()
    
    no_proxy = os.environ.get("no_proxy") or os.environ.get("NO_PROXY")
    if no_proxy:
        no_proxy = no_proxy.strip()
        if no_proxy == "*":
            return {}

    proxies: dict[str, str | None] = {}
    for scheme in ("http", "https", "all"):
        if scheme in raw_proxies:
            proxy_url = raw_proxies[scheme]
            if "://" not in proxy_url:
                proxy_url = f"http://{proxy_url}"
            proxies[scheme] = proxy_url

    if no_proxy:
        for host in no_proxy.split(","):
            host = host.strip()
            if host:
                proxies[f"all://*{host}"] = None

    return proxies