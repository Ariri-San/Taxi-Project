import googlemaps
import os
import environ

env = environ.Env()
environ.Env.read_env()


class ApiGoogle():
    def __init__(self) -> None:
        key = os.environ['KEY']
        self.gmaps = googlemaps.Client(key=key)
    
    
    def find_places(self, name):
        try:
            find_places = self.gmaps.places_autocomplete(name, components={'country': ['UK']})
            
            list_show = ["formatted_address", "name", "url", "geometry"]
            find_places_2 = []
            for i in find_places:
                place = self.gmaps.place(i["place_id"])["result"]
                find_places_2.append({j:place[j] for j in place if j in list_show})
            
            if find_places_2:
                return find_places_2
            return True
        except:
            return False
    
    
    def find_distance(self, origin, destination):
        try:
            distance = self.gmaps.distance_matrix(origins=origin, destinations=destination)
            print(distance)
            return distance
        except:
            return False
        