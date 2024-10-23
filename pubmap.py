import folium
from folium.plugins import MarkerCluster
import pgeocode
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize pgeocode for the UK
nomi = pgeocode.Nominatim('GB')

# Define a mapping from price to color
price_color_map = {
    0: 'green',
    1: 'blue',
    2: 'orange',
    3: 'red',
    4: 'purple',
    5: 'darkred',
    # Prices above £5 will default to 'gray'
}

# Function to parse price and return the corresponding color
def get_color(price_str):
    try:
        # Extract numeric value from price string
        price = float(price_str.replace('£', '').replace(',', '').strip())
        # Determine color based on price
        # Round to nearest integer to match price_color_map keys
        price_int = int(round(price))
        return price_color_map.get(price_int, 'gray')  # Default color if price not in map
    except:
        return 'gray'  # Default color in case of parsing error

# List of pubs with their details
pubs = [
    {
        "name": "Bird In Hand",
        "location": "Dartford, London",
        "event_time": "Thu @ 20:30",
        "phone": "1322280139",
        "price": "£0.00",
        "prize": "£0",
        "postal_code": "DA1 3EY"
    },
    {
        "name": "Bridge House",
        "location": "Penge, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8778 2100",
        "price": "£3.00",
        "prize": "£300",
        "postal_code": "SE20 8RZ"
    },
    {
        "name": "Clissold Park Tavern",
        "location": "Stoke Newington, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7226 7770",
        "price": "£2.00",
        "prize": "£100",
        "postal_code": "N16 9DB"
    },
    {
        "name": "Coach and Horses",
        "location": "Clapham, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7622 3815",
        "price": "£0.00",
        "prize": "£0",
        "postal_code": "SW4 7EX"
    },
    {
        "name": "Craft Beer Co Brixton",
        "location": "Brixton, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 7274 8383",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "SW9 8PA"
    },
    {
        "name": "Cricketers",
        "location": "Enfield, London",
        "event_time": "Thu @ 21:00",
        "phone": "0208 363 5218",
        "price": "£0.00",
        "prize": "£20",
        "postal_code": "EN2 6NP"
    },
    {
        "name": "Famous Royal Oak",
        "location": "Muswell Hill, London",
        "event_time": "Thu @ 21:00",
        "phone": "020 8444 2504",
        "price": "£1.00",
        "prize": "£15",
        "postal_code": "N10 3QY"
    },
    {
        "name": "Gosnells Of London",
        "location": "Bermondsey, London",
        "event_time": "Thu @ 19:00",
        "phone": "",
        "price": "£0.00",
        "prize": "£100",
        "postal_code": "SE16 3RA"
    },
    {
        "name": "Hop Poles",
        "location": "Hammersmith, London",
        "event_time": "Thu @ 19:00",
        "phone": "020 8748 1411",
        "price": "£2.00",
        "prize": "£30",
        "postal_code": "W6 9HR"
    },
    {
        "name": "Italian Job",
        "location": "Notting Hill, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7229 5963",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "W11 1HE"
    },
    {
        "name": "Kings Arms",
        "location": "Chelsea, London",
        "event_time": "Thu @ 20:00",
        "phone": "2073515043",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "SW10 9PN"
    },
    {
        "name": "LDN Craft",
        "location": "Angel, London",
        "event_time": "Thu @ 19:00",
        "phone": "7521610863",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "N1 0PS"
    },
    {
        "name": "Lord Raglan",
        "location": "Walthamstow, London",
        "event_time": "Thu @ 19:30",
        "phone": "0208 520 8483",
        "price": "£2.00",
        "prize": "£40",
        "postal_code": "E17 9HX"
    },
    {
        "name": "Lucky Voice Islington",
        "location": "Angel, London",
        "event_time": "Thu @ 19:00",
        "phone": "020 7354 6280",
        "price": "£3.00",
        "prize": "£50",
        "postal_code": "N1 1RG"
    },
    {
        "name": "Mondo Tap House",
        "location": "Battersea, London",
        "event_time": "Thu @ 19:00",
        "phone": "020 7720 0782",
        "price": "£2.00",
        "prize": "£30",
        "postal_code": "SW8 4UG"
    },
    {
        "name": "Pitcher and Piano Richmond",
        "location": "Richmond, London",
        "event_time": "Thu @ 19:30",
        "phone": "",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "TW9 1TQ"
    },
    {
        "name": "Railway Telegraph",
        "location": "Forest Hill, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 6995 0331",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "SE23 1BS"
    },
    {
        "name": "Roxy Bar and Screen",
        "location": "Borough, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 7407 4057",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "SE1 1LB"
    },
    {
        "name": "Royal Inn On The Park",
        "location": "Hackney, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 8985 3321",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "E9 7HJ"
    },
    {
        "name": "Shillibeer's Bar and Grill",
        "location": "Islington, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 3218 0083",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "N7 9EF"
    },
    {
        "name": "Sir Colin Campbell Music Quiz",
        "location": "Kilburn, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7693 5443",
        "price": "£2.00",
        "prize": "£40",
        "postal_code": "NW6 2BY"
    },
    {
        "name": "Stapleton Tavern",
        "location": "Crouch Hill, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7272 5395",
        "price": "£1.00",
        "prize": "£50",
        "postal_code": "N4 4AU"
    },
    {
        "name": "The Acorn",
        "location": "Barking, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 3673 2462",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "IG11 8UF"
    },
    {
        "name": "The Angel and Crown",
        "location": "Richmond, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 8940 1508",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "TW9 1JL"
    },
    {
        "name": "The Beaconsfield",
        "location": "Manor House, London",
        "event_time": "Thu @ 21:00",
        "phone": "020 8826 5200",
        "price": "£0.00",
        "prize": "£0",
        "postal_code": "N4 1DZ"
    },
    {
        "name": "The Berrylands",
        "location": "Surbiton, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8399 4043",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "KT5 8LS"
    },
    {
        "name": "The Brockley Jack",
        "location": "Brockley, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8699 3966",
        "price": "£1.00",
        "prize": "£50",
        "postal_code": "SE4 2DH"
    },
    {
        "name": "The Castle Portobello",
        "location": "Ladbroke Grove, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 7221 7103",
        "price": "£0.00",
        "prize": "£0",
        "postal_code": "W11 1LU"
    },
    {
        "name": "The Catcher In The Rye",
        "location": "Finchley, London",
        "event_time": "Thu @ 20:00",
        "phone": "2083434369",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "N3 1DP"
    },
    {
        "name": "The Copper Kettle",
        "location": "Surbiton, London",
        "event_time": "Thu @ 20:00",
        "phone": "",
        "price": "£1.00",
        "prize": "£0",
        "postal_code": "KT6 5LX"
    },
    {
        "name": "The Crown",
        "location": "Hackney, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7403 0123",
        "price": "£3.00",
        "prize": "£50",
        "postal_code": "E8 1HP"
    },
    {
        "name": "The Crown and Anchor",
        "location": "Chiswick, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8742 7466",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "W4 5TA"
    },
    {
        "name": "The Duchess",
        "location": "Hammersmith, London",
        "event_time": "Thu @ 19:30",
        "phone": "2087489128",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "W6 0XF"
    },
    {
        "name": "The Duke Of York",
        "location": "Marylebone, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 72587418",
        "price": "£1.00",
        "prize": "£50",
        "postal_code": "W1H 5HT"
    },
    {
        "name": "The Golden Hinde",
        "location": "Pickfords Wharf, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7403 0123",
        "price": "£3.00",
        "prize": "£0",
        "postal_code": "SE1 9DG"
    },
    {
        "name": "The Gunnersbury",
        "location": "Chiswick, London",
        "event_time": "Thu @ 18:30",
        "phone": "020 8742 7466",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "W4 5RP"
    },
    {
        "name": "The Hanbury Arms",
        "location": "Islington, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7288 2222",
        "price": "£1.00",
        "prize": "£50",
        "postal_code": "N1 7DU"
    },
    {
        "name": "The Hercules",
        "location": "Holloway Road, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7281 6663",
        "price": "£2.00",
        "prize": "£250",
        "postal_code": "N7 6JA"
    },
    {
        "name": "The Holly Tree",
        "location": "Forest Gate, London",
        "event_time": "Thu @ 21:00",
        "phone": "020 8221 9830",
        "price": "£0.00",
        "prize": "£0",
        "postal_code": "E7 0DZ"
    },
    {
        "name": "The Leconfield Pub",
        "location": "Stoke Newington, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7354 2791",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "N16 9BU"
    },
    {
        "name": "The Old Nun's Head",
        "location": "Nunhead, London",
        "event_time": "Thu @ 20:15",
        "phone": "020 7639 4007",
        "price": "£2.00",
        "prize": "£100",
        "postal_code": "SE15 3QQ"
    },
    {
        "name": "The Orchard",
        "location": "Shepherds Bush, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8746 7800",
        "price": "£3.00",
        "prize": "£100",
        "postal_code": "W12 9BP"
    },
    {
        "name": "The Pembroke",
        "location": "Primrose Hill, London",
        "event_time": "Thu @ 20:00",
        "phone": "0207 4832 927",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "NW1 8JA"
    },
    {
        "name": "The Pembroke",
        "location": "Earls Court, London",
        "event_time": "Thu @ 19:00",
        "phone": "020 7373 8337",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "SW5 9JA"
    },
    {
        "name": "The Plough",
        "location": "East Dulwich, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 8693 4236",
        "price": "£2.00",
        "prize": "£60",
        "postal_code": "SE22 8JJ"
    },
    {
        "name": "The Poet",
        "location": "Islington, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7226 2900",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "N1 3DS"
    },
    {
        "name": "The Prince N16",
        "location": "Stoke Newington, London",
        "event_time": "Thu @ 20:00",
        "phone": "0207 043 5210",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "N16 0EB"
    },
    {
        "name": "The Prince of Wales",
        "location": "Battersea, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7228 0395",
        "price": "£1.00",
        "prize": "£20",
        "postal_code": "SW11 3AE"
    },
    {
        "name": "The Red Lion",
        "location": "Isleworth, London",
        "event_time": "Thu @ 19:45",
        "phone": "020 8560 1457",
        "price": "£3.00",
        "prize": "£350",
        "postal_code": "TW7 6QJ"
    },
    {
        "name": "The Regent",
        "location": "Islington, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 7700 2725",
        "price": "£2.00",
        "prize": "£0",
        "postal_code": "N1 1LX"
    },
    {
        "name": "The Waverley Arms",
        "location": "Nunhead, London",
        "event_time": "Thu @ 20:00",
        "phone": "0207 450 1139",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "SE15 3BU"
    },
    {
        "name": "The Westbury",
        "location": "Wood Green, London",
        "event_time": "Thu @ 21:00",
        "phone": "020 8881 1661",
        "price": "£1.00",
        "prize": "£0",
        "postal_code": "N22 6SA"
    },
    {
        "name": "The White Ferry House",
        "location": "Pimlico, London",
        "event_time": "Thu @ 19:00",
        "phone": "020 7233 6133",
        "price": "£1.00",
        "prize": "£30",
        "postal_code": "SW1V 4LD"
    },
    {
        "name": "The White Horse",
        "location": "Harrow on the Hill, London",
        "event_time": "Thu @ 21:00",
        "phone": "020 8422 1215",
        "price": "£1.00",
        "prize": "£0",
        "postal_code": "HA2 0HL"
    },
    {
        "name": "The World's End",
        "location": "Finsbury Park, London",
        "event_time": "Thu @ 19:30",
        "phone": "020 7281 8679",
        "price": "£2.00",
        "prize": "£50",
        "postal_code": "N4 3EF"
    },
    {
        "name": "Whelans Croydon",
        "location": "Croydon, London",
        "event_time": "Thu @ 20:00",
        "phone": "",
        "price": "£2.50",
        "prize": "£50",
        "postal_code": "CR2 6PW"
    },
    {
        "name": "White Hart Brew Pub",
        "location": "Whitechapel, London",
        "event_time": "Thu @ 21:00",
        "phone": "2077902894",
        "price": "£1.00",
        "prize": "£40",
        "postal_code": "E1 4TP"
    },
    {
        "name": "Woody's",
        "location": "Kingston, London",
        "event_time": "Thu @ 20:00",
        "phone": "020 8541 4984",
        "price": "£1.00",
        "prize": "£100",
        "postal_code": "KT1 1HH"
    },
]

