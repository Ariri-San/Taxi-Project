import googlemaps
# from datetime import datetime

key = "AIzaSyDEnymewL5xuqEqp3baWmzXley4_iUdYdk"
gmaps = googlemaps.Client(key=key)



places = gmaps.places("sriling", region="UK")

places_id = [i["place_id"] for i in places["results"]]

places_2 = [gmaps.place(i)["result"] for i in places_id]

# place = gmaps.place("ChIJJ-Afs9eofEgRe6Odhnn61XU")

distance = gmaps.distance_matrix(origins="1 Ironworks Rd, Barrow-in-Furness LA14 2PG, UK",
                                 destinations="Unit 6A Metnor Business Park, Hadrian Rd, Wallsend NE28 6HH, UK",
                                 region="UK")

