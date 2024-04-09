import googlemaps
import os
import environ
import datetime
from . import models
# from asgiref.sync import async_to_sync, sync_to_async

env = environ.Env()
environ.Env.read_env()


class ApiGoogle():
    def __init__(self) -> None:
        key = os.environ['KEY']
        self.gmaps = googlemaps.Client(key=key)
        

    def check_datetime(self, joined_prices, datetime):
        # now = datetime.datetime.now()
        day = datetime.isoweekday()
        if day == 7:
            day = "S"
        else:
            day = "O"
        time = datetime.time()
        
        for joined_price in joined_prices:
            start = joined_price.priceday.start
            finish = joined_price.priceday.finish
            if joined_price.day_of_week == day:
                
                if start < finish:
                    if start <= time <= finish:
                        return joined_price
                else:
                    if time > start or time < finish:
                        return joined_price
    
    
    def check_fixed_price(self, origin, destination):
        fixed_origin = models.FixedPrice.objects.filter(formated_address=origin).all()
        fixed_destination = models.FixedPrice.objects.filter(formated_address=destination).all()
        
        price = 0
        if fixed_origin:
            price = fixed_origin[0].price
        if fixed_destination:
            if fixed_destination[0].price > price:
                price = fixed_destination[0].price
        if price > 0:
            return price
        else:
            return False
    
    
    def find_place(self, name):
        # try:
            find_places = self.gmaps.find_place(name, "textquery")["candidates"]
            
            for place in find_places:
                place_2 = self.gmaps.place(place["place_id"])["result"]
                if place_2["formatted_address"] in name or name in place_2["formatted_address"]:
                    return name, place_2["geometry"]["location"]["lat"], place_2["geometry"]["location"]["lng"]
            return False
        # except:
        #     return False
    
    
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
    # afind_places = sync_to_async(find_places, thread_sensitive=False)
    
    
    def find_distance(self, origin, destination, date, date_return):
        try:
            distance = self.gmaps.distance_matrix(origins=origin, destinations=destination)
            
            meter = distance["rows"][0]["elements"][0]["distance"]["value"]
            duration = distance["rows"][0]["elements"][0]["duration"]["text"]
            mile = float(meter) * 0.000621371
            
            
            #  ---- Get PriceMile ---- 
            price_miles = models.PriceMile.objects.filter(is_active=True).all()
            price_mile = price_miles[0]
            
            
            #  ---- Get JoinedPrice ---- 
            joined_prices = models.JoinedPrice.objects.filter(pricemile=price_mile)
            joined_price = self.check_datetime(joined_prices, date).priceday.price
            if date_return:
                joined_price += self.check_datetime(joined_prices, date_return).priceday.price

            #  ---- Find Price Travel ---- 
            fixed_price = self.check_fixed_price(origin, destination)
            if fixed_price:
                price = fixed_price
            else:
                price = float(joined_price) * mile
            
            
            return {"meter": round(meter, 1)  , "mile": round(mile, 2)  , "duration": duration, "price": round(price, 3)  , "price_per_mile": float(joined_price)}
        except:
            return False
    # afind_distance = sync_to_async(find_distance, thread_sensitive=False)
    
        