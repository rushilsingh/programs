import requests

url = "http://maps.googleapis.com/maps/api/geocode/json?address="

def get_address(address):
    """ Lookup address string using maps api and get json
        Return formatted address field from json """
    try:
        data = requests.get(url+address).json()['results'][0]
    except:
        result = "No results found"
    else:
        adr = data['formatted_address']
        lat = str(data['geometry']['location']['lat'])
        lng = str(data['geometry']['location']['lng'])

        result = ""
        result += "Address: "+adr+'\n'
        result += "Latitude: "+lat+'\n'
        result += "Longitude: "+lng
    finally:
        return result


def main():

    print "Ctrl+C to exit"
    while True:
        address = raw_input("Enter:")
        print get_address(address)

if __name__ == '__main__':
    main()
