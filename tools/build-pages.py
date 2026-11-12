#!/usr/bin/env python3
"""tools/build-pages.py — /rooms/ /restaurant/ /location/ /contact/ pages banata hai.
   index.html se header/footer/sticky/scripts reuse karta hai (same design),
   i18n strings app.src.js me PAGE-I18N marker block me likhta hai.
   Chalayein: python3 tools/build-pages.py   (project root se)"""
import re, os, json, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
IDX = os.path.join(ROOT, "index.html")
t = open(IDX, encoding="utf-8").read()

BASE = "https://shreemahamayahotelpallu.netlify.app"
NAP = ('Shri Maha Maya Hotel &amp; Restaurant · Main Highway, near Indian Oil Fuel Station, Pallu, '
       'Hanumangarh, Rajasthan 335522 · +91 81073 01306 · +91 96604 01306 · shreemahamayahotel@gmail.com')

# ---------- shared blocks from index.html ----------
head = t[:t.index("</head>")]
header = t[t.index('<header class="nav"'):t.index("</header>") + len("</header>")]
mmenu = t[t.index('<div class="m-menu"'):t.index("</div>", t.index('<div class="m-menu"')) + 6]
# m-menu block ends at first </div> after its inner content? safer: up to marker before <main
mmenu = t[t.index('<div class="m-menu"'):t.index("<main")]
footer = t[t.index("<footer"):t.index("</footer>") + len("</footer>")]
tail = t[t.index("<!-- Sticky mobile quick-contact bar -->"):]
_fs = t.rindex("<form", 0, t.index('id="booking-form"'))
form = t[_fs:t.index("</form>", _fs) + len("</form>")]
m0 = t.index('<div class="food-tabs reveal" role="tablist" id="food-tabs">')
menuui = t[m0:t.index("</div>", t.index('id="food-tabs-body"')) + 6]

# ---------- i18n content (single source of truth) ----------
I = {}
def add(k, en, hi): I[k] = {"en": en, "hi": hi}

# /rooms/
add("pg.r.h1", "AC Rooms in Pallu — Standard, Deluxe & Family at Our Pure Veg Hotel",
    "पल्लू में एसी कमरे — हमारे शुद्ध शाकाहारी होटल में स्टैण्डर्ड, डीलक्स और फ़ैमिली")
add("pg.r.lede", "Three simple room types and one honest promise: cool air, hot water, a quiet night and pure-veg room service at any hour of the day or night.",
    "तीन सरल कमरे और एक साफ़ वादा: ठंडी हवा, गरम पानी, शांत रात और किसी भी समय शुद्ध शाकाहारी रूम सर्विस।")
add("pg.r.h2a", "Room types and rates", "कमरे के प्रकार और दाम")
add("pg.r.p1", "Shri Maha Maya Hotel & Restaurant has ten air-conditioned guest rooms in three types. Every rate is per room per night, not per person, so a couple pays the same as a solo traveller. Booking is simple: call or WhatsApp us, pay an advance of half the room rent or more, and your room is held for you.",
    "श्री महा माया होटल एण्ड रेस्टोरेंट में तीन प्रकार के दस एसी कमरे हैं। हर दाम प्रति कमरा प्रति रात है, प्रति व्यक्ति नहीं — यानी युगल और अकेले यात्री का दाम samaan। बुकिंग आसान है: कॉल या WhatsApp कीजिए, आधी दाम या उससे अधिक एडवांस दीजिए, और कमरा आपके नाम रहता है।")
add("pg.r.h3a", "Standard AC Room — ₹1,000 per night", "स्टैण्डर्ड एसी कमरा — ₹1,000 प्रति रात")
add("pg.r.p2", "Simple, spotless and easy on the pocket. A comfortable queen bed, working AC, attached bathroom with geyser and room service on call. Sleeps 2–3 guests — the right pick for solo travellers, couples and pilgrims who want a good night without extra frills.",
    "सरल, साफ़ और बजट के अनुकूल। आरामदायक क्वीन बेड, चलता एसी, गीज़र वाला अटैच्ड बाथरूम और कॉल पर रूम सर्विस। 2–3 मेहमान — अकेले यात्रियों, युगलों और श्रद्धालुओं के लिए सही।")
add("pg.r.h3b", "Deluxe AC Room — ₹1,200 per night", "डीलक्स एसी कमरा — ₹1,200 प्रति रात")
add("pg.r.p3", "A little more space and light, with a private balcony to step out onto after a long drive. Same queen bed, attached bath, geyser and 24×7 room service. Sleeps 2–3 guests — couples on a road trip usually pick this one.",
    "थोड़ी ज़्यादा जगह और रोशनी, तथा लंबे सफ़र के बाद निकलने के लिए निजी बालकनी। वही क्वीन बेड, अटैच्ड बाथ, गीज़र और 24×7 रूम सर्विस। 2–3 मेहमान — रोड ट्रिप वाले युगल इसे चुनते हैं।")
