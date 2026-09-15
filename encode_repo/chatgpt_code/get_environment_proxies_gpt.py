from urllib.request import getproxies


def get_environment_proxies():
    proxy_info = getproxies()
    proxies = {}

    for scheme in ("http", "https", "all"):
        proxy = proxy_info.get(scheme)

        if proxy:
            if "://" not in proxy:
                proxy = "http://" + proxy

            proxies[f"{scheme}://"] = proxy

    no_proxy = proxy_info.get("no")

    if no_proxy is None:
        return proxies

    if no_proxy.strip() == "*":
        return {}

    for hostname in no_proxy.split(","):
        hostname = hostname.strip()

        if hostname:
            proxies[f"all://*{hostname}"] = None

    return proxies