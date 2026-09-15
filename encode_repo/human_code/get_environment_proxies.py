import typing from urllib.request 
import getproxies

def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]:
    proxy_info = getproxies()
    mounts: typing.Dict[str, typing.Optional[str]] = {}

    for scheme in ("http", "https", "all"):
        if proxy_info.get(scheme):
            hostname = proxy_info[scheme]
            mounts[f"{scheme}://"] = (
                hostname if "://" in hostname else f"http://{hostname}"
            )

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        if hostname == "*":
            return {}
        elif hostname:
            mounts[f"all://*{hostname}"] = None
    return mounts