add("pg.r.h3c", "Family AC Room — ₹1,400 per night", "फ़ैमिली एसी कमरा — ₹1,400 प्रति रात")
add("pg.r.p4", "Our largest room, made for families: two beds, a table and chairs, and space for 3–4 guests. An extra bed can be added for ₹200 per night. Attached bathroom, geyser, AC and round-the-clock room service included.",
    "हमारा सबसे बड़ा कमरा, परिवारों के लिए: दो बिस्तर, मेज़-कुर्सियाँ और 3–4 मेहमानों की जगह। ₹200 प्रति रात में एक्स्ट्रा बेड। अटैच्ड बाथरूम, गीज़र, एसी और चौबीसों घंटे रूम सर्विस शामिल।")
add("pg.r.h2b", "What every room includes", "हर कमरे में क्या-क्या है")
add("pg.r.l1", "Air conditioning and a comfortable bed with clean linen", "एयर कंडीशनिंग और साफ़ चादर के साथ आरामदायक बिस्तर")
add("pg.r.l2", "Attached bathroom with geyser (hot water at any hour)", "गीज़र वाला अटैक्ड बाथरूम (किसी भी समय गरम पानी)")
add("pg.r.l3", "24×7 room service from our pure-veg kitchen", "हमारी शुद्ध शाकाहारी रसोई से 24×7 रूम सर्विस")
add("pg.r.l4", "Free Wi-Fi in rooms, lobby and restaurant", "कमरों, लॉबी और रेस्टोरेंट में मुफ़्त Wi-Fi")
add("pg.r.l5", "CCTV-monitored premises and secure parking beside the hotel", "CCTV निगरानी वाला परिसर और होटल के बगल में सुरक्षित पार्किंग")
add("pg.r.l6", "Balcony in Deluxe; table-chairs and two beds in Family", "डीलक्स में बालकनी; फ़ैमिली में मेज़-कुर्सियाँ और दो बिस्तर")
add("pg.r.h2c", "Check-in, payment and house rules", "चेक-इन, भुगतान और नियम")
add("pg.r.p5", "Check-in is possible at any time because the front desk never closes; check-out is at 11:00 AM. Please carry a government photo ID (Aadhaar, driving licence or voter ID) for every booking. An advance of half the room rent or more confirms your reservation; cancellations are fully refunded only within 20–30 minutes of booking.",
    "फ्रंट डेस्क कभी बंद नहीं होता, इसलिए चेक-इन किसी भी समय संभव है; चेक-आउट सुबह 11:00 बजे है। हर बुकिंग के लिए सरकारी फोटो आईडी (आधार, ड्राइविंग लाइसेंस या वोटर आईडी) लाइए। आधी दाम या उससे अधिक एडवांस बुकिंग पक्की करती है; cancellation पर full refund केवल बुकिंग के 20–30 मिनट के भीतर।")
add("pg.r.p6", "We accept cash and UPI. Pets are welcome at the hotel. Please note we do not provide driver or staff accommodation, and breakfast is not included in room rates — though the kitchen is always a short call away.",
    "हम नकद और UPI स्वीकार करते हैं। पालतू जानवर स्वीकार हैं। कृपया ध्यान दें: ड्राइवर/स्टाफ़ ठहरने की व्यवस्था नहीं है, और नाश्ता कमरे के दाम में शामिल नहीं — हालाँकि रसोई बस एक कॉल दूर है।")
add("pg.r.h2d", "Which room should you pick?", "कौन-सा कमरा चुनें?")
add("pg.r.p7", "Travelling solo or as a couple on a budget, the Standard AC room covers everything you need. Want a balcony and a little more room to breathe after hours on the highway, choose Deluxe. With children or a small group of three to four, the Family AC room with two beds and a sitting table is the comfortable choice — and the pure-veg thali is never more than a phone call away.",
    "अकेले या बजट में युगल हों तो स्टैण्डर्ड एसी काफी है। हाईवे के घंटों बाद बालकनी और थोड़ी जगह चाहिए तो डीलक्स लीजिए। बच्चों या 3–4 लोगों के साथ फ़ैमिली एसी कमरा दो बिस्तर और बैठक की मेज़ के साथ आरामदायक है — और शुद्ध शाकाहारी थाली बस एक कॉल दूर।")

# /restaurant/
add("pg.e.h1", "Pure Veg Restaurant & Rajasthani Thali on the Highway at Pallu",
    "पल्लू में हाईवे पर शुद्ध शाकाहारी रेस्टोरेंट और राजस्थानी थाली")
