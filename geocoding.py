import requests

while True:
    try :
        # Base Url for geocoding
        url = "https://us1.locationiq.com/v1/search.php"

        address = input("\n Input the address: ")

        #Your unique private_token should replace value of the private_token variable.
        #To know how to obtain a unique private_token please refer the README file for this script.
        private_token = "pk.e06a20fc9226bad7da5908c21d85b421"

        data = {
            'key': private_token,
            'q': address,
            'format': 'json'
        }

        response = requests.get(url, params=data)

        latitude = response.json()[0]['lat']
        longitude = response.json()[0]['lon']
        disname = response.json()[0]['display_name']

        print(f"The latitude of the given address is: {latitude}")
        print(f"The longitude of the given address is: {longitude}")
        print(disname)
    
    except KeyError :
        print("Enter a valid location name")
        pass

    except KeyboardInterrupt:
        break