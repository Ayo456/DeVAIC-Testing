import re

def parse_header_links(value: str) -> list[dict]:
    links = []
    for link_str in re.findall(r'<[^>]*>(?:\s*;\s*[^,]+)*', value):
        match = re.match(r'<([^>]*)>(.*)', link_str)
        if not match:
            continue
        
        url, params_str = match.groups()
        link_dict = {"url": url}
        
        for key, val1, val2 in re.findall(r';\s*([a-zA-Z*_-]+)\s*=\s*(?:"([^"]*)"|([^;,\s]+))', params_str):
            link_dict[key] = val1 if val1 != "" else val2
            
        links.append(link_dict)
        
    return links