add("pg.e.lede", "A 100% vegetarian kitchen that never sleeps late-night: thali, tawa rotis, kadhi, pakoras and highway-style chai, made fresh for every order.",
    "एक 100% शाकाहारी रसोई जो देर रात तक जागती है: थाली, तवा रोटी, कढ़ी, पकौड़े और हाईवे वाली चाय — हर ऑर्डर पर ताज़ा।")
add("pg.e.h2a", "A 100% pure-vegetarian kitchen", "100% शुद्ध शाकाहारी रसोई")
add("pg.e.p1", "Shri Maha Maya is a pure-vegetarian hotel and restaurant on the highway at Pallu, Hanumangarh. No eggs, no compromises: flour from the local mill, desi ghee, and spices ground in our own kitchen. Jain food can be prepared on request, and every dish is cooked fresh when you order it.",
    "श्री महा माया पल्लू, हनुमानगढ़ में हाईवे पर स्थित शुद्ध शाकाहारी होटल और रेस्टोरेंट है। न अंडा, न समझौता: स्थानीय चक्की का आटा, देसी घी और अपनी रसोई में पिसे मसाले। अनुरोध पर जैन भोजन बनता है, और हर व्यंजन ऑर्डर पर ताज़ा बनता है।")
add("pg.e.p2", "Families, truckers, pilgrims and road-trippers all eat at the same tables here — that is the point of a highway hotel. The dining hall is simple, clean and quick, and parcel orders are packed hot for the road ahead. We do not offer home delivery; takeaway and parcel are always available.",
    "परिवार, ट्रक चालक, श्रद्धालु और रोड-ट्रिपर — सब यहाँ एक ही मेज़ों पर खाते हैं। डाइनिंग हॉल सरल, साफ़ और तेज़ है, और पार्सल गरम पैक होते हैं। होम डिलीवरी नहीं है; टेकअवे और पार्सल हमेशा उपलब्ध।")
add("pg.e.h2b", "The Rajasthani thali", "राजस्थानी थाली")
add("pg.e.p3", "Dal, sabji, roti, dahi and salad — everything on one platter. Our thali at ₹140 is the most-ordered plate in the house: seasonal sabji, dal tempered with ghee and cumin, soft tawa or tandoori rotis, cool dahi and a fresh salad. Ask for a half portion of paneer or masala dishes if you are travelling light.",
    "दाल, सब्ज़ी, रोटी, दही और सलाद — सब कुछ एक थाली में। ₹140 की हमारी थाली घर की सबसे ऑर्डर की जाने वाली प्लेट है: मौसमी सब्ज़ी, घी-जीरे की तड़के वाली दाल, नरम तवा या तंदूरी रोटी, ठंडा दही और ताज़ा सलाद। हल्का खाना हो तो पनीर या मसाला व्यंजनों की हाफ पortion पूछिए।")
add("pg.e.h2c", "Full menu — twelve categories", "पूरा मेनू — बारह श्रेणियाँ")
add("pg.e.p4", "Paneer, masala, dal, dahi-raita, roti, rice, Mahamaya specials, beverages, salad, parantha, fast food and papad — seventy-one dishes in all, each priced per plate. Tap a category below; half portions are available on paneer, masala, dal, rice, specials and fast food items.",
    "पनीर, मसाला, दाल, दही-रायता, रोटी, चावल, महामाया स्पेशल, पेय, सलाद, परांठा, फास्ट फूड और पापड़ — कुल 71 व्यंजन, हर एक का दाम प्रति प्लेट। नीचे श्रेणी टैप कीजिए; पनीर, मसाला, दाल, चावल, स्पेशल और फास्ट फूड में हाफ पortion मिलती है।")
add("pg.e.h2d", "Kitchen hours, chai and late-night orders", "रसोई का समय, चाय और देर रात ऑर्डर")
add("pg.e.p5", "The kitchen serves from 6:00 AM to 12:30 AM every day, and room service runs 24×7 for hotel guests. Early departures get 5 AM chai on request; late arrivals get masala maggi, pakoras or a full meal before the road resumes. For parcels, call ahead and your order is packed hot by the time you reach the counter.",
    "रसोई हर दिन सुबह 6:00 से रात 12:30 तक चलती है, और होटल मेहमानों के लिए रूम सर्विस 24×7। जल्दी निकलने वालों को अनुरोध पर सुबह 5 बजे चाय; देर से पहुँचने वालों को मसाला मैगी, पकौड़े या पूरा भोजन। पार्सल के लिए पहले कॉल कीजिए — काउंटर पहुँचते ही ऑर्डर गरम पैक मिलेगा।")

# /location/
add("pg.l.h1", "Highway Hotel at Pallu — Beside the Indian Oil Fuel Station, Hanumangarh",
    "पल्लू में हाईवे होटल — इंडियन ऑयल फ्यूल स्टेशन के बगल में, हनुमानगढ़")
