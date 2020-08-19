def ip_info(ip_address, mode='json'):
    from ip2geotools.databases.noncommercial import DbIpCity
    if ip_address is None:
        return {}
    response = DbIpCity.get(ip_address=ip_address, api_key='free')
    if response is None:
        return {}
    if mode.__eq__('json'):
        return response.to_json()
    res = {}
    try:
        res['ip_address'] = ip_address
        res['city'] = response.city
        res['region'] = response.region
        res['country'] = response.country
        res['geo_lat'] = response.latitude
        res['geo_long'] = response.longitude
        return res
    except Exception as e:
        print(e.__str__())
        return res
