from datetime import datetime
from urllib.parse import urlparse
import requests, socket, tldextract


def returnSpecialDomainList():
    return ["gov", "edu"]


def returnHeaders() -> dict:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }


def contentIsUrl(url: str) -> bool:
    try:
        response = requests.get(url=url, headers=returnHeaders())
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


def getIpAddress(domain_name: str):
    try:
        ip_address = socket.gethostbyname(domain_name)
        if ip_address:
            return ip_address
        else:
            return False
    except:
        return False




def getIpCountry(ip_address: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        if response["status"] == "success":
            return response["countryCode"].lower()
    except:
        return False


def getDomainInformationsFromUrl(url: str) -> dict[str | int] | bool:
    if contentIsUrl(url=url):
        __dn = urlparse(url=url).netloc
        extracted = tldextract.extract(url).suffix
        domainIsSpecial = "".join(
            [x for x in returnSpecialDomainList() if extracted.startswith(x)]
        )
        IpAddress = getIpAddress(domain_name=__dn)
        country = getIpCountry(IpAddress)
        if domainIsSpecial:
            return {
                "status": True,
                "domain_name": str(__dn),
                "extention": str(extracted),
                "is_special": True,
                "ip_address": IpAddress,
                "point": 5,
                "country": country,
            }

        else:
            return {
                "status": False,
                "domain_name": str(__dn),
                "extention": str(extracted),
                "is_special": False,
                "ip_address": IpAddress,
                "point": 2,
                "country": country,
            }

    else:
        return False


def getDominBeforeContent(domain: str):
    year = datetime.now().year
    url = f"http://archive.org/wayback/available?url={domain}&timestamp={year}"
    response = requests.get(url=url).json()["archived_snapshots"]

    return dict(response)["closest"]["url"]


def passwordController(password: str):
    if (
        any(_.islower() for _ in password)
        and any(_.isupper() for _ in password)
        and any(_.isdigit() for _ in password)
    ):
        return True

    else:
        return False