add("pg.l.lede", "A natural halt on the highway: fuel up next door, eat a hot thali across the counter, and sleep in a cool, quiet room a few steps away.",
    "हाईवे पर स्वाभाविक पड़ाव: बगल में ईंधन, काउंटर पर गरम थाली, और कुछ कदम दूर ठंडा, शांत कमरा।")
add("pg.l.h2a", "Exact address and landmark", "पूरा पता और पहचान")
add("pg.l.p1", "Shri Maha Maya Hotel & Restaurant stands on the main highway at Pallu, Hanumangarh district, Rajasthan 335522, directly beside the Indian Oil fuel station. If you can see the fuel station, you have already seen our signboard. Ample parking for cars, SUVs, buses and trucks sits right off the highway.",
    "श्री महा माया होटल एण्ड रेस्टोरेंट राजस्थान 335522, ज़िला हनुमानगढ़ के पल्लू में मुख्य हाईवे पर, इंडियन ऑयल फ्यूल स्टेशन के ठीक बगल में है। फ्यूल स्टेशन दिखते ही हमारा बोर्ड भी दिख जाएगा। कार, SUV, बस और ट्रकों के लिए पर्याप्त पार्किंग हाईवे से सटी है।")
add("pg.l.h2b", "Serving travellers from", "किन शहरों के यात्रियों के लिए")
add("pg.l.p2", "Travellers across this belt of Rajasthan make Shri Maha Maya their regular halt. Approximate road distances from the hotel:",
    "राजस्थान के इस क्षेत्र के यात्री श्री महा माया को अपना नियमित पड़ाव मानते हैं। होटल से अनुमानित सड़क दूरियाँ:")
add("pg.l.c1", "Rawatsar — approx. 40 km", "रॉवतसर — लगभग 40 किमी")
add("pg.l.c2", "Sardarshahar — approx. 60 km", "सरदारशहर — लगभग 60 किमी")
add("pg.l.c3", "Nohar — approx. 70 km", "नोहर — लगभग 70 किमी")
add("pg.l.c4", "Hanumangarh — approx. 80 km", "हनुमानगढ़ — लगभग 80 किमी")
add("pg.l.c5", "Bikaner — approx. 150 km", "बीकानेर — लगभग 150 किमी")
add("pg.l.c6", "Salasar — approx. 165 km", "सालासर — लगभग 165 किमी")
add("pg.l.c7", "Khatu Shyam — approx. 260 km", "खटू श्याम — लगभग 260 किमी")
add("pg.l.h2c", "On the highway route", "हाईवे रूट पर")
add("pg.l.p3", "The hotel sits on the busy highway corridor that links Bikaner and Hanumangarh towards the Sri Ganganagar side, with traffic from the Bathinda and Sirsa direction joining the same stretch. That makes it an easy, well-lit stop: no narrow lanes, no U-turns — turn in beside the fuel station and you are parked.",
    "होटल उस व्यस्त हाईवे कॉरिडोर पर है जो बीकानेर और हनुमानगढ़ को श्री गंगानगर की ओर जोड़ता है, और बठिंडा-सीरसा दिशा का ट्रैफ़िक भी इसी खंड पर मिलता है। इसलिए पड़ाव आसान और रोशन है: न तंग गलियाँ, न यू-टर्न — फ्यूल स्टेशन के बगल से मुड़िए और आप पार्क।")
add("pg.l.h2d", "Map, directions and reviews", "नक्शा, दिशा-निर्देश और समीक्षाएँ")
add("pg.l.h2e", "Parking, fuel and traveller basics", "पार्किंग, ईंधन और यात्री सुविधाएँ")
add("pg.l.p5", "Fuel next door, ample parking beside the hotel, clean washrooms and a pure-veg kitchen open till 12:30 AM: the small things that matter on a long drive are all handled in one stop. Bus and truck crews can park overnight beside the hotel and request 5 AM chai before an early departure.",
    "बगल में ईंधन, होटल के साथ पर्याप्त पार्किंग, साफ़ वॉशरूम और रात 12:30 तक खुली शुद्ध शाकाहारी रसोई: लंबे सफ़र की छोटी-बड़ी ज़रूरतें एक ही पड़ाव पर पूरी। बस और ट्रक चालक रात भर होटल के बगल में पार्क कर सकते हैं और तड़के निकलने से पहले 5 बजे की चाय पा सकते हैं।")
add("pg.l.p4", "Use the map below for turn-by-turn navigation, open our Google Maps listing to save the place, or read and write reviews on our Google profile. Coordinates for GPS devices: 28.938974, 74.216543.",
    "नीचे के नक्शे से बारी-बारी नेविगेशन पाइए, गूगल मैप्स लिस्टिंग खोलकर जगह सेव कीजिए, या गूगल प्रोफ़ाइल पर समीक्षाएँ पढ़िए-लिखिए। GPS उपकरणों के लिए निर्देशांक: 28.938974, 74.216543।")

