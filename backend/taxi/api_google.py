import googlemaps
import os
import environ
from asgiref.sync import async_to_sync, sync_to_async

env = environ.Env()
environ.Env.read_env()


class ApiGoogle():
    def __init__(self) -> None:
        key = os.environ['KEY']
        self.gmaps = googlemaps.Client(key=key)
    
    
    def find_place(self, name):
        try:
            find_places = self.gmaps.places_autocomplete(name, components={'country': ['UK']})
            
            for place in find_places:
                if name == place["description"]:
                    return True
            
            return False
        except:
            return False
    
    
    def find_places(self, name):
        try:
            find_places = self.gmaps.places_autocomplete(name, components={'country': ['UK']})
            
            list_show = ["formatted_address", "name", "url", "geometry"]
            find_places_2 = []
            for place in find_places:
                place = self.gmaps.place(place["place_id"])["result"]
                find_places_2.append({j:place[j] for j in place if j in list_show})
            
            if find_places_2:
                return find_places_2
            
            return True
        except:
            return False
    afind_places = sync_to_async(find_places, thread_sensitive=False)
    
    
    def find_distance(self, origin, destination):
        try:
            distance = self.gmaps.distance_matrix(origins=origin, destinations=destination)
            
            distance_meter = distance["rows"][0]["elements"][0]["distance"]["value"]
            duration = distance["rows"][0]["elements"][0]["duration"]["text"]
            
            return {"distance_meter": distance_meter, "duration": duration}
        except:
            return False
    afind_distance = sync_to_async(find_distance, thread_sensitive=False)
    
        