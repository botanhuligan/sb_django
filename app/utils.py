import requests
MAC_URL = 'http://macvendors.co/api/%s'


def get_data_by_mac(mac):
    request = requests.get(MAC_URL % mac)
    body = request.json()
    res = {}
    if body and "result" in body:
        result = body["result"]
        if "company" in result:
            res["company"] = result["company"]
        if "address" in result:
            res["address"] = result["address"]
    return res


if __name__ == "__main__":
    import uuid
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff )for ele in range(0,8*6,8)][::-1])
    print(get_data_by_mac(mac))