# Function to get coordinates using pgeocode
def get_coordinates(postal_code):
    try:
        # Clean the postal code to ensure proper formatting
        postal_code = postal_code.strip().upper()
        location = nomi.query_postal_code(postal_code)
        if not location.empty and not (location.latitude != location.latitude):  # Check for NaN
            latitude = location.latitude
            longitude = location.longitude
            logging.info(f"Coordinates for {postal_code}: ({latitude}, {longitude})")
            return (latitude, longitude)
        else:
            logging.warning(f"Could not find coordinates for postal code: {postal_code}")
            return (None, None)
    except Exception as e:
        logging.error(f"Error getting coordinates for {postal_code}: {e}")
        return (None, None)

# Get coordinates for all pubs
for pub in pubs:
    lat, lon = get_coordinates(pub["postal_code"])
    pub["latitude"] = lat
    pub["longitude"] = lon

# Create a folium map centered around London
london_coordinates = [51.5074, -0.1278]
m = folium.Map(location=london_coordinates, zoom_start=11)

# Initialize MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map with colored icons
for pub in pubs:
    if pub["latitude"] and pub["longitude"]:
        # Determine marker color based on price
        color = get_color(pub["price"])
        
        # Create HTML content for the popup
        popup_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h4>{pub['name']}</h4>
            <b>Location:</b> {pub['location']}<br>
            <b>Event Time:</b> {pub['event_time']}<br>
            <b>Phone:</b> {pub['phone'] if pub['phone'] else 'N/A'}<br>
            <b>Price:</b> {pub['price']}<br>
            <b>Prize:</b> {pub['prize']}<br>
            <b>Postal Code:</b> {pub['postal_code']}
        </div>
        """
        folium.Marker(
            location=[pub["latitude"], pub["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=color, icon='beer')
        ).add_to(marker_cluster)
    else:
        logging.warning(f"Skipping {pub['name']} due to missing coordinates.")

# Define the legend HTML
legend_html = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 220px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     padding: 10px;
     ">
     &nbsp;<b>Price Legend</b><br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:green"></i>&nbsp;£0<br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:blue"></i>&nbsp;£1<br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:orange"></i>&nbsp;£2<br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:red"></i>&nbsp;£3<br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:purple"></i>&nbsp;£4<br>
     &nbsp;<i class="fa fa-beer fa-2x" style="color:darkred"></i>&nbsp;£5+<br>
     </div>
     '''

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
map_filename = "london_pubs_map.html"
m.save(map_filename)
logging.info(f"Map has been saved to {map_filename}")