# /contact/
add("pg.c.h1", "Contact Shri Maha Maya Hotel & Restaurant — Call, WhatsApp or Booking Form",
    "संपर्क करें — कॉल, व्हाट्सएप या बुकिंग फ़ॉर्म")
add("pg.c.lede", "We reply within minutes on WhatsApp and phone, day or night. The front desk is staffed 24×7, so there is always a human at the other end.",
    "हम व्हाट्सएप और फ़ोन पर मिनटों में जवाब देते हैं, दिन हो या रात। फ्रंट डेस्क 24×7 है, इसलिए हमेशा कोई न कोई मौजूद है।")
add("pg.c.h2a", "Phone, WhatsApp and email", "फ़ोन, व्हाट्सएप और ईमेल")
add("pg.c.p1", "Call the front desk on +91 81073 01306 (also WhatsApp) or +91 96604 01306 at any hour. For written enquiries, email shreemahamayahotel@gmail.com. For room availability, food orders or parcel requests, WhatsApp is fastest — one message and we confirm.",
    "फ्रंट डेस्क को किसी भी समय +91 81073 01306 (व्हाट्सएप भी) या +91 96604 01306 पर कॉल कीजिए। लिखित पूछताछ के लिए shreemahamayahotel@gmail.com। कमरे की उपलब्धता, खाना या पार्सल के लिए व्हाट्सएप सबसे तेज़ — एक मैसेज, और हम पुष्टि करते हैं।")
add("pg.c.h2b", "Booking enquiry form", "बुकिंग पूछताछ फ़ॉर्म")
add("pg.c.p2", "Fill the form below with your dates, guests and room preference. On submit it validates your details and opens a pre-filled WhatsApp message to the hotel, so your enquiry reaches us instantly with everything we need to confirm your stay.",
    "नीचे फ़ॉर्म में तारीख़ें, मेहमान और कमरे की पसंद भरिए। भेजते ही फ़ॉर्म विवरण जाँचता है और होटल को एक पूर्व-भरा व्हाट्सएप संदेश खोलता है, जिससे आपकी पूछताछ तुरंत हम तक पहुँचती है।")
add("pg.c.h2c", "Front desk and kitchen hours", "फ्रंट डेस्क और रसोई का समय")
add("pg.c.p3", "Front desk and room service: 24×7, all days. Restaurant kitchen: 6:00 AM to 12:30 AM daily. Check-in any time; check-out 11:00 AM. Early chai at 5 AM can be arranged the night before — just tell the desk.",
    "फ्रंट डेस्क और रूम सर्विस: 24×7, हर दिन। रेस्टोरेंट रसोई: सुबह 6:00 से रात 12:30 तक। चेक-इन किसी भी समय; चेक-आउट 11:00 AM। सुबह 5 बजे चाय एक रात पहले बता देने पर व्यवस्थित हो जाती है।")
add("pg.c.h2d", "Frequently asked questions", "अक्सर पूछे जाने वाले प्रश्न")

# ---------- page shells ----------
def tag(k, tg, attrs=""):
    return '<%s%s data-i18n="%s">%s</%s>' % (tg, attrs, k, I[k]["en"], tg)

def crumbs(page_label_en, page_i18n_key):
    return ('<nav class="crumbs container" aria-label="Breadcrumb"><ol>'
            '<li><a href="/">Home</a></li><li aria-current="page">%s</li></ol></nav>' % page_label_en)

CTA_BOOK = ('<div class="page-cta container sec-cta-btns">'
            '<a class="btn btn-gold" href="/contact/#booking-form" data-i18n="cta.book">Book Your Room</a>'
            '<a class="btn btn-outline" href="https://wa.me/918107301306?text=Namaste!%20I%20would%20like%20to%20enquire%20about%20Shri%20Maha%20Maya%20Hotel%2C%20Pallu." data-wa '
            'data-wa-en="Namaste! I would like to enquire about Shri Maha Maya Hotel, Pallu." '
            'data-wa-hi="नमस्ते! मैं श्री महा माया होटल, पल्लू के बारे में पूछताछ करना चाहता/चाहती हूँ।" data-ga="click_whatsapp">'
            '<span data-icon="whatsapp"></span><span data-i18n="cta.wa">Ask on WhatsApp</span></a>'
            '<a class="btn btn-outline" href="tel:+918107301306" data-ga="click_call"><span data-icon="phone"></span><span data-i18n="cta.call2">Call the Hotel</span></a></div>')
add("cta.call2", "Call the Hotel", "होटल को कॉल करें")

