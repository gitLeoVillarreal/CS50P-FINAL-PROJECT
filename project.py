import requests  
import unicodedata
from datetime import datetime, timedelta, timezone
API_key = "7863a84bb283f47d0dc415733fe5946e"  

def getLocalTime(apiTime):
    try:
        fixed_tz = timezone(timedelta(seconds=apiTime))
        time = datetime.now(fixed_tz)
        return time.strftime("%H:%M:%S") 
    except ValueError:
        print("Something went wrong...")   


def getWeather(lat, lon, name, state):
    try:
        icons = {
        "01d": "☀️",   "01n": "🌑",    
        "02d": "⛅",   "02n": "🌤️",   
        "03d": "☁️",   "03n": "☁️",
        "04d": "☁️",   "04n": "☁️",
        "09d": "🌧️",   "09n": "🌧️",
        "10d": "🌦️",   "10n": "🌧️",
        "11d": "🌩️",   "11n": "🌩️",
        "13d": "❄️",   "13n": "❄️",
        "50d": "🌫️",   "50n": "🌫️"
    }
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_key}")
        if response.status_code == 200:
            weatherData = response.json()
            if len(weatherData) == 0:
                raise ValueError
            print(f"\n=== WEATHER IN {name.upper()}, {state.upper().strip()} ===")
            print(f"-Main: {icons[weatherData['weather'][0]['icon']]}  {weatherData['weather'][0]['main']} {icons[weatherData['weather'][0]['icon']]}")
            print(f"-Current temperature: {int(weatherData['main']['temp'])}°C 🌡️")
            print(f"-Feels like: {int(weatherData['main']['feels_like'])}°C 🌡️")
            print(f"-Minimum temperature: {int(weatherData['main']['temp_min'])}°C 🌡️")
            print(f"-Maximum temperature: {int(weatherData['main']['temp_max'])}°C 🌡️")
            print(f"-Wind speed: {(weatherData['wind']['speed'])}m/s🍃")
            print(f"-Local time: {getLocalTime(weatherData['timezone'])}\n")
        else:
            raise requests.RequestException
    except ValueError:
        print("ERROR")
    except FileNotFoundError:
            print("////You haven't saved any cities yet")
    except requests.RequestException:
        print("///Something went wrong")
def getGeo(city, *argv): 
    try:
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_key}")
        validCity = False
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                raise ValueError
            if len(argv) == 1:
                for _, place in enumerate(data):
                    if place.get('name') and place.get('state'):
                        if place.get('name') == city and place.get('state') == argv[0]:
                            name = place.get("name")
                            state = place.get("state")
                            lat = place.get("lat")
                            lon = place.get("lon")
                            validCity = True
                            break 
                        else:
                            continue
                
                if validCity == False:
                    print("Invalid city...", end="")
                    raise ValueError

            elif len(argv) == 0:
                print(f"== SELECT WICH {city.upper()} ==")
                counter = 1
                validCities = []
                for _, place in enumerate(data):
                    if place.get("state"):
                        print(f"{counter}.- {place['name']}, {place['state']}")
                        validCities.append(place)
                        counter += 1
                op = int(input("Select the number of your city: "))-1
                if op < 0 or op >= len(validCities):
                    print("Invalid option...", end="")
                    raise ValueError
            
                selected = validCities[op]
                name = selected.get("name")
                state = str(selected.get("state"))
                lat = selected.get("lat")
                lon = selected.get("lon")
                validCity = True
      
            else:
                print("Argv error")
                raise ValueError
            
            return lat, lon, name, state
        else:
            raise requests.RequestException
    except ValueError:
        print("ERROR")
        return None
    except FileNotFoundError:
            print("////You haven't saved any cities yet")
    except requests.RequestException:
        print("///Something went wrong")
    
    
def quickCheck():
    try:
        capture = input("Insert a city (for specified city please use ',' ex: 'city', 'state'): ").title()

        if ', ' in capture:
            city, state = capture.split(", ")
            result = getGeo(city, state)
        elif not ', ' in capture:
            result = getGeo(capture)
        else:
            raise ValueError
        
        if result != None:
            lat, lon, name, state = result
            getWeather(lat, lon, name, state)
    except ValueError:
        print("ERROR")
    except FileNotFoundError:
            print("////You haven't saved any cities yet")
def checkRepeatedCities(Favourites, cityAdded):
    with open(Favourites, 'r') as file:
        cities = file.read()
        if cityAdded in cities:
            return True
        else:
            return False
        
def compareCitiesWithDifferentCharacters(capture, city):
    try:
        capName, capState = capture.split(", ")
        cityName, cityState = city.split(", ")
    except ValueError:
        return False
    normalizedCapName = unicodedata.normalize('NFKD', capName).encode('ascii', 'ignore').decode('utf-8').casefold()
    normalizedCapState = unicodedata.normalize('NFKD', capState).encode('ascii', 'ignore').decode('utf-8').casefold()

    normalizedCityName = unicodedata.normalize('NFKD', cityName).encode('ascii', 'ignore').decode('utf-8').casefold()
    normalizedCityState = unicodedata.normalize('NFKD', cityState).encode('ascii', 'ignore').decode('utf-8').casefold()

    if (normalizedCapName in normalizedCityName) and normalizedCapState == normalizedCityState:
        return True
    else:
        return False

