def parse_header_links(header):
    links = []

    for link in header.split(","):
        parts = link.strip().split(";")

        uri = parts[0].strip()

        if uri.startswith("<") and uri.endswith(">"):
            uri = uri[1:-1]

        parsed_link = {"url": uri}

        for param in parts[1:]:
            param = param.strip()

            if "=" in param:
                key, value = param.split("=", 1)
                value = value.strip().strip('"')
                parsed_link[key.strip()] = value

        links.append(parsed_link)

    return links