FAQ = [(q, a) for q, a in [
    ("What are the room prices at Shri Maha Maya Hotel & Restaurant?", "Standard AC rooms are ₹1,000, Deluxe AC ₹1,200 and Family AC ₹1,400 per room per night. Prices are per room, not per person."),
    ("What are the check-in and check-out times?", "Check-in is possible any time — our front desk is open 24×7. Check-out is at 11:00 AM."),
    ("Is the restaurant really 100% pure vegetarian?", "Yes. Our kitchen is completely pure vegetarian with no eggs. Jain food can be prepared on request."),
    ("Do you have parking for buses and trucks?", "Yes. There is ample parking right off the highway for cars, SUVs, buses and trucks, beside the Indian Oil fuel station."),
    ("Is Wi-Fi available at the hotel?", "Yes, free Wi-Fi is available in rooms, the lobby and the restaurant."),
    ("Is the front desk open at night?", "Yes, the front desk and room service run 24×7. The kitchen serves from 6:00 AM to 12:30 AM."),
    ("Where exactly is the hotel located?", "We are on the main highway at Pallu, Hanumangarh, Rajasthan 335522, beside the Indian Oil fuel station."),
    ("How do I book a room?", "Call or WhatsApp us on +91 81073 01306, or send the booking form on this website. An advance of half the room rent or more confirms your booking."),
    ("Which cities and routes do travellers come from?", "Guests stop with us while travelling between Pallu, Hanumangarh, Sri Ganganagar, Nohar, Bikaner, Bathinda and Sirsa on the highway."),
    ("Do you have family rooms?", "Yes, the Family AC room sleeps 3–4 guests at ₹1,400 per night. An extra bed can be added for ₹200."),
    ("What payment methods do you accept?", "We accept cash and UPI payments."),
    ("Are pets allowed at the hotel?", "Yes, pets are allowed at the hotel.")]]
FAQ_HTML = '<div class="faq-list">' + "\n".join(
    '<details class="faq-item"><summary data-i18n="faq.q%d">%s</summary><p data-i18n="faq.a%d">%s</p></details>' % (i, q, i, a)
    for i, (q, a) in enumerate(FAQ, 1)) + "</div>"

ROOM_CARDS = ""
for key, h3, p, price in [("standard", "pg.r.h3a", "pg.r.p2", "₹1,000"), ("deluxe", "pg.r.h3b", "pg.r.p3", "₹1,200"), ("family", "pg.r.h3c", "pg.r.p4", "₹1,400")]:
    ROOM_CARDS += ('<h3 data-i18n="%s">%s</h3>%s\n'
        '<a class="btn btn-gold btn-sm" href="https://wa.me/918107301306?text=Namaste!%%20Is%%20the%%20%s%%20room%%20available%%3F" data-wa '
        'data-wa-en="Namaste! Is the %s room available tonight? Please confirm." '
        'data-wa-hi="नमस्ते! क्या %s कमरा आज रात खाली है? कृपया पुष्टि कीजिए।" data-ga="click_whatsapp">'
        '<span data-i18n="rooms.check">Check Availability</span> <span class="arrow">→</span></a>\n') % (
        h3, I[h3]["en"], tag(p, "p"), key.capitalize(), key.capitalize(),
        {"standard": "स्टैण्डर्ड एसी", "deluxe": "डीलक्स एसी", "family": "फ़ैमिली एसी"}[key])