#adds a city to the file Favourites    
def addCity(Favourites):
    try:
        with open(Favourites, 'a') as file:
            while True:
                capture = input("Insert a city (for specified city please use ',' ex: 'city', 'state') or ? to exit: ").title()
            #The program exits when the user type '?'
                if capture == '?':
                    return False
            #if the user type an unspecified city the program will display the cities with that name
                elif not ', ' in capture:
                    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={capture}&limit=5&appid={API_key}")
                    data = response.json()
                    if len(data) == 0:
                        print("Invalid city...", end="")
                        raise ValueError
                    print(f"== SELECT WICH {capture.upper()} ==")
                    counter = 1
                    validCities = []
                    for _, place in enumerate(data):
                        if place.get("state"):
                            print(f"{counter}.- {place['name']}, {place['state']}")
                            validCities.append(place)
                            counter += 1
                    op = int(input("Select the number of your city: "))-1
                    if op < 0 or op >= len(validCities):
                        print("Invalid option...", end="")
                        raise ValueError
                    selected = validCities[op]
                    cityAdded = selected.get('name') + ", " +selected.get('state')
            #if the type a specified city the program will check if that city is valid
                elif ', ' in capture:
                    city, state = capture.split(", ")
                    if ' ' in city:
                        city = city.replace(" ", "_")
                    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_key}")
                    data = response.json()
                    validCity = False
                    for _, place in enumerate(data):
                        if place.get('name') and place.get('state'):
                            lookingForCity = place.get('name') + ", " + place.get('state')
                            if compareCitiesWithDifferentCharacters(capture, lookingForCity):
                                cityAdded = lookingForCity
                                validCity = True
                                break 
                        else:
                            continue
                    if validCity == False:
                        print("Invalid city...", end="")
                        raise ValueError
                else:
                    raise ValueError
            
                if not checkRepeatedCities(Favourites, cityAdded):
                    file.write(cityAdded + "\n")
                    print("~Your city has been saved.")
                else:
                    print("This city has been already saved before...", end="")
                    raise ValueError
    except ValueError:
        print("ERROR")
    except FileNotFoundError:
            print("////You haven't saved any cities yet")        
        
def checkWeatherInSavedCities(city, state):
    result = getGeo(city, state)
    if result != None:
        lat, lon, name, state = result
        getWeather(lat, lon, name, state)

def savedCities(Favourites):
    try:
        with open(Favourites) as file:
            cities = file.readlines()
        if len(cities) == 0:
            print("///You haven't saved any cities yet.")
        else:
            with open(Favourites, 'r') as file:
                print("== SAVED CITIES ==")
                for i, c in enumerate(cities):
                    print(f"{i+1}.- {c.strip('\n')}")
                op = int(input("Select the number of your city: "))-1
                if op < 0 or op >= len(cities):
                    print("Invalid option...", end="")
                    raise ValueError
                city, state = cities[op].split(', ')
                checkWeatherInSavedCities(city, state.strip())
    except ValueError:
        print("ERROR")
    except FileNotFoundError:
            print("////You haven't saved any cities yet")

#delete as many cities as the user wants
def deleteCities(Favourites):
    with open(Favourites) as file:
        cities = file.readlines()
    if len(cities) == 0:
        print("///You haven't saved any cities yet.")
    else:
        with open(Favourites, 'r') as file:
            print("== SAVED CITIES ==")
            for i, c in enumerate(cities):
                print(f"{i+1}.- {c.strip('\n')}")
            amount = int(input("How many cities you will delete?: "))
            if amount > len(cities) or amount < 0:
                print("Invalid amount of cities")
            else:
                citiesToDelete = []
                with open(Favourites, 'w') as file:
                    for _ in range(amount):
                        index = int(input("Select the number of the city you want to delete: "))-1
                        if index < 0 or index >= len(cities):
                            print("//// Invalid city number. Try again.")
                        elif index in citiesToDelete:
                            print("//// This city is already selected. Try another.")
                        else:
                            citiesToDelete.append(index)

                    for j, city in enumerate(cities):
                        if j not in citiesToDelete:
                            file.write(city)
                    print("~YOUR CITY(IES) HAVE BEEN DELETED")

def main():  
    Favourites = "FavouritesCities.txt"
    while True:
        print("=== WEATHER APP ===")
        print("a) Quick check.\n"
            + "b) Save a city.\n"
            + "c) Saved cities.\n"
            + "d) Delete city.\n"
            + "e) Exit.\n")
        op = input("Select an option: ").lower()
        if op == 'a':
            quickCheck()
        elif op == 'b':
            addCity(Favourites)
        elif op == "c":
            savedCities(Favourites)
        elif op == "d":
            deleteCities(Favourites)
        elif op == "e":
            return False
        else:
            print("///Invalid option...")
    
if __name__ == "__main__":
    main()
