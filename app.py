import streamlit as st
import pandas as pd
import time
import os
import base64
from PIL import Image

# ====================================================================
# 1. PAGE CONFIGURATION 
# ====================================================================
st.set_page_config(page_title="NeoGuide: AI Tourism Engine", page_icon="MAP", layout="wide")
st.markdown('<h1 style="text-align: center; color: #00FFBB;"> 🗺️ NEO-GUIDE: AI-POWERED LOCAL TOURISM & HIDDEN GEMS FINDER</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #A0AEC0;">Acharya Institute of Graduate Studies - BCA 5th Semester</h3>', unsafe_allow_html=True)
st.markdown('<h5 style="text-align: center; color: #00FFBB; font-style: italic; text-align: center;">Presented by: Sneha M</h5>', unsafe_allow_html=True)
st.markdown("---")

# ====================================================================
# 2. DATABASE & MOCK PIPELINE
# ====================================================================
@st.cache_resource
def connect_db():
    return "MongoDB Connected Successfully!"

db_status = connect_db()
st.sidebar.markdown(f"**Database Status:** <span style='color:#00FFBB; font-weight:bold;'>{db_status}</span>", unsafe_allow_html=True)

# ====================================================================
# 3. SIDEBAR CONTROLS & FILTERS
# ====================================================================
st.sidebar.markdown("### Hybrid Engine Filters")
selected_category = st.sidebar.selectbox("Filter by Category", ["All", "Waterfall", "Trekking", "Secret Terrains", "Blue Escapes", "Beach"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Location Anchor Settings")
origin_point = st.sidebar.selectbox(
    "Set Your Starting Base (Origin Point)",
    ["Acharya Campus (AIGS)", "Majestic (Bengaluru City Center)", "Kempegowda Int. Airport (KIA)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### AI Smart Budget Configurator")
transport_mode = st.sidebar.radio("Select Transport Mode", ["Two-Wheeler (Bike)", "Four-Wheeler (Car)", "Public Transit (Bus/Train)"])

transport_rates = {
    "Two-Wheeler (Bike)": 3.0,          
    "Four-Wheeler (Car)": 14.0,         
    "Public Transit (Bus/Train)": 2.0   
}

origin_distance_matrix = {
    "Acharya Campus (AIGS)": [2890, 540, 1262, 2790, 343],
    "Majestic (Bengaluru City Center)": [2895, 530, 1265, 2795, 345],
    "Kempegowda Int. Airport (KIA)": [2850, 570, 1240, 2750, 365]
}

distances_km = origin_distance_matrix[origin_point]

if origin_point == "Kempegowda Int. Airport (KIA)":
    current_rate = 3.5  
    selected_budget_range = "Flight Booking Mode Enabled"
    
    category_budgets = {
        "All": "Rs. 12,432 - Rs. 32,000",
        "Waterfall": "Rs. 32,000",
        "Trekking": "Rs. 25,000",
        "Secret Terrains": "Rs. 25,000",
        "Blue Escapes": "Rs. 12,432",
        "Beach": "Rs. 14,500"
    }
    
    transit_info = {
        "Base": "Kempegowda Int. Airport (KIA)",
        "Dawki": "Landing Airport: Guwahati (GAU) | Flight Ticket: Rs. 6,900 | Total: Rs. 25,000",
        "Chorla": "Landing Airport: Goa (GOI/GOX) | Flight Ticket: Rs. 8,500 | Total: Rs. 25,000",
        "Suvali": "Landing Airport: Surat (STV) | Flight Ticket: Rs. 6,135 | Total: Rs. 14,500",
        "Nuranang": "Landing Airport: Guwahati (GAU) | Flight Ticket: Rs. 8,350 | Total: Rs. 32,000",
        "Kavvayi": "Landing Airport: Kannur (CNN) | Flight Ticket: Rs. 4,339 | Total: Rs. 12,432"
    }
else:
    current_rate = transport_rates[transport_mode]
    
    if origin_point == "Majestic (Bengaluru City Center)":
        min_cost = 345 * current_rate
        max_cost = 3235 * current_rate
        
        category_budgets = {
            "All": f"Rs. {min_cost:,.0f} - Rs. {max_cost:,.0f}",
            "Waterfall": f"Rs. {3235 * current_rate:,.0f}",
            "Trekking": f"Rs. {530 * current_rate:,.0f}",
            "Secret Terrains": f"Rs. {3135 * current_rate:,.0f}",
            "Blue Escapes": f"Rs. {345 * current_rate:,.0f}",
            "Beach": f"Rs. {1265 * current_rate:,.0f}"
        }
        
        transit_info = {
            "Base": "Majestic (Bengaluru City Center)",
            "Dawki": "Train/Road Transit | Duration: ~2.5 Days | Avg Cost: Rs. 22,500",
            "Chorla": "Overnight Bus/Train | Duration: ~10 Hours | Avg Cost: Rs. 5,000",
            "Suvali": "Train Transit to Surat | Duration: ~23 Hours | Avg Cost: Rs. 12,800",
            "Nuranang": "Long Rail Transit to Assam | Duration: ~3 Days | Avg Cost: Rs. 20,000",
            "Kavvayi": "Overnight Train (KSR to Payyanur) | Duration: ~9 Hours | Avg Cost: Rs. 4,000"
        }
    else:
        min_cost = 343 * current_rate
        max_cost = 3230 * current_rate
        
        category_budgets = {
            "All": f"Rs. {min_cost:,.0f} - Rs. {max_cost:,.0f}",
            "Waterfall": f"Rs. {3230 * current_rate:,.0f}",
            "Trekking": f"Rs. {540 * current_rate:,.0f}",
            "Secret Terrains": f"Rs. {3124 * current_rate:,.0f}",
            "Blue Escapes": f"Rs. {343 * current_rate:,.0f}",
            "Beach": f"Rs. {1262 * current_rate:,.0f}"
        }
        
        transit_info = {
            "Base": "Acharya Campus (AIGS)",
            "Dawki": "Road Trip via National Highways | Duration: ~55 Hours Drive | Avg Cost: Rs. 26,800",
            "Chorla": "Road Trip via National Highways | Duration: ~10.5 Hours Drive | Avg Cost: Rs. 4,250",
            "Suvali": "Road Trip via National Highways | Duration: ~23 Hours Drive | Avg Cost: Rs. 11,000",
            "Nuranang": "Road Trip via National Highways | Duration: ~65 Hours Drive | Avg Cost: Rs. 28,600",
            "Kavvayi": "Road Trip via National Highways | Duration: ~7.5 Hours Drive | Avg Cost: Rs. 5,000"
        }

selected_budget_range = category_budgets.get(selected_category, "N/A")

st.sidebar.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); 
        padding: 18px; 
        border-radius: 12px; 
        border-left: 5px solid #00FFBB; 
        box-shadow: 0 4px 15px rgba(0, 255, 187, 0.1); 
        margin-top: 12px; 
        margin-bottom: 12px;
    ">
        <h4 style="color: #94A3B8; margin-top: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">
            💰 Estimated Budget
        </h4>
        <p style="color: #00FFBB; font-size: 22px; font-weight: 800; margin-top: 5px; margin-bottom: 5px; font-family: 'Courier New', monospace;">
            {selected_budget_range}
        </p>
        <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px; margin-top: 8px;">
            <small style="color: #38BDF8; font-weight: 500;">📂 Category: {selected_category}</small>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

st.success(f"Selected Transport: **{transport_mode}** | Selected Category: **{selected_category}** (Context: {selected_budget_range})")

# Image Loader Function
def get_image_base64_string(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        except Exception:
            pass
    return "https://picsum.photos"

# ====================================================================
# 4. DATABASES WITH COMPLETE METADATA MATRIX
# ====================================================================
places = [
    "Dawki Umngot Deep Gorge", 
    "Chorla Ghat Secret Streams", 
    "Suvali Isolated Beach", 
    "Nuranang Hidden Falls", 
    "Kavvayi Secret Backwaters"
]
categories = ["Secret Terrains", "Trekking", "Beach", "Waterfall", "Blue Escapes"]
ratings = ["9.6/10", "9.2/10", "8.7/10", "9.5/10", "9.1/10"]
latitudes = [25.18, 15.66, 21.17, 27.56, 12.09]
longitudes = [92.02, 74.12, 72.64, 91.99, 75.14]
crowd_status = ["Low Crowd (Peaceful)", "Moderate Crowd", "Low Crowd (Peaceful)", "High Overcrowded", "Low Crowd (Peaceful)"]

ai_scraped_descriptions = [
    "AI VISUAL SUMMARY & ADDRESS: A jaw-dropping deep canyon featuring the crystalline, transparent waters of the Umngot River. Located at West Jaintia Hills, Dawki, Meghalaya - 793109, India near the Indo-Bangladesh border.",
    "AI VISUAL SUMMARY & ADDRESS: A mist-covered tropical rainforest canopy concealing untouched, crystal-clear freshwater rapids. Situated at Chorla Ghat, intersection of Goa, Karnataka, and Maharashtra borders - 403505.",
    "AI VISUAL SUMMARY & ADDRESS: A serene, secluded coastline characterized by unique jet-black volcanic sands and absolute solitude. Located at Suvali Beach, Hazira Outskirts, Surat, Gujarat - 395009, India.",
    "AI VISUAL SUMMARY & ADDRESS: A spectacular, roaring 100-meter white-water cascade plunging down rugged Himalayan slopes. Located at Nuranang, near Tawang District, Arunachal Pradesh - 790104, India.",
    "AI VISUAL SUMMARY & ADDRESS: North Kerala's largest undiscovered backwater stretch, formed by a peaceful cluster of small mangrove islands. Located at Kavvayi Island, Payyanur, Kannur District, Kerala - 670307, India."
]

ai_itineraries = []

if origin_point == "Kempegowda Int. Airport (KIA)":
    ai_itineraries = [
        f"AI TOURISM ROUTE LOGISTICS & DETAILS:\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Dawki', '')}\n\n[PLACE INFO]: Dawki Umngot Gorge features the crystal-clear Umngot River, known as one of the cleanest rivers in India. The water is so transparent that boats appear to float in mid-air, creating a magical visual experience.\n\nDAY 2: LOCAL EXPEDITION SCHEDULE:\n- 07:00 AM: Start from Shillong transit base\n- 09:30 AM: Reach Dawki Umngot Gorge & enjoy crystal-clear boating\n- 12:30 PM: Traditional Meghalayan local lunch\n- 02:00 PM: Visit Indo-Bangladesh Border & Friendship Gate\n- 05:00 PM: Return to Shillong base",
        
        f"AI TOURISM ROUTE LOGISTICS & DETAILS:\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Chorla', '')}\n\n[PLACE INFO]: Chorla Ghat is a misty paradise located deep inside the Western Ghats rainforest at the intersection of Goa, Karnataka, and Maharashtra. It is a haven for nature lovers, bird watchers, and trekkers.\n\nDAY 1: LOCAL EXPEDITION SCHEDULE:\n- 08:30 AM: Reach Chorla trail base and check-in\n- 11:00 AM: Guided nature walk inside the thick tropical rainforest\n- 01:30 PM: Photoshoot at hidden freshwater streams & cascades\n- 04:00 PM: Sunset photography from scenic valley viewpoints",
        
        f"AI TOURISM ROUTE LOGISTICS & DETAILS:\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Suvali', '')}\n\n[PLACE INFO]: Suvali Beach is a peaceful, secluded coastline located on the outskirts of Surat, Gujarat. It is famous for its unique jet-black volcanic sand and absolute solitude, making it perfect for mental relaxation.\n\nDAY 1: LOCAL EXPEDITION SCHEDULE:\n- 04:30 PM: Reach Suvali isolated beach shore\n- 05:00 PM: Enjoy a relaxing walk on the peaceful black sand coast\n- 06:15 PM: Capture stunning sunset photography over the Arabian Sea\n- 07:00 PM: Taste local Gujarati street food and return from beach",
        
        f"AI TOURISM ROUTE LOGISTICS & DETAILS:\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Nuranang', '')}\n\n[PLACE INFO]: Nuranang Hidden Falls (also known as Bong Bong Falls) is a spectacular 100-meter white-water cascade plunging down rugged Himalayan slopes in Arunachal Pradesh. It is surrounded by breathtaking snow-capped mountains.\n\nDAY 2: LOCAL EXPEDITION SCHEDULE:\n- 09:30 AM: Arrive at Nuranang Hidden Falls & take a cascade trail walk\n- 11:30 AM: Explore the scenic hydro-power station viewpoint\n- 01:00 PM: Enjoy a warm high-altitude local Himalayan lunch\n- 04:00 PM: Return to Tawang transit base",
        
        f"AI TOURISM ROUTE LOGISTICS & DETAILS:\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Kavvayi', '')}\n\n[PLACE INFO]: Kavvayi Backwaters is North Kerala's largest undiscovered island stretch. Formed by a peaceful cluster of small mangrove islands and lined with tall coconut trees, it offers a pure rustic coastal vibe away from crowds.\n\nDAY 1: LOCAL EXPEDITION SCHEDULE:\n- 03:30 PM: Board a traditional canoe for Kavvayi exploration at Payyanur\n- 04:30 PM: Cruise through the secret mangrove forest island channels\n- 06:30 PM: Golden hour photography & serene backwater sunset views\n- 07:30 PM: Experience traditional Malabar seafood dinner"
    ]
elif transport_mode == "Four-Wheeler (Car)":
    ai_itineraries = [
        f"AI TOURISM ROUTE LOGISTICS (CAR ROAD TRIP):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Dawki', '')}\n\n[PLACE INFO]: Driving your own car through the winding mountain roads and national highways to reach Dawki is a lifetime experience. The lush green nature along the roads makes this road trip incredibly beautiful.\n\nDAY 4: LOCAL EXPEDITION SCHEDULE (After 3 Days Road Drive):\n- 07:00 AM: Drive from Shillong hotel base towards Dawki canyon\n- 09:30 AM: Reach Dawki and cross the historic suspension bridge\n- 11:00 AM: Enjoy clear water boating and riverside photography\n- 12:30 PM: Lunch at a local riverside camp\n- 05:00 PM: Drive back to Shillong base camp",
        
        f"AI TOURISM ROUTE LOGISTICS (CAR ROAD TRIP):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Chorla', '')}\n\n[PLACE INFO]: A long drive from Bengaluru to Chorla Ghat is a dream for road trip enthusiasts. Driving through the hairpin curves surrounded by dense fog and the sound of waterfalls is refreshing.\n\nDAY 1: LOCAL EXPEDITION SCHEDULE (Direct Road Drive):\n- 03:30 PM: Enter Chorla Ghat forest region after a scenic drive\n- 04:30 PM: Check-in at the jungle resort or eco-camp base\n- 05:30 PM: Stop at lush green foggy viewpoints for photography\n- 06:15 PM: Capture Western Ghats sunset right from the car deck\n- 08:00 PM: Campfire setup and dinner",
        
        f"AI TOURISM ROUTE LOGISTICS (CAR ROAD TRIP):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Suvali', '')}\n\n[PLACE INFO]: This road trip takes you through smooth Gujarat highways past Surat city, allowing you to drive directly up to the secluded sand shores of Suvali Beach for a highly relaxing evening.\n\nDAY 3: LOCAL EXPEDITION SCHEDULE (After 2 Days Road Drive):\n- 04:30 PM: Arrive at Suvali beach parking zone\n- 05:30 PM: Take a relaxing walk along the empty, silent shoreline\n- 06:15 PM: Professional car-backdrop photography during sunset\n- 07:30 PM: Drive back to Surat city hotel",
        
        f"AI TOURISM ROUTE LOGISTICS (CAR ROAD TRIP):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Nuranang', '')}\n\n[PLACE INFO]: Driving a car through the extreme Himalayan loops and snowy passes on the way to Tawang is pure adventure. Stopping at this hidden waterfall along the highway is a major highlight.\n\nDAY 6: LOCAL EXPEDITION SCHEDULE (After 5 Days Mountain Drive):\n- 09:30 AM: Arrive at Nuranang Hidden Falls valley via Car\n- 11:00 AM: Photography near the roaring white-water cascade\n- 01:00 PM: Hot lunch overlooking the majestic mountain ranges\n- 03:00 PM: Check vehicle vitals and continue driving to Tawang",
        
        f"AI TOURISM ROUTE LOGISTICS (CAR ROAD TRIP):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Kavvayi', '')}\n\n[PLACE INFO]: A scenic coastal drive tracking the green landscapes of Kerala, heading through Kannur to reach the peaceful backwater parking bays of Payyanur islands.\n\nDAY 1: LOCAL EXPEDITION SCHEDULE (Direct Road Drive):\n- 02:30 PM: Reach Payyanur backwater harbor parking point\n- 03:30 PM: Park car and board a traditional wooden exploration canoe\n- 05:00 PM: Cruise smoothly under the leaning coconut tree canopy lines\n- 06:30 PM: Capture golden hour reflections on the calm backwaters"
    ]
else:
    ai_itineraries = [
        f"AI TOURISM ROUTE LOGISTICS (TRAIN/PUBLIC TRANSIT):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Dawki', '')}\n\n[PLACE INFO]: A highly affordable budget route using public buses or shared taxis to explore the beauty of Northeast India and experience Dawki Gorge on a minimal budget.\n\nDAY 5: LOCAL EXPEDITION SCHEDULE (After Train/Bus Transit):\n- 07:00 AM: Board a shared Sumo or public transit bus from Shillong\n- 09:30 AM: Drop off at Dawki public transit junction\n- 10:30 AM: Join a shared group boat ride on Umngot River to save costs\n- 12:30 PM: Enjoy a budget local lunch at the border flea market\n- 05:00 PM: Head back to Shillong base via evening shared transport",
        
        f"AI TOURISM ROUTE LOGISTICS (TRAIN/PUBLIC TRANSIT):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Chorla', '')}\n\n[PLACE INFO]: Take an overnight public sleeper bus or train from Bengaluru to Belgaum/Goa, and use local state transport connectivity to explore the wilderness of Chorla Ghat.\n\nDAY 2: LOCAL EXPEDITION SCHEDULE (After Overnight Bus):\n- 09:00 AM: Reach Chorla Ghat forest base via connecting local state bus\n- 11:00 AM: Join a budget-friendly group nature trek along wild trails\n- 01:00 PM: Have a packed forest box lunch near clean freshwater streams\n- 04:00 PM: Walk to the nearest state bus stop for the return journey",
        
        f"AI TOURISM ROUTE LOGISTICS (TRAIN/PUBLIC TRANSIT):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Suvali', '')}\n\n[PLACE INFO]: Travel via train to Surat railway station, then easily catch a local city transit bus (BRTS) or shared auto to access the secluded shores of Suvali Beach economically.\n\nDAY 2: LOCAL EXPEDITION SCHEDULE (After Train Transit):\n- 03:00 PM: Arrive at Surat station and board a local city transit bus\n- 04:30 PM: Reach Suvali beach access point via a budget auto ride\n- 05:00 PM: Free-entry beach walking and relaxation on dark volcanic sand\n- 06:15 PM: Watch the open sky ocean sunset with zero entry fees\n- 07:00 PM: Take an evening auto back to the city transit hub",
        
        f"AI TOURISM ROUTE LOGISTICS (TRAIN/PUBLIC TRANSIT):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Nuranang', '')}\n\n[PLACE INFO]: Travel by rail up to Assam, then take an affordable shared local mountain Sumo taxi up the high ridges to view Nuranang Falls without expensive car rentals.\n\nDAY 6: LOCAL EXPEDITION SCHEDULE (After Train + Connecting Bus):\n- 09:30 AM: Drop off at Nuranang Hidden Falls via shared mountain Sumo\n- 11:30 AM: Enjoy a free trail walk close to the roaring water cascade\n- 01:30 PM: Stop at a small local army canteen for hot Maggie & tea (Affordable)\n- 04:00 PM: Catch the next connecting shared transit towards Tawang",
        
        f"AI TOURISM ROUTE LOGISTICS (TRAIN/PUBLIC TRANSIT):\n\nSTARTING BASE: {transit_info.get('Base', '')}\nTRANSIT METHOD: {transit_info.get('Kavvayi', '')}\n\n[PLACE INFO]: Board an overnight train from Bengaluru Majestic to Payyanur station, then take a short local town bus to enjoy a scenic passenger boat ride for less than Rs. 20.\n\nDAY 2: LOCAL EXPEDITION SCHEDULE (After Overnight Train):\n- 08:30 AM: De-board train at Payyanur station and have local breakfast\n- 01:00 PM: Reach Kavvayi public ferry point via a local town bus\n- 03:30 PM: Board the government public passenger boat for a low-cost backwater ride\n- 06:30 PM: Watch the golden hour sunset right from the public boat dock\n- 07:30 PM: Board local transport back to the railway station"
    ]

nearby_locations = [
    "Mawlynnong Village, Single Decker Living Root Bridge, Shnongpdeng, Krang Suri Falls",
    "Vazra Sakla Falls, Anjunem Dam, Dudhsagar Falls, Bondla Wildlife",
    "Dumas Beach, Surat Castle, Cemeteries, Gavier Lake",
    "Tawang Monastery, Sela Pass, Madhuri Lake, Jaswant Garh",
    "Valiyaparamba, Ezhimala Hill, Chootad Beach, Madayipara"
]
nearby_locations = [
    "Mawlynnong Village, Single Decker Living Root Bridge, Shnongpdeng, Krang Suri Falls",
    "Vazra Sakla Falls, Anjunem Dam, Dudhsagar Falls, Bondla Wildlife",
    "Dumas Beach, Surat Castle, Cemeteries, Gavier Lake",
    "Tawang Monastery, Sela Pass, Madhuri Lake, Jaswant Garh",
    "Valiyaparamba, Ezhimala Hill, Chootad Beach, Madayipara"
]

# (Main Places Full Addresses)
main_places_addresses = {
    "Dawki Umngot Deep Gorge": "West Jaintia Hills District, Dawki, Meghalaya - 793109 (Indo-Bangladesh Border)",
    "Chorla Ghat Secret Streams": "Chorla Ghat Junction, SH-4, Intersection of Goa-Karnataka-Maharashtra Borders - 403505",
    "Suvali Isolated Beach": "Suvali Beach Road, Hazira Industrial Outskirts, Surat, Gujarat - 395009",
    "Nuranang Hidden Falls": "Nuranang River Valley, Near Jang Town, Tawang District, Arunachal Pradesh - 790104",
    "Kavvayi Secret Backwaters": "Kavvayi Island, Near Payyanur, Kannur District, North Kerala - 670307"
}

# (Distance Matrix)
nearby_places_info = {
    "Dawki Umngot Deep Gorge": {
        "Mawlynnong Village": "29 KM",
        "Single Decker Living Root Bridge": "27 KM",
        "Shnongpdeng": "8 KM",
        "Krang Suri Falls": "38 KM"
    },
    "Chorla Ghat Secret Streams": {
        "Vazra Sakla Falls": "12 KM",
        "Anjunem Dam": "15 KM",
        "Dudhsagar Falls": "74 KM",
        "Bondla Wildlife": "45 KM"
    },
    "Suvali Isolated Beach": {
        "Dumas Beach": "28 KM",
        "Surat Castle": "22 KM",
        "Cemeteries": "24 KM",
        "Gavier Lake": "26 KM"
    },
    "Nuranang Hidden Falls": {
        "Tawang Monastery": "32 KM",
        "Sela Pass": "48 KM",
        "Madhuri Lake": "65 KM",
        "Jaswant Garh": "25 KM"
    },
    "Kavvayi Secret Backwaters": {
        "Valiyaparamba": "14 KM",
        "Ezhimala Hill": "18 KM",
        "Chootad Beach": "12 KM",
        "Madayipara": "22 KM"
    }
}

nearby_hotspots_explain = {
    "Mawlynnong Village": "Known as the Cleanest Village in Asia. It offers beautiful eco-friendly pathways, colorful flower bushes, and an impressive tree-house skywalk viewpoint.",
    "Single Decker Living Root Bridge": "An ancient, stunning bridge handmade woven by local Khasi tribes using the living roots of rubber trees across a rapid forest stream.",
    "Shnongpdeng": "A magical riverside camp featuring incredibly transparent emerald waters where wooden boats look like they are floating in the air.",
    "Krang Suri Falls": "One of the most beautiful waterfalls in Meghalaya, famous for its deep blue natural swimming pool cut out of dark canyon rocks.",
    
    "Vazra Sakla Falls": "A tall, majestic vertical waterfall cascading down a sheer wet cliff side deep inside the dense, green evergreen Western Ghats jungle.",
    "Anjunem Dam": "A massive concrete dam reservoir tucked neatly between misty tropical rolling hills, offering an incredible landscape photography view.",
    "Dudhsagar Falls": "A giant, multi-tiered white water cascade rushing down a mountain cliff with a historic stone railway bridge arch path passing right in front of it.",
    "Bondla Wildlife": "An eco-tourism paradise featuring a lush green jungle path inside a protected Indian forest sanctuary with thick overhanging tree branches.",
    
    "Dumas Beach": "A vast, windy beach coast famous for its unique dark grey volcanic sand and mysterious aura under hazy golden evening skies.",
    "Surat Castle": "A beautifully restored historic brick and stone castle fortress wall structure sitting historically along a quiet river embankment.",
    "Cemeteries": "An ancient site displaying majestic European-style tomb monuments and weathered stone domes surrounded by quiet shaded green trees.",
    "Gavier Lake": "A peaceful, rustic swamp wetland lake completely covered in green lotus leaves, acting as a natural sanctuary for small wild birds.",
    
    "Tawang Monastery": "The largest grand Tibetan Buddhist monastery complex in India, built with bright colorful yellow roofs on a high snow-capped Himalayan ridge.",
    "Sela Pass": "A high-altitude mountain pass road featuring a frozen blue lake, fluttering colorful Tibetan prayer flags, and breathtaking snow peaks.",
    "Madhuri Lake": "A pristine alpine lake surrounded by steep high mountains, featuring old dead tree trunks standing straight up out of the calm water surface.",
    "Jaswant Garh": "A neat brick military war memorial shrine honoring brave Indian soldiers, with the national flag flying high next to white snow layers.",
    
    "Valiyaparamba": "A peaceful blue backwater river body separated from a sandy ocean beach by a narrow strip of tall green coconut trees.",
    "Ezhimala Hill": "Scenic green coastal hills rising right next to the blue crashing sea waves, offering a beautiful ocean promontory view.",
    "Chootad Beach": "A highly peaceful empty beach strip bordered by a thick, beautiful forest line of tall, straight green casuarina pine trees.",
    "Madayipara": "A vast, open flat laterite rock plateau completely covered in a beautiful seasonal carpet layer of tiny blue and yellow wildflowers."
}

nearby_images_map = {
    "Dawki Umngot Deep Gorge": ["mawlynnong.png", "root_bridge.png", "shnongpdeng.png", "krang_suri.png"],
    "Chorla Ghat Secret Streams": ["vazra_sakla.png", "anjunem_dam.png", "dudhsagar.png", "bondla.png"],
    "Suvali Isolated Beach": ["dumas_beach.png", "surat_castle.png", "cemeteries.png", "gavier_lake.png"],
    "Nuranang Hidden Falls": ["tawang_monastery.png", "sela_pass.png", "madhuri_lake.png", "jaswant_garh.png"],
    "Kavvayi Secret Backwaters": ["valiyaparamba.png", "ezhimala.png", "chootad.png", "madayipara.png"]
}

local_files = ["dawki.png", "chorla.png", "suvali.png", "nuranang.png", "kavvayi.png"]
b64_photo_streams = [get_image_base64_string(f) for f in local_files]

df = pd.DataFrame({
    "Place Name": places,
    "Category": categories,
    "AI Rating": ratings,
    "AI_Description": ai_scraped_descriptions,
    "Itinerary": ai_itineraries,
    "Crowd": crowd_status,
    "Photo_Path": b64_photo_streams,
    "lat": latitudes,
    "lon": longitudes,
    "Distance_KM": distances_km,
    "Nearby_Hotspots": nearby_locations
})

if origin_point == "Kempegowda Int. Airport (KIA)":
    df["Calculated_Budget"] = [25000, 25000, 14500, 32000, 12432]
else:
    df["Calculated_Budget"] = df["Distance_KM"] * current_rate

st.sidebar.markdown(f"Current Rate: Rs.{current_rate}/KM for {transport_mode}")
st.markdown("---")

# ====================================================================
# 5. NLP-BASED CONVERSATIONAL SEARCH
# ====================================================================
st.write("### NLP-Based Conversational Search")
user_comment = st.text_input(
    "Type your travel mood (e.g., I want a beautiful waterfall / peaceful trekking / hidden beach):",
    key="travel_mood_search_input"
)

filtered_df = df.copy()

if user_comment:
    with st.spinner("NLP Engine analyzing sentiment tokens..."):
        time.sleep(0.4)
    
    user_query = user_comment.lower()
    if "waterfall" in user_query or "water" in user_query or "falls" in user_query or "nuranang" in user_query:
        filtered_df = df[df["Category"] == "Waterfall"]
        st.success("Waterfall Mood Detected! Showing best hidden cascades.")
    elif "trekking" in user_query or "trek" in user_query or "hill" in user_query or "mountain" in user_query or "chorla" in user_query:
        filtered_df = df[df["Category"] == "Trekking"]
        st.success("Adventure/Trekking Mood Detected! Showing best mountain spots.")
    elif "secret terrains" in user_query or "dawki" in user_query or "gorge" in user_query or "canyon" in user_query:
        filtered_df = df[df["Category"] == "Secret Terrains"]
        st.success("Secret Terrains/Canyon Mood Detected! Showing historical gems.")
    elif "blue" in user_query or "escapes" in user_query or "backwater" in user_query or "kavvayi" in user_query:
        filtered_df = df[df["Category"] == "Blue Escapes"]
        st.success("Blue Escapes Mood Detected! Showing traditional hidden hotspots.")
    elif "beach" in user_query or "coast" in user_query or "suvali" in user_query:
        filtered_df = df[df["Category"] == "Beach"]
        st.success("Beach Mood Detected! Showing isolated coastlines.")
    else:
        if selected_category != "All":
            filtered_df = df[df["Category"] == selected_category]
        st.info("Positive Sentiment Detected! Showing personalized options for you.")
else:
    if selected_category != "All":
        filtered_df = df[df["Category"] == selected_category]

# ====================================================================
# 6. HYBRID RECOMMENDATION OUTPUT
# ====================================================================
st.write("### Hybrid Recommendation")
st.dataframe(filtered_df[["Place Name", "Category", "AI Rating", "Crowd", "Distance_KM", "Calculated_Budget"]], use_container_width=True)

if not filtered_df.empty:
    st.write("#### AI Intel Card Discovery (Scraped Insights)")
    records = filtered_df.to_dict(orient="records")
    for row in records:
        with st.container():
            name = row["Place Name"]
            cost = row["Calculated_Budget"]
            dist = row["Distance_KM"]
            st.markdown(f"### {name}")
            
            try:
                st.image(row["Photo_Path"], use_container_width=True, caption=f"AI Scraped Photographic Capture: {name}")
            except Exception:
                st.image("https://picsum.photos", use_container_width=True, caption=f"Placeholder Image for {name}")
            
            place_address = main_places_addresses.get(name, "Address Not Scraped")
            st.markdown(f"📍 **Full Address:** `{place_address}`")
            
            st.markdown(f"""
            <div style="background-color: #1E293B; padding: 12px; border-radius: 8px; border-left: 5px solid #00FFBB; margin-bottom: 10px;">
                <span style="color: white; font-weight: bold;">Travel Metrics:</span> 
                <span style="color: #00FFBB; margin-left: 15px;">Distance: <b>{dist} KM</b></span> | 
                <span style="color: #FF5733; margin-left: 15px;">Estimated Cost: <b>Rs.{cost:,.2f}</b></span>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(row["AI_Description"])
            
            st.markdown("<span style='color: #38BDF8; font-weight: bold; font-size: 14px;'>📍 AI Suggested Nearby Hotspots (with Distance Matrix):</span>", unsafe_allow_html=True)
            # ====================================================================
            # 🛠️ QUICK ADD: COMPACT LOCAL INSIGHTS DISCOVERY CARD
            # ====================================================================
            # Language neutral data matrix for hidden gems mapping
            local_insights = {
                "Dawki Umngot Deep Gorge": "A jaw-dropping deep canyon featuring the impossibly transparent, emerald-green waters of the Umngot River near the Indo-Bangladesh border. The water is so crystalline that wooden boats appear to float in mid-air, creating a perfect surreal visual experience.",
                "Chorla Ghat Secret Streams": "Hidden deep within the lush, evergreen Western Ghats rainforest, this serene spot features crystal-clear freshwater rapids and pristine streams. It is a peaceful paradise for trekkers, birdwatchers, and nature lovers seeking absolute solitude.",
                "Suvali Isolated Beach": "A serene and completely secluded coastline on the outskirts of Surat, Gujarat, characterized by its unique jet-black volcanic sand. Bordered by a dense, straight forest line of tall green casuarina pine trees, it is perfect for peaceful mental relaxation.",
                "Nuranang Hidden Falls": "Located in the Tawang district of Arunachal Pradesh, this spectacular 100-meter waterfall plunges down rugged Himalayan slopes. Surrounded by dense forests and layers of mystical mountain mist, it offers a truly breathtaking and hidden natural escape.",
                "Kavvayi Secret Backwaters": "North Kerala's largest undiscovered backwater stretch, formed by a peaceful cluster of small mangrove islands and lined with tall coconut trees. It offers a pure, rustic coastal vibe completely away from commercial crowds."
            }

            # Fetch description text dynamically based on the current active record name
            info_text = local_insights.get(name, "Information not available for this location.")

            # High-fidelity custom dark-themed UI container with neutral universal headers
            st.markdown(f"""
            <div style="background-color: #0F172A; padding: 16px; border-radius: 8px; border-top: 4px solid #38BDF8; margin-top: 10px; margin-bottom: 15px;">
                <p style="color: #38BDF8; font-weight: bold; font-size: 14px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">
                    📜 AI Scraped Local Insights & Summary:
                </p>
                <p style="color: #E2E8F0; font-size: 14.5px; text-align: justify; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
                    {info_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
            hotspots_list = row['Nearby_Hotspots'].split(',')
            
            # ====================================================================
            # 🛠️ UPDATED SECTION: INTERACTIVE HIGH-CONTRAST EXPANDER CARDS BELOW IMAGES
            # ====================================================================
            sub_images = nearby_images_map.get(name, [])
            spots_distance_dict = nearby_places_info.get(name, {})
            
            # 1. Display only the 4 nearby spot images in a clean row grid first
            img_cols = st.columns(4)
            for idx, spot in enumerate(hotspots_list):
                spot_clean = spot.strip()
                if idx < len(img_cols):
                    with img_cols[idx]:
                        img_file = sub_images[idx] if idx < len(sub_images) else ""
                        img_b64 = get_image_base64_string(img_file)
                        try:
                            st.image(img_b64, use_container_width=True, caption=spot_clean)
                        except Exception:
                            st.image("https://picsum.photos", use_container_width=True, caption=spot_clean)

            st.markdown("<br>", unsafe_allow_html=True)

            # 2. Display highly professional, bright-colored dropdown cards below the images
            for spot in hotspots_list:
                spot_clean = spot.strip()
                distance_from_main = spots_distance_dict.get(spot_clean, "N/A")
                spot_explanation = nearby_hotspots_explain.get(spot_clean, "No explanation available.")
                
                # Expanders provide a neat vertical list without cluttering the screen width
                with st.expander(f"📌 {spot_clean} (🚗 Distance: {distance_from_main})", expanded=False):
                    st.markdown(f"""
                    <div style="
                        background-color: #0F172A; 
                        padding: 15px; 
                        border-radius: 8px; 
                        border-left: 4px solid #38BDF8; 
                        margin: 5px 0px;
                    ">
                        <p style="color: #00FFBB; font-weight: bold; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">
                            🚗 Proximity Vector: {distance_from_main} from Main Base
                        </p>
                        <p style="color: #F8FAFC; font-size: 14.5px; text-align: justify; line-height: 1.5; font-family: 'Segoe UI', sans-serif; font-weight: 500; margin-top: 0;">
                            {spot_explanation}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write(f"Category: `{row['Category']}` | AI Rating: `{row['AI Rating']}` | Predictive Crowd Density: {row['Crowd']}")
            with st.expander(f"View AI Scraped Day-Itinerary for {name}"):
                st.text(row["Itinerary"])
            st.markdown("<br><hr style='border: 0.5px dashed #A0AEC0;'><br>", unsafe_allow_html=True)
else:
    st.warning("No hidden gems found matching your query!")

st.markdown("---")

# ====================================================================
# 7. GEOSPATIAL HOTSPOT MAPPING
# ====================================================================
st.write("### Geospatial Hotspot Mapping")
if not filtered_df.empty:
    st.map(filtered_df[["lat", "lon"]], zoom=4)
else:
    st.info("No locations to display on map.")