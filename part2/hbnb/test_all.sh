#!/bin/bash

BASE="http://localhost:5000/api/v1"

echo "🧪 Testing ALL Endpoints"
echo "========================"

# USERS
echo -e "\n📝 USERS"
curl -X POST $BASE/users/ -H "Content-Type: application/json" -d '{"first_name":"John","last_name":"Doe","email":"john@test.com"}'
echo -e "\n❌ Invalid email:"
curl -X POST $BASE/users/ -H "Content-Type: application/json" -d '{"first_name":"Jane","last_name":"Doe","email":"invalid"}'
echo -e "\n📋 All users:"
curl $BASE/users/

# AMENITIES
echo -e "\n\n🛋️ AMENITIES"
curl -X POST $BASE/amenities/ -H "Content-Type: application/json" -d '{"name":"WiFi"}'
echo -e "\n📋 All amenities:"
curl $BASE/amenities/

# PLACES
echo -e "\n\n🏠 PLACES"
curl -X POST $BASE/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"Nice place","price":100,"latitude":48.8566,"longitude":2.3522,"owner_id":"test-id"}'
echo -e "\n📋 All places:"
curl $BASE/places/

# REVIEWS
echo -e "\n\n⭐ REVIEWS"
curl -X POST $BASE/reviews/ -H "Content-Type: application/json" -d '{"text":"Great!","rating":5,"place_id":"test-id","user_id":"test-id"}'
echo -e "\n📋 All reviews:"
curl $BASE/reviews/

echo -e "\n\n✅ Testing completed!"