/* ============================================================
   श्री महा माया — असली मेनू (मालिक का मेनू · अपडेट 10-11-2026)
   ------------------------------------------------------------
   ▪ Price बदलना: सिर्फ "₹..." बदल दें
   ▪ नया item जोड़ना: किसी भी list में नई line लिखें (कोमा न भूलें)
   ▪ Item हटाना: उसकी पूरी line delete कर दें
   ▪ featured = बड़े photo-card में दिखेगा, list = नीचे की सूची में
   ▪ photo बदलनी हो तो "img:" वाली line बदलें; photo नहीं है तो
     img वाली line हटा दें (सुनहरा चिह्न दिखेगा)
   ▪ halfExtra = हाफ portion पर extra चार्ज (मालिक का फ़ैसला 10-11-2026):
       पनीर +₹20 · मसाला/दाल/चावल/स्पेशल/फास्ट फूड +₹10 · दही-रायता +₹5
     जिस टैब में halfExtra नहीं लिखा, वहाँ हाफ नहीं दिखता
   ▪ hit: true = माया की "सबसे हिट डिशेस" सूची में दिखेगा
   ============================================================ */
window.MENU = {
  /* ---------- टैब 1: पनीर आइटम (हाफ = आधा दाम + ₹20) ---------- */
  "tab-paneer": {
    title: { en: "Paneer Items", hi: "पनीर आइटम" },
    halfExtra: 20,
    featured: [
      {
        name: { en: "Kadhai Paneer", hi: "कड़ाही पनीर" },
        price: "₹250", badge: true, hit: true,
        img: "images/food/food-paneer.webp",
        desc: { en: "Paneer tossed with capsicum, onion and kadhai masala — spicy, rich and made to order.", hi: "शिमला मिर्च, प्याज़ और कड़ाही मसाले में पका पनीर — तीखा, भरपूर और ऑर्डर पर ताज़ा।" }
      },
      {
        name: { en: "Shahi Paneer", hi: "शाही पनीर" },
        price: "₹230", badge: true, hit: true,
        img: "images/food/food-shahi-paneer.webp",
        desc: { en: "Rich, creamy and mildly sweet — a royal favourite with soft paneer.", hi: "मलाईदार, हल्की मीठी और शाही — नरम पनीर के साथ।" }
      },
      {
        name: { en: "Kaju Curry", hi: "काजू करी" },
        price: "₹280", hit: true,
        img: "images/food/food-kaju-curry.webp",
        desc: { en: "A rich cashew-gravy special — smooth, fragrant and worth every bite.", hi: "काजू की भरपूर ग्रेवी — मख़मली, खुशबूदार और हर निवाले के लायक।" }
      }
    ],
    list: [
      { name: { en: "Malai Kofta", hi: "मलाई कोफ्ता" }, price: "₹250", img: "images/food/food-malai-kofta.webp", hit: true },
      { name: { en: "Paneer Bhurji", hi: "पनीर भुर्जी" }, price: "₹240", img: "images/food/food-paneer-bhurji.webp", hit: true },
      { name: { en: "Matar Paneer", hi: "मटर पनीर" }, price: "₹210" },
      { name: { en: "Palak Paneer", hi: "पालक पनीर" }, price: "₹190", hit: true },
      { name: { en: "Chhola Paneer", hi: "छोला पनीर" }, price: "₹190" },
      { name: { en: "Mix Veg Paneer", hi: "मिक्स वेज पनीर" }, price: "₹190", img: "images/food/food-mixveg-paneer.webp" }
    ]
  },

  /* ---------- टैब 2: मसाला आइटम (हाफ = आधा दाम + ₹10) ---------- */
  "tab-masala": {
    title: { en: "Masala Items", hi: "मसाला आइटम" },
    halfExtra: 10,
    featured: [
      {
        name: { en: "Aloo Chhola", hi: "आलू छोला" },
        price: "₹100", hit: true,
        img: "images/food/food-chole.webp",
        desc: { en: "Chickpeas and potatoes simmered in a hearty spiced gravy.", hi: "मसालेदार ग्रेवी में पके छोले और आलू।" }
      }
    ],
    list: [
      { name: { en: "Cheese Tomato", hi: "चीज़ टमाटर" }, price: "₹230", hit: true },
      { name: { en: "Shahi Gatta", hi: "शाही गट्टा" }, price: "₹180", hit: true },
      { name: { en: "Sev Malai", hi: "सेव मलाई" }, price: "₹180" },
      { name: { en: "Sev Tomato", hi: "सेव टमाटर" }, price: "₹120" },
      { name: { en: "Besan Gatta", hi: "बेसन गट्टा" }, price: "₹130" },
      { name: { en: "Aloo Gobhi", hi: "आलू गोभी" }, price: "₹120" },
      { name: { en: "Aloo Matar", hi: "आलू मटर" }, price: "₹100" },
      { name: { en: "Aloo Palak", hi: "आलू पालक" }, price: "₹120" },
      { name: { en: "Aloo Shimla", hi: "आलू शिमला मिर्च" }, price: "₹120" },
      { name: { en: "Aloo Jeera", hi: "आलू जीरा" }, price: "₹110" },
      { name: { en: "Masala Bhindi", hi: "मसाला भिण्डी" }, price: "₹140" },
      { name: { en: "Mix Veg", hi: "मिक्स वेज" }, price: "₹130" },
      { name: { en: "Dum Aloo", hi: "दम आलू" }, price: "₹150" },
      { name: { en: "Gobhi Matar", hi: "गोभी मटर" }, price: "₹120" },
      { name: { en: "Gajar Matar", hi: "गाजर मटर" }, price: "₹120" },
      { name: { en: "Masala Matar", hi: "मसाला मटर" }, price: "₹140" },
      { name: { en: "Chana Masala", hi: "चना मसाला" }, price: "₹110" },
      { name: { en: "Tinda Tomato", hi: "टिण्डा टमाटर" }, price: "₹110" },
      { name: { en: "Gwarfali Kakriya", hi: "ग्वारफली ककड़िया" }, price: "₹120" },
      { name: { en: "Kadhi", hi: "कढ़ी" }, price: "₹120", hit: true }
    ]
  },

  /* ---------- टैब 3: दाल (हाफ = आधा दाम + ₹10) ---------- */
  "tab-dal": {
    title: { en: "Dal", hi: "दाल" },
    halfExtra: 10,
    featured: [
      {
        name: { en: "Dal Fry", hi: "दाल फ्राई" },
        price: "₹100", hit: true,
        img: "images/food/food-daltadka.webp",
        desc: { en: "Yellow dal tempered with ghee, garlic, cumin and red chillies.", hi: "घी, लहसुन, जीरे और लाल मिर्च की तड़के वाली दाल।" }
      }
    ],
    list: [
      { name: { en: "Dal Makhani", hi: "दाल मक्खनी" }, price: "₹150", hit: true }
    ]
  },

  /* ---------- टैब 4: दही रायता (हाफ = आधा दाम + ₹5) ---------- */
  "tab-dahi": {
    title: { en: "Dahi & Raita", hi: "दही रायता" },
    halfExtra: 5,
    featured: [],
    list: [
      { name: { en: "Plain Dahi", hi: "प्लेन दही" }, price: "₹50" },
      { name: { en: "Dahi Fry", hi: "दही फ्राई" }, price: "₹70" },
      { name: { en: "Plain Raita", hi: "प्लेन रायता" }, price: "₹60" },
      { name: { en: "Veg Raita", hi: "वेज रायता" }, price: "₹90" }
    ]
  },

  /* ---------- टैब 5: रोटी (हाफ नहीं) ---------- */
  "tab-roti": {
    title: { en: "Roti", hi: "रोटी" },
    featured: [],
    list: [
      { name: { en: "Tandoori Roti", hi: "तंदूरी रोटी" }, price: "₹10" },
      { name: { en: "Tandoori Butter Roti", hi: "तंदूरी बटर रोटी" }, price: "₹12" },
      { name: { en: "Tawa Roti", hi: "तवा रोटी" }, price: "₹12" },
      { name: { en: "Tawa Butter Roti", hi: "तवा बटर रोटी" }, price: "₹14" },
      { name: { en: "Missi Roti", hi: "मिस्सी रोटी" }, price: "₹30" },
      { name: { en: "Onion Roti", hi: "प्याज़ रोटी" }, price: "₹40" }
    ]
  },

  /* ---------- टैब 6: चावल (हाफ = आधा दाम + ₹10) ---------- */
  "tab-rice": {
    title: { en: "Rice", hi: "चावल" },
    halfExtra: 10,
    featured: [],
    list: [
      { name: { en: "Jeera Rice", hi: "जीरा राइस" }, price: "₹100" },
      { name: { en: "Veg Pulao", hi: "वेज पुलाव" }, price: "₹120" },
      { name: { en: "Kheer", hi: "खीर" }, price: "₹120" },
      { name: { en: "Sweet Rice", hi: "मीठा चावल" }, price: "₹120" },
      { name: { en: "Namkeen Rice", hi: "नमकीन चावल" }, price: "₹80" }
    ]
  },

  /* ---------- टैब 7: महामाया स्पेशल (हाफ = आधा दाम + ₹10) ---------- */
  "tab-special": {
    title: { en: "Mahamaya Special", hi: "महामाया स्पेशल" },
    halfExtra: 10,
    featured: [
      {
        name: { en: "Thali", hi: "थाली" },
        price: "₹140", badge: true, hit: true,
        img: "images/food/food-thali.webp",
        desc: { en: "Dal, sabji, roti, dahi and salad — everything on one platter.", hi: "दाल, सब्ज़ी, रोटी, दही और सलाद — सब कुछ एक थाली में।" }
      }
    ],
    list: [
      { name: { en: "Lahsun Chutney", hi: "लहसून चटनी" }, price: "₹150", img: "images/food/food-lahsun-chutney.webp", hit: true },
      { name: { en: "Tomato Onion Chutney", hi: "टमाटर प्याज़ चटनी" }, price: "₹140" }
    ]
  },

  /* ---------- टैब 8: पेय पदार्थ (हाफ नहीं) ---------- */
  "tab-beverages": {
    title: { en: "Beverages", hi: "पेय पदार्थ" },
    featured: [
      {
        name: { en: "Sweet Lassi", hi: "लस्सी मीठी" },
        price: "₹50", hit: true,
        img: "images/food/food-lassi.webp",
        desc: { en: "Thick, chilled and topped with malai.", hi: "गाढ़ी, ठंडी, मलाईदार लस्सी।" }
      },
      {
        name: { en: "Tea (Chai)", hi: "चाय" },
        price: "₹15", hit: true,
        img: "images/food/food-chai.webp",
        desc: { en: "Strong, milky and made the highway way.", hi: "कड़क, मलाईदार — हाईवे वाली चाय।" }
      }
    ],
    list: [
      { name: { en: "Coffee", hi: "कॉफ़ी" }, price: "₹25" },
      { name: { en: "Milk", hi: "दूध" }, price: "₹30" },
      { name: { en: "Chhachh", hi: "छाछ" }, price: "₹20" },
      { name: { en: "Lemon Water", hi: "नींबू पानी" }, price: "₹30" }
    ]
  },

  /* ---------- टैब 9: सलाद स्पेशल (हाफ नहीं) ---------- */
  "tab-salad": {
    title: { en: "Salad Special", hi: "सलाद स्पेशल" },
    featured: [],
    list: [
      { name: { en: "Plain Salad", hi: "प्लेन सलाद" }, price: "₹40" },
      { name: { en: "Green Salad", hi: "ग्रीन सलाद" }, price: "₹60" }
    ]
  },

  /* ---------- टैब 10: परांठा (हाफ नहीं) ---------- */
  "tab-prantha": {
    title: { en: "Parantha", hi: "परांठा" },
    featured: [],
    list: [
      { name: { en: "Aloo Parantha", hi: "आलू परांठा" }, price: "₹70" },
      { name: { en: "Mix Veg Parantha", hi: "मिक्स वेज परांठा" }, price: "₹90" },
      { name: { en: "Paneer Parantha", hi: "पनीर परांठा" }, price: "₹110", hit: true }
    ]
  },

  /* ---------- टैब 11: फास्ट फूड (हाफ = आधा दाम + ₹10) ---------- */
  "tab-fastfood": {
    title: { en: "Fast Food", hi: "फास्ट फूड" },
    halfExtra: 10,
    featured: [
      {
        name: { en: "Onion Pakoda", hi: "प्याज़ पकौड़ा" },
        price: "₹150", hit: true,
        img: "images/food/food-pakora.webp",
        desc: { en: "Crisp onion fritters fried fresh — best with chutney and chai.", hi: "ताज़ा तली कुरकुरी प्याज़ की पकौड़ियाँ — चटनी और चाय के साथ सर्वोत्तम।" }
      }
    ],
    list: [
      { name: { en: "Paneer Fry", hi: "पनीर फ्राई" }, price: "₹120" },
      { name: { en: "Finger Chips", hi: "फिंगर चिप्स" }, price: "₹130" },
      { name: { en: "Peanut Masala", hi: "मसाला मूंगफली" }, price: "₹150" },
      { name: { en: "Chana Chat", hi: "चना चाट" }, price: "₹130" },
      { name: { en: "Paneer Pakoda", hi: "पनीर पकौड़ा" }, price: "₹190" },
      { name: { en: "Maggi", hi: "मैगी" }, price: "₹70" },
      { name: { en: "Masala Maggi", hi: "मसाला मैगी" }, price: "₹90" }
    ]
  },

  /* ---------- टैब 12: पापड़ (हाफ नहीं) ---------- */
  "tab-papad": {
    title: { en: "Papad", hi: "पापड़" },
    featured: [],
    list: [
      { name: { en: "Plain Papad", hi: "प्लेन पापड़" }, price: "₹30" },
      { name: { en: "Masala Papad", hi: "मसाला पापड़" }, price: "₹80" }
    ]
  }
};