PAGES = {
 "rooms": dict(
   title="AC Rooms in Pallu ₹1,000–₹1,400 | Shri Maha Maya Hotel",
   desc="Standard, Deluxe & Family AC rooms at our pure-veg highway hotel in Pallu, Hanumangarh. ₹1,000–₹1,400 per room per night, 24×7 desk. Check availability on WhatsApp.",
   crumbs_label="Rooms",
   body=('<section class="page-hero"><div class="container">' + crumbs("Rooms", None) +
     tag("pg.r.h1", "h1") + tag("pg.r.lede", "p", ' class="lede"') + '</div></section>'
     '<div class="page-nap"><div class="container"><p class="nap">' + NAP + '</p></div></div>'
     '<section class="container prose">' + tag("pg.r.h2a", "h2") + tag("pg.r.p1", "p") +
     ROOM_CARDS + tag("pg.r.h2b", "h2") + '<ul>' + "".join(tag("pg.r.l%d" % i, "li") for i in range(1, 7)) + '</ul>' +
     tag("pg.r.h2c", "h2") + tag("pg.r.p5", "p") + tag("pg.r.p6", "p") +
     tag("pg.r.h2d", "h2") + tag("pg.r.p7", "p") + '</section>' + CTA_BOOK)),
 "restaurant": dict(
   title="Veg Restaurant Pallu | Shri Maha Maya Hotel & Restaurant",
   desc="100% pure-veg restaurant on the highway at Pallu: Rajasthani thali ₹140, 71 dishes across 12 categories, kitchen open 6 AM–12:30 AM. Parcel & takeaway, no home delivery.",
   crumbs_label="Restaurant",
   body=('<section class="page-hero"><div class="container">' + crumbs("Restaurant", None) +
     tag("pg.e.h1", "h1") + tag("pg.e.lede", "p", ' class="lede"') + '</div></section>'
     '<div class="page-nap"><div class="container"><p class="nap">' + NAP + '</p></div></div>'
     '<section class="container prose">' + tag("pg.e.h2a", "h2") + tag("pg.e.p1", "p") + tag("pg.e.p2", "p") +
     tag("pg.e.h2b", "h2") + tag("pg.e.p3", "p") + tag("pg.e.h2c", "h2") + tag("pg.e.p4", "p") + '</section>'
     '<section class="food" id="dining"><div class="container">' + menuui + '</div></section>'
     '<section class="container prose">' + tag("pg.e.h2d", "h2") + tag("pg.e.p5", "p") + '</section>' + CTA_BOOK)),
 "location": dict(
   title="Highway Hotel in Pallu | Shri Maha Maya Hotel & Restaurant",
   desc="Shri Maha Maya Hotel & Restaurant on the main highway at Pallu, Hanumangarh 335522 — beside the Indian Oil fuel station. Map, directions, parking and nearby cities.",
   crumbs_label="Location",
   body=('<section class="page-hero"><div class="container">' + crumbs("Location", None) +
     tag("pg.l.h1", "h1") + tag("pg.l.lede", "p", ' class="lede"') + '</div></section>'
     '<div class="page-nap"><div class="container"><p class="nap">' + NAP + '</p></div></div>'
     '<section class="container prose">' + tag("pg.l.h2a", "h2") + tag("pg.l.p1", "p") +
     tag("pg.l.h2b", "h2") + tag("pg.l.p2", "p") + '<ul>' + "".join(tag("pg.l.c%d" % i, "li") for i in range(1, 8)) + '</ul>' +
     tag("pg.l.h2c", "h2") + tag("pg.l.p3", "p") + tag("pg.l.h2d", "h2") + tag("pg.l.p4", "p") + tag("pg.l.h2e", "h2") + tag("pg.l.p5", "p") + '</section>'
     '<section class="location"><div class="container loc-grid"><div class="loc-col">'
     '<div class="loc-map" id="loc-map"><iframe id="map-iframe" title="Map — Shri Maha Maya Hotel & Restaurant, Pallu, Hanumangarh" '
     'src="https://www.google.com/maps?q=28.938974,74.216543&z=16&output=embed&hl=en" loading="lazy" '
     'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>'
     '<div class="map-actions">'
     '<a class="btn btn-gold btn-sm" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=28.938974,74.216543" data-ga="click_directions"><span data-icon="direction"></span><span data-i18n="loc.directions">Get Directions</span></a>'
     '<a class="btn btn-gold btn-sm" target="_blank" rel="noopener" href="https://www.google.com/maps/place/?q=place_id:0x3915cb5560ab22f7:0xd98ef3784c89800d" data-ga="click_directions"><span data-icon="direction"></span><span data-i18n="map.open">Open in Google Maps</span></a>'
     '<a class="btn map-rate btn-sm" target="_blank" rel="noopener" href="https://g.page/r/CQ2AiUx4847ZEBE/review" data-ga="click_review"><span data-icon="star"></span><span data-i18n="map.rate">Rate Us on Google</span></a>'
     '</div></div></div></section>' + CTA_BOOK)),
 "contact": dict(
   title="Contact & Booking | Shri Maha Maya Hotel & Restaurant",
   desc="Call +91 81073 01306, WhatsApp or email Shri Maha Maya Hotel & Restaurant, Pallu. 24×7 front desk, booking form with instant WhatsApp enquiry, and 12 quick FAQs.",
   crumbs_label="Contact",
   body=('<section class="page-hero"><div class="container">' + crumbs("Contact", None) +
     tag("pg.c.h1", "h1") + tag("pg.c.lede", "p", ' class="lede"') + '</div></section>'
     '<div class="page-nap"><div class="container"><p class="nap">' + NAP + '</p></div></div>'
     '<section class="container prose">' + tag("pg.c.h2a", "h2") + tag("pg.c.p1", "p") +
     '<div class="sec-cta-btns" style="justify-content:flex-start;margin:6px 0 10px">'
     '<a class="btn btn-gold" href="tel:+918107301306" data-ga="click_call"><span data-icon="phone"></span>+91 81073 01306</a>'
     '<a class="btn btn-outline" href="https://wa.me/918107301306?text=Namaste!" data-wa data-wa-en="Namaste! I want to enquire about Shri Maha Maya Hotel, Pallu." data-wa-hi="नमस्ते! मैं श्री महा माया होटल, पल्लू के बारे में पूछताछ करना चाहता/चाहती हूँ।" data-ga="click_whatsapp"><span data-icon="whatsapp"></span><span data-i18n="bar.wa">WhatsApp</span></a>'
     '<a class="btn btn-outline" href="mailto:shreemahamayahotel@gmail.com"><span data-icon="mail"></span>Email</a></div>'
     + tag("pg.c.h2b", "h2") + tag("pg.c.p2", "p") + '</section>'
     '<section class="contact" id="contact"><div class="container">' + form + '</div></section>'
     '<section class="container prose">' + tag("pg.c.h2c", "h2") + tag("pg.c.p3", "p") +
     tag("pg.c.h2d", "h2") + '</section><section class="faq"><div class="container">' + FAQ_HTML + '</div></section>' + CTA_BOOK)),
}

