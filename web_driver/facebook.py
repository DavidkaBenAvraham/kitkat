# -*- coding: utf-8 -*-
#!/usr/bin/env python
##
# @package Katia.Driver.facebook
from loguru import logger


## https://qna.habr.com/q/1162122
def face_token():
    """Get TOKEN"""
    from bs4 import BeautifulSoup
    import httpx
    import ssl
    
    uri = "https://www.facebook.com/adsmanager/manage"
    ctx = ssl.create_default_context()
    client = httpx.Client(verify=ctx)
    r = client.get(
        url=uri,
        headers={
            "Host": "www.facebook.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://www.facebook.com/index.php?next=https%3A%2F%2Fwww.facebook.com%2Fadsmanager%2Fmanage",
            "Connection": "keep-alive",
            "Cookie": "cookies_there",  # use the cookies that you receive after logging into your account
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        },
    )
    logger.error("[* Response headers]\n", r.headers)
    # From headers you can get => privacy_mutation_token(see x-fb-debug) =
    # "eyJ0eXBlIjowLCJjcmVhdGlvbl90aW1lIjoxNjU0NzE4MTg0LCJjYWxsc2l0ZV9pZCI6MzgxMjI5MDc5NTc1OTQ2fQ=="
    # use it for POST https://www.facebook.com/login/?privacy_mutation_token=
    # eyJ0eXBlIjowLCJjcmVhdGlvbl90aW1lIjoxNjU0NzE4MTg0LCJjYWxsc2l0ZV9pZCI6MzgxMjI5MDc5NTc1OTQ2fQ==

    body = BeautifulSoup(r.text, "lxml")
    logger.error("[* All JS scripts]")
    # find all scripts one of them will be "accessToken"
    for script in body.find_all("script"):
        logger.error(script)


if __name__ == "__main__":
    face_token()
