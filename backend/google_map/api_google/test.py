import googlemaps
# from datetime import datetime

key = "TOKEN"
gmaps = googlemaps.Client(key=key)



#places = gmaps.places("srili, UK")

#places_id = [i["place_id"] for i in places["results"]]

#places_2 = [gmaps.place(i)["result"] for i in places_id]

# place = gmaps.place("ChIJJ-Afs9eofEgRe6Odhnn61XU")

distance = gmaps.distance_matrix(origins="1 Ironworks Rd, Barrow-in-Furness LA14 2PG, UK",
                                 destinations="Unit 6A Metnor Business Park, Hadrian Rd, Wallsend NE28 6HH, UK")


find_places = gmaps.places_autocomplete("abas", components={'country': ['UK']})
            
            
list_show = ["formatted_address", "name", "url", "geometry"]
find_places_2 = []
for i in find_places:
    place = gmaps.place(i["place_id"])["result"]
    find_places_2.append({j:place[j] for j in place if j in list_show})

find_places = gmaps.find_place("srili , UK", "textquery")
find_places_2 = [gmaps.place(i["place_id"])["result"] for i in find_places["candidates"]]