# ---------- head builder ----------
def build_head(pg, path):
    h = head
    url = BASE + "/" + path + "/"
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % pg["title"].replace("&", "&amp;"), h, count=1)
    h = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % pg["desc"], h, count=1)
    h = re.sub(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % url, h, count=1)
    h = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="%s">' % pg["title"].replace("&", "&amp;"), h, count=1)
    h = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="%s">' % pg["desc"], h, count=1)
    h = re.sub(r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="%s">' % url, h, count=1)
    h = re.sub(r'<meta name="twitter:title" content=".*?">', '<meta name="twitter:title" content="%s">' % pg["title"].replace("&", "&amp;"), h, count=1)
    h = re.sub(r'<meta name="twitter:description" content=".*?">', '<meta name="twitter:description" content="%s">' % pg["desc"], h, count=1)
    # subpage: hero preload hatao (hero image yahan nahi)
    h = re.sub(r'\s*<link rel="preload" as="image"[^>]*>', "", h, count=1)
    # asset paths root-relative
    h = h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    h = h.replace('href="images/', 'href="/images/').replace('href="manifest.webmanifest"', 'href="/manifest.webmanifest"')
    ld = [{"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": pg["crumbs_label"], "item": url}]}]
    if path == "contact":
        ld.append({"@type": "FAQPage", "@id": url + "#faq",
                   "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    h = h.replace("</head>", '  <script type="application/ld+json">\n  ' +
                  json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False, indent=2) +
                  '\n  </script>\n</head>')
    return h

def fix_nav(block, path):
    """subpage nav: anchors -> page links; self par aria-current"""
    repl = {"#rooms": "/rooms/", "#dining": "/restaurant/", "#contact": "/contact/", "#amenities": "/location/"}
    for a, b in repl.items():
        block = block.replace('href="%s"' % a, 'href="%s"' % b)
    block = block.replace('href="#home"', 'href="/"')
    block = block.replace('href="#about"', 'href="/#about"')
    block = block.replace('href="#gallery"', 'href="/#gallery"')
    block = block.replace('href="/%s/"' % path, 'href="/%s/" aria-current="page"' % path)
    return block

def fix_footer(bl):
    for a, b in FOOT_REPL.items():
        bl = bl.replace('href="%s"' % a, 'href="%s"' % b)
    return bl

# ---------- write pages ----------
tail_sub = tail.replace('href="#contact" class="book"', 'href="/contact/#booking-form" class="book"')
tail_sub = tail_sub.replace('src="assets/', 'src="/assets/')
FOOT_REPL = {"#about": "/#about", "#rooms": "/rooms/", "#dining": "/restaurant/", "#amenities": "/location/", "#gallery": "/#gallery", "#contact": "/contact/"}
for path, pg in PAGES.items():
    out = build_head(pg, path) + "\n<body>\n" + fix_nav(header, path) + "\n" + fix_nav(mmenu, path) + \
          '\n<main id="top">\n' + pg["body"] + "\n</main>\n" + fix_footer(footer) + "\n" + tail_sub
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", pg["body"])).split())
    print("✓ /%s/  (~%d words body)" % (path, words))

# ---------- i18n into app.src.js ----------
app = os.path.join(ROOT, "assets/js/app.src.js")
src = open(app, encoding="utf-8").read()
block = "  /* PAGE-I18N-START (build-pages.py) */\n" + "".join(
    '  "%s": { en: %s, hi: %s },\n' % (k, json.dumps(v["en"], ensure_ascii=False), json.dumps(v["hi"], ensure_ascii=False))
    for k, v in I.items()) + "  /* PAGE-I18N-END */\n"
if "PAGE-I18N-START" in src:
    src = re.sub(r"  /\* PAGE-I18N-START.*?PAGE-I18N-END \*/\n", block, src, flags=re.S)
else:
    src = src.replace('  "footer.pg4":', block + '  "footer.pg4":', 1)
open(app, "w", encoding="utf-8").write(src)
print("✓ i18n keys:", len(I))
