import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

class BotLogic:
    def __init__(self):
        self.locations = self._load_locations()
        self.faq = self._load_faq()
        self.greetings = self._load_greetings()
        self.sessions: Dict[str, List[str]] = {}
    
    def _load_locations(self) -> Dict[str, Dict[str, float]]:
        return {
            "neu_main": {"lat": 35.226735, "lng": 33.326385, "name": "Near East University Main Campus"},
            "rectorate": {"lat": 35.2271, "lng": 33.3267, "name": "Rectorate Building (Administration)"},
            "international_office": {"lat": 35.2271, "lng": 33.3267, "name": "International Office - Rectorate Ground Floor"},
            "student_affairs": {"lat": 35.2271, "lng": 33.3267, "name": "Student Affairs Office - Rectorate"},
            "near_east_bank_main": {"lat": 35.2269, "lng": 33.3265, "name": "Near East Bank - Main Branch"},
            "near_east_bank_dorms": {"lat": 35.2255, "lng": 33.3275, "name": "Near East Bank - Dormitory Branch"},
            "cis_faculty": {"lat": 35.2268, "lng": 33.3270, "name": "Faculty of Computer and Information Systems"},
            "engineering_faculty": {"lat": 35.2274, "lng": 33.3272, "name": "Faculty of Engineering"},
            "medicine_faculty": {"lat": 35.2280, "lng": 33.3260, "name": "Faculty of Medicine"},
            "law_faculty": {"lat": 35.2265, "lng": 33.3268, "name": "Faculty of Law"},
            "architecture_faculty": {"lat": 35.2270, "lng": 33.3275, "name": "Faculty of Architecture"},
            "grand_library": {"lat": 35.2272, "lng": 33.3268, "name": "Grand Library (Büyük Kütüphane)"},
            "neu_hospital": {"lat": 35.2285, "lng": 33.3258, "name": "Near East University Hospital"},
            "sports_complex": {"lat": 35.2260, "lng": 33.3280, "name": "Sports Complex"},
            "olympic_pool": {"lat": 35.2261, "lng": 33.3281, "name": "Olympic Swimming Pool"},
            "dormitories": {"lat": 35.2253, "lng": 33.3278, "name": "Student Dormitories Area"},
        }
    
    def _get_map_link(self, location_key: str) -> str:
        if location_key not in self.locations:
            location_key = "neu_main"
        
        loc = self.locations[location_key]
        lat, lng = loc["lat"], loc["lng"]
        name = loc["name"]
        
        if location_key == "neu_main":
            maps_url = "https://www.google.com/maps/place/Near+East+University/"
        else:
            maps_url = f"https://www.google.com/maps?q={lat},{lng}"
        
        return f"🗺️ <strong><a href='{maps_url}' target='_blank'>📌 View {name} on Google Maps (Exact Location)</a></strong>"

    def _load_faq(self) -> Dict[str, str]:
        return {
            # About NEU & History
            "what is near east university": "Near East University (NEU) is a leading private university located in North Cyprus, established in 1988. We offer world-class education with modern facilities, international programs, and a diverse student community from over 100 countries.",
            "about neu": "Near East University is a prestigious institution offering undergraduate and graduate programs in various fields including Engineering, Medicine, Law, Architecture, Business, and more. We're known for our innovative teaching methods and state-of-the-art research facilities.",
            "where is neu located": "Near East University is located in Nicosia (Lefkoşa), the capital of North Cyprus. Our main campus is situated on Near East Boulevard.",
            "is neu multicultural": "Yes! NEU has students from over 100 countries, making it a truly multicultural and diverse learning environment.",
            "who is suat gunsel": "Dr. Suat İrfan Günsel is the founder and chairman of Near East University. He established NEU in 1988 with a vision to create a world-class educational institution. Under his leadership, NEU has grown into one of the largest and most prestigious universities in the region, serving over 35,000 students from 100+ countries.",
            "suat gunsel": "Dr. Suat İrfan Günsel is the visionary founder and chairman of Near East University. Since establishing NEU in 1988, he has been dedicated to providing quality education and has built NEU into a leading international university with state-of-the-art facilities including a modern hospital, research centers, and comprehensive campus infrastructure.",
            "who founded neu": "Near East University was founded in 1988 by Dr. Suat İrfan Günsel, a visionary entrepreneur and education advocate. His commitment to excellence in education has transformed NEU into one of the region's premier universities.",
            "founder of near east university": "Dr. Suat İrfan Günsel founded Near East University in 1988. He remains the chairman of the university and continues to guide its mission of providing world-class education to international students.",
            "when was neu founded": "Near East University was founded in 1988 by Dr. Suat İrfan Günsel in Nicosia, North Cyprus.",
            "neu history": "Near East University was established in 1988 by Dr. Suat İrfan Günsel. Starting with just a few faculties, NEU has grown exponentially over the past 35+ years to become one of the largest universities in Cyprus, now offering 16 faculties, a teaching hospital, research centers, and serving over 35,000 students from more than 100 countries worldwide.",
            "history of neu": "Founded in 1988 by Dr. Suat İrfan Günsel, Near East University began as a small institution with a big vision. Over three decades, it has evolved into a comprehensive university with cutting-edge facilities, including the Near East University Hospital, Grand Library, state-of-the-art laboratories, and extensive sports complexes. NEU is now recognized internationally for its academic excellence and multicultural environment.",
            "how do i register": "You can register at Near East University by logging into the Uzebim portal at https://uzebim.neu.edu.tr/ and completing the steps shown there. If it's your first time, the International Office or your faculty staff will guide you.",
            "what do i need to complete registration": "You need your passport, high school diploma, transcript, acceptance letter, and tuition payment receipt.",
            "how do i register for courses": "You can register for courses through the Genius portal at https://register.neu.edu.tr under 'Course Registration.'",
            "course registration deadline": "The course registration deadline is usually during the second week of the semester. For fall, it's typically around October 10th.",
            "how do i get username and password": "After full registration and payment, NEU emails your Uzebim and student email login details to your personal email.",
            "how to change uzebim password": "Use the 'Forgot Password' option on the Uzebim login page or ask the International Office for help.",
            "how to access uzebim": "Visit https://uzebim.neu.edu.tr and log in using your student email and password.",
            "how to see payments": "Open the Genius portal and check the 'Financial' section to see your payment history and remaining balance.",
            "how to pay school fees": "Payments can be made at Near East Bank, through POS at the International Office, or via international/local bank transfer.",
            "reset student portal password": "Use the 'Forgot Password' option on the portal, or visit the International Office if you cannot access your email.",
            "how to access student email": "NEU sends your student email and password to your registered personal email once you complete registration.",
            "update contact information": "Go to your Uzebim profile and update your phone number, email, or address.",
            "what if i miss registration": "Visit the International Office immediately. They may allow late registration depending on the deadline.",
            "see registered courses": "Your registered courses appear in Uzebim under 'Course List' and in Genius under 'My Courses.'",
            "how to get transcript": "Request one at the Student Affairs Office or email student.affairs@neu.edu.tr for a digital copy.",
            "where to find course outline": "Course outlines are uploaded by lecturers on Uzebim under each course page.",
            "who is my academic advisor": "Your advisor's name and contact info are listed in Uzebim under 'Advisor Information.'",
            "how to find class schedule": "Check the Weekly Schedule section on Uzebim. Faculty boards also post updated timetables.",
            "how to contact lecturer": "Their university email is listed under the course page on Uzebim. Some also use Microsoft Teams.",
            "what happens if i fail course": "You must retake the course next semester or during summer school.",
            "how grading system works": "NEU uses letter grades (A–F). Each letter has grade points that calculate your GPA.",
            "how many credits per course": "Most courses are 3 credits; labs are usually 1 credit.",
            "is attendance required": "Yes. Missing more than 20–30% of classes may result in an NG (No Grade).",
            "when are midterm exams": "Midterms are around Week 8. Final exams take place during the last two weeks of the semester.",
            "are there lab exams": "Yes. Some courses with practical components have separate lab exams. Your lecturer will announce the dates.",
            "how to change major": "Submit a Major Change Petition to Student Affairs. Approval depends on GPA and faculty requirements.",
            "can i apply for scholarship": "Yes. Scholarships are usually applied during admission, but some faculties allow GPA-based reassessment.",
            "what if i lose scholarship": "If your GPA falls below the required level, the scholarship may be reduced or removed until your performance improves.",
            "how to take academic leave": "Submit a Leave Request Form to Student Affairs with a valid reason (health, financial issues, etc.).",
            "how to appeal grade": "Fill out the Grade Review Form within one week of the grade being announced.",
            "how to check exam results": "Results appear in Uzebim under each course once the lecturer uploads them.",
            "how is gpa calculated": "GPA is calculated by multiplying credit hours by grade points, summing them all, and dividing by total credits taken.",
            "what is summer school": "Summer school is an optional session from June–July where students take extra or repeated courses.",
            "how to transfer credits": "Submit your transcript and course descriptions to the faculty secretary for evaluation and approval.",
            "how many faculties": "NEU has <strong>16 faculties</strong> offering diverse programs: Engineering, Medicine, Dentistry, Pharmacy, Law, Architecture, Fine Arts, Economics & Administrative Sciences, Arts & Sciences, Communication, Education, Maritime Studies, Nursing, Health Sciences, Veterinary Medicine, and Aviation & Space Sciences.",
            "best faculties": "NEU's top-ranked faculties include:<br>• <strong>Faculty of Engineering</strong> - Computer Science, Civil, Electrical Engineering<br>• <strong>Faculty of Medicine</strong> - Highly acclaimed medical program<br>• <strong>Faculty of Architecture</strong> - Award-winning design programs<br>• <strong>Faculty of Business & Economics</strong> - Internationally accredited<br>• <strong>Faculty of Law</strong> - Comprehensive legal education",
            "dean of cis": "👩‍🏫 Prof. Dr. Nadire Cavus<br>Dean, Faculty of Computer and Information Systems<br><br><strong>Expertise:</strong><br>Prof. Dr. Nadire Cavus is a renowned expert in educational technology, e-learning systems, and mobile learning platforms.<br><br><strong>Contact Information:</strong><br>📧 nadire.cavus@neu.edu.tr<br>🏫 CIS Faculty Building, NEU Campus<br><br>🔗 <a href='https://cis.neu.edu.tr/' target='_blank'>Visit CIS Faculty Website</a>",
            "who is nadire cavus": "👩‍🏫 Prof. Dr. Nadire Cavus<br>Dean, Faculty of Computer and Information Systems<br><br><strong>Professional Background:</strong><br>Prof. Dr. Nadire Cavus is a distinguished academic leader and researcher at Near East University. She specializes in:<br>• Educational Technology<br>• E-Learning Systems<br>• Mobile Learning<br>• Computer Science Education<br><br><strong>Contact Information:</strong><br>📧 nadire.cavus@neu.edu.tr<br>🏢 CIS Faculty Building, NEU Campus<br><br>🔗 <a href='https://cis.neu.edu.tr/' target='_blank'>View Full Academic Profile</a>",
            "head of cis faculty": "👩‍🏫 CIS Faculty Leadership<br><strong>Dean:</strong> Prof. Dr. Nadire Cavus<br><br>Prof. Dr. Nadire Cavus leads the Faculty of Computer and Information Systems and oversees all academic programs, research initiatives, and faculty operations.<br><br><strong>Contact:</strong><br>📧 nadire.cavus@neu.edu.tr<br>🏫 CIS Faculty Building<br><br>🔗 <a href='https://cis.neu.edu.tr/' target='_blank'>CIS Faculty Website</a>",
            "cis dean": "👩‍🏫 Prof. Dr. Nadire Cavus<br>Dean, Computer and Information Systems Faculty<br><br><strong>Contact Information:</strong><br>📧 nadire.cavus@neu.edu.tr<br>🏫 CIS Faculty Building<br><br>🔗 <a href='https://cis.neu.edu.tr/' target='_blank'>Faculty Website</a>",
            "faculty deans": "Each of NEU's 16 faculties has a dean. Some key deans include:<br><br>• <strong>CIS Faculty:</strong> Prof. Dr. Nadire Cavus<br>• <strong>Engineering Faculty:</strong> Contact the faculty office<br>• <strong>Medicine Faculty:</strong> Contact the faculty office<br>• <strong>Law Faculty:</strong> Contact the faculty office<br><br>For complete dean contact information, visit: <a href='https://neu.edu.tr/akademik/fakulteler/' target='_blank'>NEU Faculties Page</a>",
            "how to contact faculty dean": "Each faculty dean has an office in their respective faculty building. You can:<br>1. Email them directly (format: firstname.lastname@neu.edu.tr)<br>2. Visit the faculty secretary to schedule an appointment<br>3. Check the faculty website for specific contact details<br><br>Example: CIS Dean Prof. Dr. Nadire Cavus - nadire.cavus@neu.edu.tr",
            "faculty leadership": "NEU's faculties are led by experienced deans and academic leadership teams. Each faculty has:<br>• <strong>Dean</strong> - Overall faculty head<br>• <strong>Vice Deans</strong> - Support the dean<br>• <strong>Department Heads</strong> - Lead individual departments<br><br>Visit <a href='https://neu.edu.tr/akademik/fakulteler/' target='_blank'>NEU Faculties</a> for complete leadership information.",
            "where is cis faculty": f"📍 <strong>Faculty of Computer and Information Systems (CIS)</strong><br><br>The CIS Faculty building is located in the academic zone of the main NEU campus.<br><br>{self._get_map_link('cis_faculty')}<br><br>🚶 <strong>Directions:</strong> From the main entrance, follow signs to the academic buildings zone. Look for 'CIS' or 'Bilgisayar ve Bilişim Sistemleri Fakültesi' signs.<br><br>💡 You can also ask security or students for 'CIS Faculty' directions.",
            "cis faculty location": f"📍 <strong>CIS Faculty Building Location</strong><br><br>{self._get_map_link('cis_faculty')}<br><br>The CIS Faculty is on the main NEU campus in the academic zone. The faculty office and Dean's office (Prof. Dr. Nadire Cavus) are inside the CIS building.<br><br>🚶 From main entrance → Follow academic buildings signs → Look for 'CIS Faculty'",
            "engineering faculty location": f"📍 <strong>Faculty of Engineering</strong><br><br>The Faculty of Engineering is one of the largest buildings on campus, located in the central academic area.<br><br>{self._get_map_link('engineering_faculty')}<br><br>🚶 Look for the Engineering Faculty signs or ask any student for directions to 'Mühendislik Fakültesi'.",
            "medicine faculty location": f"📍 <strong>Faculty of Medicine</strong><br><br>The Faculty of Medicine is located near the NEU Hospital. It's clearly marked and easy to find.<br><br>{self._get_map_link('medicine_faculty')}<br><br>🏥 Located adjacent to NEU Hospital building.",
            "where is law faculty": f"📍 <strong>Faculty of Law</strong><br><br>{self._get_map_link('law_faculty')}<br><br>The Faculty of Law building is in the academic zone of the main campus. Check the map link above for precise directions.",
            "faculty building directions": f"All faculty buildings are located on the main NEU campus.<br><br>{self._get_map_link('neu_main')}<br><br>Or ask security/students for specific faculty locations.",
            "where is north cyprus": "North Cyprus is the Turkish-speaking northern part of the island of Cyprus, located in the Eastern Mediterranean.",
            "difference between north and south cyprus": "North Cyprus (TRNC) is Turkish-administered and uses Turkish Lira. South Cyprus uses the Euro and is under EU administration.",
            "is neu one campus": "NEU has one main campus with all faculties, dorms, labs, and facilities inside.",
            "near east university map": "Here is the map location for Near East University: https://www.google.com/maps/place/Near+East+University/",
            "show me neu on map": "You can view NEU on Google Maps here: https://www.google.com/maps/place/Near+East+University/",
            "where is near east university located": "Near East University is located in Nicosia, North Cyprus. Map: https://www.google.com/maps/place/Near+East+University/",
            "where is campus map": f"🗺️ NEU Campus Map<br><br>{self._get_map_link('neu_main')}<br><br>📍 Near East Boulevard, Nicosia, North Cyprus<br><br>💡 Printed maps available at International Office and faculty entrances",
            "campus map": f"🗺️ NEU Campus Map<br><br>{self._get_map_link('neu_main')}<br><br>📍 Near East University<br>Near East Boulevard (Yakın Doğu Bulvarı)<br>Nicosia, North Cyprus",
            "show me on map": f"🗺️ Near East University Campus Map<br><br>{self._get_map_link('neu_main')}<br><br>📍 Near East Boulevard, Nicosia, North Cyprus<br>📌 GPS: 35.226735, 33.326385",
            "show map": f"🗺️ NEU Campus Map<br><br>{self._get_map_link('neu_main')}<br><br>📍 Near East Boulevard, Nicosia, North Cyprus",
            "neu location": f"📍 NEU Location<br><br>{self._get_map_link('neu_main')}<br><br>Near East Boulevard, Nicosia (Lefkoşa), North Cyprus<br>📌 GPS: 35.226735, 33.326385",
            "directions to neu": f"🧭 Get Directions to NEU<br><br>{self._get_map_link('neu_main')}<br><br>📍 Main Entrance: Near East Boulevard (Yakın Doğu Bulvarı)<br>🚗 Click the map link above for turn-by-turn directions",
            "where is administration building": f"📍 <strong>Administration Building (Rectorate)</strong><br><br>The main administration building (Rectorate) is located near the flag area at the center of campus, next to the Grand Library.<br><br>{self._get_map_link('rectorate')}<br><br>🏛️ This building houses: International Office, Student Affairs, and main administrative offices.",
            "where is student affairs office": f"📍 <strong>Student Affairs Office</strong><br><br>Student Affairs Office is inside the Rectorate building on the ground floor.<br><br>{self._get_map_link('student_affairs')}",
            "how to get student id": "After completing registration and uploading your photo, Student Affairs prints your ID for pickup.",
            "banks on campus": f"🏬 Banking Services on Campus<br>NEU campus has 2 Near East Bank branches for your convenience<br><br><strong>1️⃣ Main Branch</strong> - Central Campus<br>📍 Located next to Rectorate Building<br>{self._get_map_link('near_east_bank_main')}<br>✓ Full banking services: Account opening, transfers, currency exchange<br>✓ 24/7 ATM<br><br><strong>2️⃣ Dormitory Branch</strong><br>📍 Near student dormitory area<br>{self._get_map_link('near_east_bank_dorms')}<br>✓ ATM and basic banking services<br><br>🌐 <a href='https://www.neareastbank.com/' target='_blank'>neareastbank.com</a>",
            "near east bank location": f"📍 Near East Bank Locations<br><br><strong>Main Branch</strong><br>Central campus, next to Rectorate Building<br>{self._get_map_link('near_east_bank_main')}<br><br><strong>Dormitory Branch</strong><br>Near student housing area<br>{self._get_map_link('near_east_bank_dorms')}<br><br>💡 Both branches offer 24/7 ATM access",
            "where is near east bank": f"🏬 Near East Bank - Main Branch<br>Central campus area, adjacent to Rectorate Building<br><br>{self._get_map_link('near_east_bank_main')}<br><br><strong>Services Available:</strong><br>✓ Student account opening<br>✓ International money transfers<br>✓ Currency exchange<br>✓ 24/7 ATM access<br><br>🌐 <a href='https://www.neareastbank.com/' target='_blank'>Visit neareastbank.com</a><br><br>💡 <em>A second branch is available near the dormitories.</em>",
            "bank services on campus": f"Near East Bank on campus offers: account opening for students, international money transfers, currency exchange, ATM withdrawals, and general banking services.<br><br>{self._get_map_link('near_east_bank_main')}<br><br>Visit the main branch near the Rectorate building.",
            "atm on campus": f"Yes, there are multiple ATMs on campus. The main ones are at both Near East Bank branches:<br><br>📍 <strong>Main Branch (Rectorate area)</strong><br>{self._get_map_link('near_east_bank_main')}<br><br>📍 <strong>Dormitory Branch</strong><br>{self._get_map_link('near_east_bank_dorms')}<br><br>Additional ATMs are located near the library and student center.",  
            "international office hours": "Monday to Friday, 08:00–16:00 (closed on weekends).",
            "how to contact international office": f"📧 Email: international@neu.edu.tr<br>📞 Phone: +90 392 680 20 00<br>📍 Location: Rectorate Building, Ground Floor<br><br>{self._get_map_link('international_office')}<br><br>Visit during office hours (Mon-Fri, 08:00-16:00) for registration, visa, and student support.",
            "where is international office": f"📍 <strong>International Office Location</strong><br><br>The International Office is located in the <strong>Rectorate Building, Ground Floor</strong>, near the center of campus (flag area).<br><br>{self._get_map_link('international_office')}<br><br>🚶 <strong>How to find it:</strong> Look for signs pointing to 'International Office' or 'Uluslararası Ofis' near the central flag area.<br><br>🕒 Office Hours: Monday-Friday, 08:00-16:00<br>📧 international@neu.edu.tr",
            "international office location": f"📍 <strong>International Office - Rectorate Building, Ground Floor</strong><br><br>{self._get_map_link('international_office')}<br><br>Located in the central campus area near the flag and administration buildings.<br><br>🕒 Hours: Monday to Friday, 08:00–16:00<br>📧 international@neu.edu.tr<br>📞 +90 392 680 20 00",
            "directions to international office": f"From the main campus entrance, head towards the central flag area. The International Office is on the ground floor of the Rectorate Building (main administration building).<br><br>{self._get_map_link('international_office')}<br><br>Ask any student or security for 'Uluslararası Ofis' if you need help finding it.",
            "neu general email": "info@neu.edu.tr",
            "who to contact for help": "International Office: international@neu.edu.tr<br>Student Affairs: student.affairs@neu.edu.tr<br>NEU Main Line: +90 392 680 20 00<br>Or visit your faculty secretary.",
            "transportation options": "Public buses, NEU shuttles, taxis, and private minibuses are the main transportation options.",
            "transportation cost": "Public bus fares range from 10–20 TL per ride depending on distance.",
            "are neu buses free": "Some NEU shuttles are free for students, especially those running within campus.",
            "bus stops on campus": "Main bus stops are near the dormitories, the library, and the hospital area.",
            "what is adakart": "AdaKart is a rechargeable travel card used for public buses across North Cyprus.",
            "how to top up adakart": "You can top up at local markets, kiosks, and designated refill points around Nicosia.",
            "parking on campus": "Yes, students can park in designated areas, especially near faculties and dorms.",
            "library opening hours": "The Grand Library is open 24/7 during the academic semester.",
            "how to borrow books": "Present your student ID at the library desk or use the self-service borrowing machine.",
            "where to study on campus": "Library reading rooms, faculty study lounges, and open seating areas across campus.",
            "cafeterias on campus": "Yes. Dozens of cafeterias and restaurants are located around the main campus.",
            "gym on campus": "Yes. NEU boasts one of the largest sports complexes in Cyprus, with gym facilities available.",
            "swimming pool": "Yes, NEU has an Olympic-sized indoor pool accessible to students.",
            "sports at neu": "Basketball, football, volleyball, tennis, swimming, fitness training, and many more.",
            "how to join club": "Visit the Student Clubs Office or register during club sign-up events at the start of each semester.",
            "where are computer labs": "Computer labs are located in the Engineering Faculty, Library basement, and various departmental buildings.",
            "are computer labs free": "Yes. Labs are free for students as long as no class is in session.",
            "printing on campus": "Yes. The library and computer labs offer printing services for a small fee.",
            "how to apply for dorm": "Apply online through the NEU Dormitory website or visit the Dormitory Office on campus.",
            "types of dorms": "NEU offers male and female dorms, single rooms, double rooms, and apartment-style options.",
            "what is included in dorm fees": "Water, internet, furniture, cleaning, and security are included; electricity may vary by dorm.",
            "do dorms have wifi": "Yes. All NEU dormitories have Wi-Fi coverage.",
            "are dorms separated by gender": "Yes. Male and female students live in separate dorm buildings.",
            "do dorms have curfew": "Some dorms have entry restrictions; premium dorms usually have 24/7 access.",
            "can i cook in dorm": "Some dorms allow cooking in shared kitchens; check your dorm's rules.",
            "dorm cleaning": "Dorm cleaning typically occurs once or twice per week, depending on the building.",
            "dorm laundry": "Yes. Laundry rooms with washing machines and dryers are available.",
            "how to change dorm room": "Submit a request to the Dormitory Office; changes depend on availability.",
            "dorm security": "Yes. Security is available 24/7 at all NEU dormitories.",
            "medical emergency": "Call 112 or go directly to Near East University Hospital located on campus.",
            "does neu have hospital": "Yes. NEU Hospital is one of the top hospitals in North Cyprus and is located inside the campus.",
            "are medical services free": "Emergency services are free, but other treatments may require payment or insurance coverage.",
            "pharmacy on campus": "There are pharmacies near the hospital and at the university entrance.",
            "is north cyprus safe": "Yes. North Cyprus is known for being peaceful and has a low crime rate, especially around universities.",
            "campus security number": "NEU Security can be reached at +90 392 680 20 00 (ext. security).",
            "how to open bank account": "Visit Near East Bank with your passport, student certificate, and phone number.",
            "which bank to use": "Near East Bank is the most convenient because it has branches on campus.",
            "atm on campus": "Yes. Several ATMs (Near East Bank, İş Bankası, Ziraat, Garanti) are located near the library and dorms.",
            "cost of living": "Approximately 6,000–9,000 TL monthly depending on lifestyle (food, transport, utilities).",
            "currency in north cyprus": "Turkish Lira (TL) is the official currency, but Euros and Pounds are accepted in some places.",
            "do i need visa": "Students receive a temporary entry visa on arrival and must complete a residence permit after registration.",
            "how to apply for residence permit": "Apply through the 'İkamet' online system after completing your university registration and medical tests.",
            "medical tests required": "Blood test and chest X-ray are usually required before placing your residence permit application.",
            "residence permit processing time": "Normally 2–4 weeks after submitting all documents.",
            "residence permit renewal": "Log in to the İkamet portal, update your documents, and pay the renewal fee.",
            "health insurance required": "Yes. Student health insurance is mandatory and part of your residence permit requirements.",
            "wifi on campus": "Yes. NEU provides campus-wide Wi-Fi for all students.",
            "wifi password": "Log in using your student credentials. Reset through Uzebim if forgotten.",
            "what is uzebim": "Uzebim is NEU's online academic system for accessing lessons, exams, materials, and announcements.",
            "how to submit assignments": "Assignments are uploaded to Uzebim under the specific course or submitted via Microsoft Teams if required.",
            "weather in north cyprus": "Summers are hot (30–40°C), while winters are mild (10–18°C).",
            "what clothes to bring": "Light clothes for summer, a jacket for winter, and comfortable walking shoes.",
            "beaches nearby": "Yes. Beaches in Kyrenia (Girne) are 20–30 minutes from NEU.",
            "shopping malls": "Yes. Nicosia has several malls including 1001 Airport Mall and CityMall.",
            "food cost": "Affordable. Meals cost around 80–200 TL depending on where you eat.",
            "local sim card": "Visit Turkcell or Telsim shops with your passport to buy a student SIM package.",
            "what can you do": "I'm the NEU Virtual Assistant! I can help you with:<br>• Information about NEU and our faculties<br>• Admissions and application process<br>• Campus facilities and services<br>• Tuition fees and scholarships<br>• Library hours and resources<br>• Registration and course information<br>• Dormitories and campus life<br>• Visa and residence permits<br>• And much more! Just ask me anything about Near East University!",
            "help": "I'm here to help! You can ask me about:<br>• University information<br>• Registration & course enrollment<br>• Faculties and programs<br>• Admissions<br>• Campus life & facilities<br>• Fees and scholarships<br>• Dormitories<br>• Visa requirements<br>• Transportation<br>• And more! Try questions like 'How do I register?', 'Library hours?', or 'What is Uzebim?'",
            "thank you": "You're welcome! Is there anything else you'd like to know about Near East University?",
            "thanks": "Happy to help! Feel free to ask if you have more questions about NEU.",
            "nice": "Thank you! I'm glad I could help. Do you have any other questions about Near East University?",
            "ok": "Great! If you have any more questions about NEU, I'm here to help!",
            "okay": "Perfect! Let me know if you need any more information about Near East University.",
            "good": "Wonderful! Is there anything else about NEU you'd like to know?",
        }

    def _load_greetings(self) -> List[str]:
        return [
            "Hello! I'm the NEU Virtual Assistant. How can I help you today?",
            "Hi there! Welcome to Near East University. What can I assist you with?",
            "Greetings! I'm here to help with any questions about NEU. What would you like to know?",
        ]

    def _is_greeting(self, message: str) -> bool:
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        message_lower = message.lower().strip()
        return any(message_lower.startswith(greet) or message_lower == greet for greet in greetings)

    def _is_acknowledgment(self, message: str) -> bool:
        acknowledgments = ["nice", "ok", "okay", "good", "great", "cool", "thanks", "thank you", "awesome", "perfect"]
        message_lower = message.lower().strip()
        return message_lower in acknowledgments or any(message_lower == ack for ack in acknowledgments)

    def _find_best_match(self, message: str) -> Optional[str]:
        message_lower = message.lower().strip()

        # First try exact match
        if message_lower in self.faq:
            return self.faq[message_lower]

        # Try partial match with improved scoring
        best_match = None
        best_score = 0

        for faq_key, answer in self.faq.items():
            faq_words = set(faq_key.split())
            message_words = set(message_lower.split())

            # Calculate matching words
            matching_words = faq_words.intersection(message_words)

            # Skip if no matching words for single-word queries
            if len(matching_words) == 0:
                continue

            # For single-word messages, require at least 1 match
            # For multi-word messages, require at least 2 matches
            min_matches = 1 if len(message_words) <= 2 else 2
            if len(matching_words) < min_matches:
                continue

            # Calculate score based on:
            # 1. Number of matching words
            # 2. Percentage of FAQ words matched
            # 3. Specificity (prefer longer FAQ keys with good matches)
            match_count = len(matching_words)
            match_ratio = match_count / len(faq_words)
            specificity_bonus = len(faq_words) * 0.1

            score = match_count + (match_ratio * 5) + specificity_bonus

            # Bonus if FAQ key is fully contained in message
            if all(word in message_lower for word in faq_words):
                score += 10

            if score > best_score:
                best_score = score
                best_match = answer

        return best_match

    def _scrape_neu_website(self, query: str) -> Optional[str]:
        try:
            query_lower = query.lower()

            if any(word in query_lower for word in ['admission', 'apply', 'application', 'requirements', 'entry']):
                return self._scrape_admissions_page()
            
            if any(word in query_lower for word in ['dean', 'faculty', 'head', 'professor', 'department']):
                return self._scrape_faculty_info()
            
            if any(word in query_lower for word in ['tuition', 'fee', 'cost', 'payment', 'price']):
                return self._scrape_tuition_info()
            
            if any(word in query_lower for word in ['scholarship', 'discount', 'financial aid', 'bursary']):
                return self._scrape_scholarship_info()
            
            if any(word in query_lower for word in ['dormitory', 'dorm', 'accommodation', 'housing', 'residence']):
                return self._scrape_accommodation_info()
            
            if any(word in query_lower for word in ['international', 'foreign', 'visa', 'residence permit']):
                return self._scrape_international_info()

            neu_pages = {
                'about': 'https://neu.edu.tr/en/about-us/',
                'academics': 'https://neu.edu.tr/en/academic/',
                'faculties': 'https://neu.edu.tr/en/academic/faculties/',
                'student': 'https://neu.edu.tr/en/student/',
                'campus': 'https://neu.edu.tr/en/campus-life/',
            }

            page_to_scrape = None
            if any(word in query_lower for word in ['about', 'history', 'founded', 'established']):
                page_to_scrape = neu_pages['about']
            elif any(word in query_lower for word in ['academic', 'program', 'course', 'degree']):
                page_to_scrape = neu_pages['academics']
            elif any(word in query_lower for word in ['student', 'registration']):
                page_to_scrape = neu_pages['student']
            elif any(word in query_lower for word in ['campus', 'facility', 'library']):
                page_to_scrape = neu_pages['campus']

            if page_to_scrape:
                return self._fetch_page_content(page_to_scrape, query)

            return self._google_site_search(query)

        except Exception as e:
            return None

    def _scrape_faculty_info(self) -> str:
        return (
            "📚 <strong>Faculty Information</strong><br><br>"
            "For detailed information about faculty deans and leadership:<br><br>"
            "👉 <strong><a href='https://neu.edu.tr/en/academic/faculties/' target='_blank'>View All Faculties & Deans</a></strong><br><br>"
            "You can find:<br>"
            "• Complete list of all 16 faculties<br>"
            "• Dean information and contact details<br>"
            "• Department heads and academic staff<br>"
            "• Faculty office locations and hours"
        )
    
    def _scrape_admissions_page(self) -> str:
        return (
            "🎓 <strong>Admissions Information</strong><br><br>"
            "<strong>How to Apply:</strong><br>"
            "1. Visit the online application portal<br>"
            "2. Submit required documents (passport, diploma, transcript)<br>"
            "3. Pay application fee<br>"
            "4. Await acceptance letter<br><br>"
            "📋 <strong><a href='https://neu.edu.tr/en/prospective-students/admission-requirements/' target='_blank'>View Full Admission Requirements</a></strong><br><br>"
            "📧 Contact: admissions@neu.edu.tr<br>"
            "📞 Phone: +90 392 680 20 00<br><br>"
            "<strong>Application Periods:</strong><br>"
            "• Fall Semester: June - September<br>"
            "• Spring Semester: December - January"
        )
    
    def _scrape_tuition_info(self) -> str:
        return (
            "💰 <strong>Tuition & Fees Information</strong><br><br>"
            "Tuition fees vary by program and faculty:<br><br>"
            "📊 <strong><a href='https://neu.edu.tr/en/prospective-students/tuition-fees/' target='_blank'>View Current Tuition Fees</a></strong><br><br>"
            "<strong>Payment Options:</strong><br>"
            "• Full payment (discounts available)<br>"
            "• Installment plans<br>"
            "• Bank transfer<br>"
            "• Credit/Debit card at campus<br><br>"
            "💳 Payment Location: Near East Bank (Main Campus)<br>"
            "📧 Financial inquiries: finance@neu.edu.tr<br><br>"
            "<strong>Additional Costs:</strong><br>"
            "• Registration fees<br>"
            "• Health insurance<br>"
            "• Accommodation (if applicable)<br>"
            "• Student card and materials"
        )
    
    def _scrape_scholarship_info(self) -> str:
        return (
            "🎓 <strong>Scholarship Opportunities</strong><br><br>"
            "NEU offers various scholarship programs:<br><br>"
            "<strong>Scholarship Types:</strong><br>"
            "• Academic Excellence Scholarships (25-100%)<br>"
            "• Sports Scholarships<br>"
            "• Sibling Discounts<br>"
            "• Early Registration Discounts<br>"
            "• Country-specific scholarships<br><br>"
            "📋 <strong><a href='https://neu.edu.tr/en/prospective-students/scholarships/' target='_blank'>View All Scholarship Options</a></strong><br><br>"
            "<strong>How to Apply:</strong><br>"
            "Scholarships are typically evaluated during admission based on:<br>"
            "• High school GPA<br>"
            "• Entrance exam scores<br>"
            "• Special talents or achievements<br><br>"
            "📧 Contact: scholarships@neu.edu.tr<br>"
            "💡 Tip: Apply early to increase scholarship chances!"
        )
    
    def _scrape_accommodation_info(self) -> str:
        return (
            "🏠 <strong>Accommodation at NEU</strong><br><br>"
            "<strong>On-Campus Dormitories:</strong><br>"
            "• Male and female dormitories<br>"
            "• Single, double, and triple rooms<br>"
            "• All rooms furnished with beds, desks, wardrobes<br>"
            "• 24/7 security and supervision<br>"
            "• WiFi included<br><br>"
            "📍 <strong><a href='https://neu.edu.tr/en/campus-life/accommodation/' target='_blank'>View Dormitory Details & Prices</a></strong><br><br>"
            "<strong>Facilities:</strong><br>"
            "• Common rooms and study areas<br>"
            "• Laundry services<br>"
            "• Cafeteria and dining halls<br>"
            "• Recreation areas<br><br>"
            "📧 Dormitory Office: dormitory@neu.edu.tr<br>"
            "📞 Phone: +90 392 680 20 00 (ext. 2500)<br><br>"
            "<strong>Off-Campus Options:</strong><br>"
            "• Private apartments near campus<br>"
            "• Shared housing with other students<br>"
            "• Contact Student Affairs for assistance"
        )
    
    def _scrape_international_info(self) -> str:
        return (
            "🌍 <strong>International Students Office</strong><br><br>"
            "<strong>We assist with:</strong><br>"
            "• Student visa applications<br>"
            "• Residence permit processing<br>"
            "• Equivalence certificates<br>"
            "• Orientation programs<br>"
            "• Integration support<br><br>"
            "📍 <strong>Location:</strong> Rectorate Building, Ground Floor<br>"
            "📧 Email: international@neu.edu.tr<br>"
            "📞 Phone: +90 392 680 20 00<br><br>"
            "🔗 <strong><a href='https://neu.edu.tr/en/international/' target='_blank'>Visit International Office Page</a></strong><br><br>"
            "<strong>Required Documents:</strong><br>"
            "• Valid passport<br>"
            "• Acceptance letter from NEU<br>"
            "• Health insurance<br>"
            "• Proof of financial support<br>"
            "• High school diploma & transcript<br><br>"
            "<strong>Office Hours:</strong><br>"
            "Monday - Friday: 9:00 AM - 5:00 PM<br><br>"
            "💡 Visit us during orientation week for complete guidance!"
        )


    def _fetch_page_content(self, url: str, query: str) -> Optional[str]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=8)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract main content paragraphs
                paragraphs = []
                for p in soup.find_all('p', limit=5):
                    text = p.get_text(strip=True)
                    if len(text) > 50:
                        paragraphs.append(text)

                if paragraphs:
                    content = "<br><br>".join(paragraphs[:2])
                    return (
                        f"Here's information from the NEU website:<br><br>"
                        f"{content}<br><br>"
                        f"📖 <strong><a href='{url}' target='_blank'>Read more on NEU website</a></strong>"
                    )

            return None
        except:
            return None

    def _google_site_search(self, query: str) -> Optional[str]:
        try:
            search_url = f"https://www.google.com/search?q=site:neu.edu.tr+{query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                links_found = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'neu.edu.tr' in href and '/url?q=' in href:
                        actual_url = href.split('/url?q=')[1].split('&')[0]
                        if actual_url not in links_found:
                            links_found.append(actual_url)
                        if len(links_found) >= 3:
                            break

                if links_found:
                    result = "🔍 <strong>I found these relevant pages on the NEU website:</strong><br><br>"
                    for i, url in enumerate(links_found, 1):
                        # Extract page title from URL
                        page_name = url.split('neu.edu.tr/')[-1].replace('-', ' ').replace('/', ' ').title()
                        result += f"{i}. <a href='{url}' target='_blank'>{page_name or 'NEU Information'}</a><br>"
                    result += "<br>Click the links above for detailed information."
                    return result

            return None
        except:
            return None

    def generate_response(self, message: str, session_id: str, language: str = "EN") -> str:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(message)

        message_cleaned = message.strip()
        msg_lower = message_cleaned.lower()

        if self._is_greeting(message_cleaned):
            return random.choice(self.greetings)

        if self._is_acknowledgment(message_cleaned):
            answer = self._find_best_match(message_cleaned)
            if answer:
                return answer
            return "You're welcome! Is there anything else you'd like to know about Near East University?" if language == "EN" else "Rica ederim! Near East Üniversitesi hakkında başka bilgi almak ister misiniz?"

        if "map" in msg_lower or "location" in msg_lower:
            return "Here is the map location for Near East University: https://www.google.com/maps/place/Near+East+University/" if language == "EN" else "Near East Üniversitesi harita konumu: https://www.google.com/maps/place/Near+East+University/"

        answer = self._find_best_match(message_cleaned)

        if answer:
            return answer

        scraped_result = self._scrape_neu_website(message_cleaned)
        if scraped_result:
            return scraped_result

        if language == "TR":
            return (
                "Bu konuda veritabanımda henüz özel bilgi yok, ancak size yardımcı olabilirim!<br><br>"
                "<strong>📚 Faydalı Kaynaklar:</strong><br>"
                "• <a href='https://neu.edu.tr' target='_blank'>NEU Resmi Web Sitesi</a><br>"
                "• <a href='https://www.google.com/maps?ll=35.226735,33.326385&z=15&t=m&hl=en&gl=ES&mapclient=embed&cid=13187758565112652345' target='_blank'>NEU Kampüs Haritası</a><br>"
                "• <a href='https://neu.edu.tr/akademik/fakulteler/' target='_blank'>Fakülteler & Dekanlar</a><br>"
                "• <a href='https://uzebim.neu.edu.tr' target='_blank'>Uzebim Portalı</a> (Öğrenci Sistemi)<br>"
                "• <a href='https://register.neu.edu.tr' target='_blank'>Genius Portalı</a> (Ders Kaydı)<br><br>"
                "<strong>📞 Direkt İletişim:</strong><br>"
                "• Uluslararası Ofis: international@neu.edu.tr<br>"
                "• Öğrenci İşleri: student.affairs@neu.edu.tr<br>"
                "• Ana Hat: +90 392 680 20 00<br><br>"
                "Şunlar hakkında soru sorabilirsiniz: kayıt, fakülteler, dekanlar, kampüs haritası, kütüphane, yurtlar, vize, kampüs tesisleri veya öğrenim ücreti."
            )
        
        return (
            "I don't have specific information about that in my database yet, but I can help you find it!<br><br>"
            "<strong>📚 Useful Resources:</strong><br>"
            "• <a href='https://neu.edu.tr' target='_blank'>NEU Official Website</a><br>"
            "• <a href='https://www.google.com/maps?ll=35.226735,33.326385&z=15&t=m&hl=en&gl=ES&mapclient=embed&cid=13187758565112652345' target='_blank'>NEU Campus Map</a><br>"
            "• <a href='https://neu.edu.tr/akademik/fakulteler/' target='_blank'>Faculties & Deans</a><br>"
            "• <a href='https://uzebim.neu.edu.tr' target='_blank'>Uzebim Portal</a> (Student System)<br>"
            "• <a href='https://register.neu.edu.tr' target='_blank'>Genius Portal</a> (Course Registration)<br><br>"
            "<strong>📞 Direct Contact:</strong><br>"
            "• International Office: international@neu.edu.tr<br>"
            "• Student Affairs: student.affairs@neu.edu.tr<br>"
            "• Main Line: +90 392 680 20 00<br><br>"
            "Try asking about: registration, faculties, deans, campus map, library, dormitories, visa, campus facilities, or tuition."
        )

    def get_session_history(self, session_id: str) -> List[str]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

bot = BotLogic()
