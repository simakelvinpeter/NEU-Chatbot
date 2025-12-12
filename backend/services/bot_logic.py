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
            "neu_main": {
                "lat": 35.226735, 
                "lng": 33.326385, 
                "name": "Near East University Main Campus",
                "share_link": "https://maps.app.goo.gl/itWcEscDtg79itd27"
            },
            "rectorate": {
                "lat": 35.2271, 
                "lng": 33.3267, 
                "name": "Rectorate Building (Administration)",
                "share_link": ""
            },
            "international_office": {
                "lat": 35.2271, 
                "lng": 33.3267, 
                "name": "International Office - Rectorate Ground Floor",
                "share_link": ""
            },
            "student_affairs": {
                "lat": 35.2271, 
                "lng": 33.3267, 
                "name": "Student Affairs Office - Rectorate",
                "share_link": ""
            },
            "near_east_bank_main": {
                "lat": 35.2269, 
                "lng": 33.3265, 
                "name": "Near East Bank - Main Branch",
                "share_link": ""
            },
            "near_east_bank_dorms": {
                "lat": 35.2255, 
                "lng": 33.3275, 
                "name": "Near East Bank - Dormitory Branch",
                "share_link": ""
            },
            "cis_faculty": {
                "lat": 35.2268, 
                "lng": 33.3270, 
                "name": "Faculty of Computer and Information Systems",
                "share_link": ""
            },
            "engineering_faculty": {
                "lat": 35.2274, 
                "lng": 33.3272, 
                "name": "Faculty of Engineering",
                "share_link": ""
            },
            "medicine_faculty": {
                "lat": 35.2280, 
                "lng": 33.3260, 
                "name": "Faculty of Medicine (TIP)",
                "share_link": "https://maps.app.goo.gl/SkmWGXdkfsv6A8PW9"
            },
            "law_faculty": {
                "lat": 35.2265, 
                "lng": 33.3268, 
                "name": "Faculty of Law",
                "share_link": ""
            },
            "architecture_faculty": {
                "lat": 35.2270, 
                "lng": 33.3275, 
                "name": "Faculty of Architecture",
                "share_link": ""
            },
            "health_sciences_faculty": {
                "lat": 35.2273, 
                "lng": 33.3264, 
                "name": "Faculty of Health Sciences (Saglik Bilimleri)",
                "share_link": "https://maps.app.goo.gl/AB2VRNV5xb4HjNTL8"
            },
            "pharmacy_faculty": {
                "lat": 35.2275, 
                "lng": 33.3269, 
                "name": "Faculty of Pharmacy",
                "share_link": "https://maps.app.goo.gl/qJqzFPTcdmoTZtDj9"
            },
            "grand_library": {
                "lat": 35.2272, 
                "lng": 33.3268, 
                "name": "Grand Library (Büyük Kütüphane)",
                "share_link": "https://maps.app.goo.gl/ogbEYWfhDra6WbF28"
            },
            "neu_hospital": {
                "lat": 35.2285, 
                "lng": 33.3258, 
                "name": "Near East University Grand Hospital",
                "share_link": "https://maps.app.goo.gl/sSWHALZPDFERokyT9"
            },
            "sports_complex": {
                "lat": 35.2260, 
                "lng": 33.3280, 
                "name": "Sports Complex",
                "share_link": ""
            },
            "sports_tower": {
                "lat": 35.2258, 
                "lng": 33.3282, 
                "name": "Sports Tower",
                "share_link": "https://maps.app.goo.gl/dK88dC1ybnKw6BoA8"
            },
            "olympic_pool": {
                "lat": 35.2261, 
                "lng": 33.3281, 
                "name": "Olympic Swimming Pool",
                "share_link": ""
            },
            "dormitories": {
                "lat": 35.2253, 
                "lng": 33.3278, 
                "name": "Student Dormitories Area",
                "share_link": ""
            },
            "neu_mosque": {
                "lat": 35.2269, 
                "lng": 33.3271, 
                "name": "NEU Mosque (Cami)",
                "share_link": "https://maps.app.goo.gl/AbaMwvUt9JVHbumb7"
            },
        }
    
    def _get_map_link(self, location_key: str) -> str:
        if location_key not in self.locations:
            location_key = "neu_main"
        
        loc = self.locations[location_key]
        lat, lng = loc["lat"], loc["lng"]
        name = loc["name"]
        share_link = loc.get("share_link", "")
        
        # Use share link if available, otherwise construct URL
        if share_link:
            maps_url = share_link
            # Extract place_id or use coordinates for embed
            embed_url = f"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3265!2d{lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zM!5e0!3m2!1sen!2s!4v1702000000000!5m2!1sen!2s"
        elif location_key == "neu_main":
            maps_url = "https://maps.app.goo.gl/itWcEscDtg79itd27"
            embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3265.0644944447656!2d33.32418837637935!3d35.22673557270906!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14de4f6cf9b33f8f%3A0xb6dd16516c3eb1b9!2sNear%20East%20University!5e0!3m2!1sen!2s!4v1702000000000!5m2!1sen!2s"
        else:
            maps_url = f"https://www.google.com/maps?q={lat},{lng}"
            embed_url = f"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3265!2d{lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zM!5e0!3m2!1sen!2s!4v1702000000000!5m2!1sen!2s"
        
        # Create directions URL (from current location)
        directions_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&travelmode=walking"
        
        # Return enhanced map response with embedded iframe and directions
        return f"""
        <div class="map-container" style="margin: 15px 0; animation: slideIn 0.3s ease-out;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 12px 12px 0 0; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                    <svg style="width: 20px; height: 20px; fill: white;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    {name}
                </h3>
            </div>
            <div style="border: 2px solid #667eea; border-top: none; overflow: hidden;">
                <iframe 
                    src="{embed_url}" 
                    width="100%" 
                    height="300" 
                    style="border:0; display: block;" 
                    allowfullscreen="" 
                    loading="lazy" 
                    referrerpolicy="no-referrer-when-downgrade">
                </iframe>
            </div>
            <div style="margin-top: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <a href="{directions_url}" target="_blank" style="
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                    color: white; 
                    padding: 12px; 
                    border-radius: 10px; 
                    text-align: center; 
                    text-decoration: none; 
                    font-weight: 600;
                    font-size: 14px;
                    box-shadow: 0 4px 12px rgba(255,107,107,0.3);
                    transition: transform 0.2s, box-shadow 0.2s;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(255,107,107,0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(255,107,107,0.3)';">
                    <svg style="width: 18px; height: 18px; fill: white;" viewBox="0 0 24 24"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
                    Get Directions from My Location
                </a>
                <a href="{maps_url}" target="_blank" style="
                    background: #667eea; 
                    color: white; 
                    padding: 12px; 
                    border-radius: 10px; 
                    text-align: center; 
                    text-decoration: none; 
                    font-weight: 600;
                    font-size: 14px;
                    box-shadow: 0 4px 12px rgba(102,126,234,0.3);
                    transition: transform 0.2s, box-shadow 0.2s;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(102,126,234,0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(102,126,234,0.3)';">
                    <svg style="width: 18px; height: 18px; fill: white;" viewBox="0 0 24 24"><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/></svg>
                    View on Map
                </a>
            </div>
            <div style="margin-top: 10px;">
                <a href="https://maps.apple.com/?daddr={lat},{lng}" target="_blank" style="
                    display: flex;
                    background: #34c759; 
                    color: white; 
                    padding: 10px; 
                    border-radius: 8px; 
                    text-align: center; 
                    text-decoration: none; 
                    font-weight: 500;
                    font-size: 13px;
                    box-shadow: 0 2px 8px rgba(52,199,89,0.3);
                    transition: all 0.2s;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(52,199,89,0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(52,199,89,0.3)';">
                    <svg style="width: 16px; height: 16px; fill: white;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    Open in Apple Maps
                </a>
            </div>
            <div style="margin-top: 12px; padding: 12px; background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%); border-radius: 10px; font-size: 13px; border-left: 4px solid #667eea;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <svg style="width: 16px; height: 16px; fill: #667eea;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    <strong style="color: #667eea;">Location Details</strong>
                </div>
                <div style="color: #555; line-height: 1.6;">
                    <strong>Coordinates:</strong> {lat}, {lng}<br>
                    <strong>Navigation:</strong> Click "Get Directions" for turn-by-turn guidance<br>
                    <strong>Tip:</strong> Allow location access for best navigation experience
                </div>
            </div>
        </div>
        <style>
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """
    
    def _format_response(self, content: str, response_type: str = "info", title: str = None, follow_up_suggestions: List[str] = None) -> str:
        """Format responses with enhanced visual structure"""
        
        # Response type configurations with SVG icons
        type_config = {
            "info": {"icon": '<svg style="width: 20px; height: 20px; fill: #667eea;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>', "color": "#667eea", "bg": "#f0f4ff"},
            "success": {"icon": '<svg style="width: 20px; height: 20px; fill: #34c759;" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>', "color": "#34c759", "bg": "#e8f8ed"},
            "warning": {"icon": '<svg style="width: 20px; height: 20px; fill: #ff9500;" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>', "color": "#ff9500", "bg": "#fff4e6"},
            "tip": {"icon": '<svg style="width: 20px; height: 20px; fill: #5856d6;" viewBox="0 0 24 24"><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z"/></svg>', "color": "#5856d6", "bg": "#f3f2ff"},
            "location": {"icon": '<svg style="width: 20px; height: 20px; fill: #ff2d55;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>', "color": "#ff2d55", "bg": "#ffe6ed"},
            "academic": {"icon": '<svg style="width: 20px; height: 20px; fill: #007aff;" viewBox="0 0 24 24"><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/></svg>', "color": "#007aff", "bg": "#e6f2ff"}
        }
        
        config = type_config.get(response_type, type_config["info"])
        
        # Build response HTML
        response_html = f"""
        <div style="border-left: 4px solid {config['color']}; padding: 15px; margin: 10px 0; background: {config['bg']}; border-radius: 8px;">
        """
        
        if title:
            response_html += f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                {config['icon']}
                <strong style="font-size: 16px; color: {config['color']};">{title}</strong>
            </div>
            """
        
        response_html += f"""
            <div style="color: #333; line-height: 1.6;">
                {content}
            </div>
        """
        
        # Add follow-up suggestions
        if follow_up_suggestions:
            response_html += """
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ccc;">
                <div style="font-size: 14px; color: #666; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                    <svg style="width: 16px; height: 16px; fill: #666;" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                    <strong>You might also want to ask:</strong>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            """
            for suggestion in follow_up_suggestions:
                response_html += f"""
                <button class="follow-up-btn" onclick="sendFollowUpQuery('{suggestion}')" style="
                    background: white;
                    border: 1px solid {config['color']};
                    color: {config['color']};
                    padding: 6px 12px;
                    border-radius: 16px;
                    font-size: 13px;
                    cursor: pointer;
                    transition: all 0.2s;
                    white-space: nowrap;
                ">
                    {suggestion}
                </button>
                """
            response_html += """
                </div>
            </div>
            """
        
        response_html += "</div>"
        return response_html
    
    def _create_info_card(self, title: str, items: Dict[str, str], icon: str = None) -> str:
        """Create an information card with structured data"""
        # Default SVG icon for info card
        if icon is None:
            icon = '<svg style="width: 24px; height: 24px; fill: #667eea;" viewBox="0 0 24 24"><path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>'
        
        card_html = f"""
        <div style="background: white; border: 2px solid #e0e0e0; border-radius: 12px; padding: 16px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 2px solid #f0f0f0;">
                {icon}
                <h3 style="margin: 0; font-size: 18px; color: #333;">{title}</h3>
            </div>
            <div style="display: grid; gap: 10px;">
        """
        
        for key, value in items.items():
            card_html += f"""
                <div style="display: flex; align-items: start; gap: 8px;">
                    <span style="color: #667eea; font-weight: bold; min-width: 20px;">▪</span>
                    <div style="flex: 1;">
                        <strong style="color: #555;">{key}:</strong>
                        <span style="color: #666; margin-left: 5px;">{value}</span>
                    </div>
                </div>
            """
        
        card_html += """
            </div>
        </div>
        """
        return card_html
    
    def _create_step_guide(self, title: str, steps: List[Dict[str, str]], icon: str = None) -> str:
        """Create a step-by-step guide"""
        # Default SVG icon for step guide
        if icon is None:
            icon = '<svg style="width: 24px; height: 24px; fill: white;" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
        
        guide_html = f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 12px; color: white; margin: 10px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
                {icon}
                <h3 style="margin: 0; font-size: 18px;">{title}</h3>
            </div>
        </div>
        <div style="background: white; border: 2px solid #667eea; border-top: none; border-radius: 0 0 12px 12px; padding: 16px; margin-top: -10px;">
        """
        
        for i, step in enumerate(steps, 1):
            guide_html += f"""
            <div style="display: flex; gap: 12px; margin-bottom: 16px; align-items: start;">
                <div style="
                    min-width: 32px;
                    height: 32px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 16px;
                ">
                    {i}
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 4px;">{step['title']}</div>
                    <div style="color: #666; font-size: 14px;">{step['description']}</div>
                </div>
            </div>
            """
        
        guide_html += """
        </div>
        """
        return guide_html

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
            "where is cis faculty": f"📍 <strong>Faculty of Computer and Information Systems (CIS)</strong><br><br>The CIS Faculty building is located in the academic zone of the main NEU campus.<br><br>{self._get_map_link('cis_faculty')}<br><br>🚶 <strong>Directions:</strong> From the main entrance, follow signs to the academic buildings zone. Look for 'CIS' or 'Bilgisayar ve Bilişim Sistemleri Fakültesi' signs.<br><br>💡 You can also ask security or students for 'CIS Faculty' directions.",
            "cis faculty location": f"📍 <strong>CIS Faculty Building Location</strong><br><br>{self._get_map_link('cis_faculty')}<br><br>The CIS Faculty is on the main NEU campus in the academic zone. The faculty office and Dean's office (Prof. Dr. Nadire Cavus) are inside the CIS building.<br><br>🚶 From main entrance → Follow academic buildings signs → Look for 'CIS Faculty'",
            "engineering faculty location": f"📍 <strong>Faculty of Engineering</strong><br><br>The Faculty of Engineering is one of the largest buildings on campus, located in the central academic area.<br><br>{self._get_map_link('engineering_faculty')}<br><br>🚶 Look for the Engineering Faculty signs or ask any student for directions to 'Mühendislik Fakültesi'.",
            "medicine faculty location": f"📍 <strong>Faculty of Medicine</strong><br><br>The Faculty of Medicine is located near the NEU Hospital. It's clearly marked and easy to find.<br><br>{self._get_map_link('medicine_faculty')}<br><br>🏥 Located adjacent to NEU Hospital building.",
            "where is law faculty": f"📍 <strong>Faculty of Law</strong><br><br>{self._get_map_link('law_faculty')}<br><br>The Faculty of Law building is in the academic zone of the main campus. Check the map link above for precise directions.",
            "where is pharmacy faculty": f"📍 <strong>Faculty of Pharmacy</strong><br><br>{self._get_map_link('pharmacy_faculty')}<br><br>🧪 The Pharmacy Faculty is located in the health sciences area of campus. Click 'Get Directions' for turn-by-turn navigation from your current location.",
            "pharmacy faculty location": f"📍 <strong>Faculty of Pharmacy Location</strong><br><br>{self._get_map_link('pharmacy_faculty')}<br><br>💊 Easy to find in the health sciences zone. Use the map above for precise directions.",
            "where is health sciences faculty": f"📍 <strong>Faculty of Health Sciences (Sağlık Bilimleri)</strong><br><br>{self._get_map_link('health_sciences_faculty')}<br><br>🏥 Located near the Grand Hospital. Click 'Get Directions' to navigate from your location.",
            "where is grand hospital": f"📍 <strong>NEU Grand Hospital</strong><br><br>{self._get_map_link('neu_hospital')}<br><br>🏥 NEU's state-of-the-art hospital is one of the largest in Cyprus. Open 24/7 for emergencies.",
            "where is grand library": f"📍 <strong>Grand Library (Büyük Kütüphane)</strong><br><br>{self._get_map_link('grand_library')}<br><br>📚 Open 24/7 during semester. One of the largest university libraries in the region with millions of resources.",
            "where is mosque": f"📍 <strong>NEU Mosque (Cami)</strong><br><br>{self._get_map_link('neu_mosque')}<br><br>🕌 Beautiful mosque on campus for prayer and religious activities. Open daily for all five prayers.",
            "where is sports tower": f"📍 <strong>Sports Tower</strong><br><br>{self._get_map_link('sports_tower')}<br><br>🏋️ Multi-story sports facility with gym equipment, courts, and training areas. Modern facility for all students.",
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

            # Comprehensive NEU page mappings for direct scraping
            neu_pages_map = {
                # Academic & Education
                'library': ('https://neu.edu.tr/en/academic/library/', ['library', 'books', 'resources', 'study', 'kütüphane', 'kutuphan']),
                'ects': ('https://neu.edu.tr/en/academic/ects/', ['ects', 'credit', 'transfer', 'european credit']),
                'calendar': ('https://neu.edu.tr/en/academic/academic-calendar/', ['calendar', 'semester', 'schedule', 'dates', 'takvim']),
                'regulations': ('https://neu.edu.tr/en/academic/regulations/', ['regulation', 'rules', 'policy', 'policies', 'yönetmelik']),
                'faculties': ('https://neu.edu.tr/en/academic/faculties/', ['faculty', 'faculties', 'fakülte']),
                'colleges': ('https://neu.edu.tr/en/academic/colleges/', ['college', 'colleges', 'yüksekokul']),
                'vocational': ('https://neu.edu.tr/en/academic/vocational-schools/', ['vocational', 'meslek yüksekokulu', 'myo']),
                'graduate': ('https://neu.edu.tr/en/academic/graduate-education/', ['graduate', 'master', 'phd', 'doctorate', 'postgraduate', 'lisansüstü']),
                'preparatory': ('https://neu.edu.tr/en/academic/preparatory-school/', ['preparatory', 'prep', 'hazırlık', 'english preparatory']),
                'distance': ('https://neu.edu.tr/en/academic/distance-education/', ['distance education', 'online', 'uzaktan eğitim']),
                
                # Student Services
                'admission': ('https://neu.edu.tr/en/prospective-students/admission-requirements/', ['admission', 'apply', 'application', 'requirements', 'entry', 'başvuru']),
                'tuition': ('https://neu.edu.tr/en/prospective-students/tuition-fees/', ['tuition', 'fee', 'cost', 'payment', 'price', 'ücret']),
                'scholarship': ('https://neu.edu.tr/en/prospective-students/scholarships/', ['scholarship', 'discount', 'financial aid', 'bursary', 'burs']),
                'accommodation': ('https://neu.edu.tr/en/student/accommodation/', ['accommodation', 'dormitory', 'dorm', 'housing', 'residence', 'yurt', 'konaklama']),
                'international': ('https://neu.edu.tr/en/student/international-students/', ['international', 'foreign', 'visa', 'residence permit', 'uluslararası']),
                'student_affairs': ('https://neu.edu.tr/en/student/student-affairs/', ['student affairs', 'öğrenci işleri', 'student services']),
                
                # About & Info
                'about': ('https://neu.edu.tr/en/about-us/', ['about', 'history', 'founded', 'established', 'hakkında']),
                'ranking': ('https://neu.edu.tr/en/about-us/world-ranking/', ['ranking', 'rank', 'ranked', 'position', 'world ranking', 'world rank', 'sıralama', 'neu rank']),
                'accreditation': ('https://neu.edu.tr/en/academic/accreditations/', ['accreditation', 'accredited', 'recognition', 'akreditasyon']),
                'research': ('https://neu.edu.tr/en/research/', ['research', 'publication', 'journal', 'araştırma']),
                
                # Campus Life
                'campus': ('https://neu.edu.tr/en/campus-life/', ['campus', 'facility', 'facilities', 'kampüs']),
                'sports': ('https://neu.edu.tr/en/campus-life/sports/', ['sport', 'sports', 'athletics', 'gym', 'fitness', 'spor']),
                'clubs': ('https://neu.edu.tr/en/campus-life/student-clubs/', ['club', 'clubs', 'organization', 'society', 'kulüp']),
                
                # Career & Contact
                'career': ('https://neu.edu.tr/en/career/', ['career', 'job', 'employment', 'work', 'kariyer']),
                'contact': ('https://neu.edu.tr/en/contact/', ['contact', 'phone', 'email', 'address', 'iletişim']),
            }

            # Check for direct page matches
            for page_key, (url, keywords) in neu_pages_map.items():
                if any(keyword in query_lower for keyword in keywords):
                    result = self._fetch_page_content(url, query)
                    if result:
                        return result
                    # If scraping fails, return direct link
                    return (
                        f"For information about {page_key.replace('_', ' ')}, please visit:<br><br>"
                        f"🔗 <strong><a href='{url}' target='_blank'>NEU {page_key.replace('_', ' ').title()} Page</a></strong><br><br>"
                        f"This page contains comprehensive and up-to-date information about your query.<br><br>"
                        f"📞 For more details: +90 392 680 20 00<br>"
                        f"📧 Email: info@neu.edu.tr"
                    )

            # Try Google site search for anything else
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to extract page title
                page_title = ""
                title_tag = soup.find('title')
                if title_tag:
                    page_title = title_tag.get_text(strip=True).replace(' - Near East University', '').replace(' | NEU', '')
                
                # Try multiple content extraction strategies
                content_found = []
                
                # Strategy 1: Look for main content div/article
                main_content = soup.find(['article', 'main', 'div'], class_=lambda x: x and ('content' in x.lower() or 'main' in x.lower()))
                if main_content:
                    for p in main_content.find_all('p', limit=8):
                        text = p.get_text(strip=True)
                        if len(text) > 40 and text not in content_found:
                            content_found.append(text)
                
                # Strategy 2: Look for headings and their following content
                if len(content_found) < 3:
                    for heading in soup.find_all(['h1', 'h2', 'h3'], limit=5):
                        heading_text = heading.get_text(strip=True)
                        if len(heading_text) > 10:
                            content_found.append(f"<strong>{heading_text}</strong>")
                            # Get next paragraph or list
                            next_elem = heading.find_next(['p', 'ul', 'ol'])
                            if next_elem:
                                if next_elem.name in ['ul', 'ol']:
                                    items = [f"• {li.get_text(strip=True)}" for li in next_elem.find_all('li')[:5]]
                                    if items:
                                        content_found.append("<br>".join(items))
                                else:
                                    text = next_elem.get_text(strip=True)
                                    if len(text) > 40:
                                        content_found.append(text)
                
                # Strategy 3: Extract all meaningful paragraphs
                if len(content_found) < 2:
                    for p in soup.find_all('p', limit=10):
                        text = p.get_text(strip=True)
                        if len(text) > 50 and text not in content_found:
                            content_found.append(text)
                
                # Strategy 4: Look for lists
                if len(content_found) < 2:
                    for ul in soup.find_all(['ul', 'ol'], limit=3):
                        items = [f"• {li.get_text(strip=True)}" for li in ul.find_all('li')[:8]]
                        if items:
                            content_found.append("<br>".join(items))
                
                # Strategy 5: Extract contact information
                contact_info = []
                for elem in soup.find_all(['a', 'span', 'p']):
                    text = elem.get_text(strip=True)
                    if '@neu.edu.tr' in text or '+90' in text or 'Tel:' in text or 'Phone:' in text or 'Email:' in text:
                        if text not in contact_info and len(text) < 100:
                            contact_info.append(text)
                
                if content_found:
                    # Format the response nicely
                    formatted_content = "<br><br>".join(content_found[:4])
                    
                    result = f"📚 <strong>{page_title or 'Information from NEU Website'}</strong><br><br>"
                    result += formatted_content
                    
                    if contact_info:
                        result += "<br><br>📞 <strong>Contact Information:</strong><br>"
                        result += "<br>".join(contact_info[:3])
                    
                    result += f"<br><br>🔗 <strong><a href='{url}' target='_blank'>View Full Details on NEU Website</a></strong>"
                    
                    return result

            return None
        except Exception as e:
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

        # PRIORITY WEB SCRAPING: Handle specific queries that need website info FIRST
        # These should be checked BEFORE map/location queries to avoid false matches
        
        # Ranking queries - check early
        if any(word in msg_lower for word in ["rank", "ranking", "ranked", "world rank", "world ranking", "position", "sıralama"]):
            if not any(word in msg_lower for word in ["tournament", "event", "competition"]):
                scraped_result = self._scrape_neu_website(message_cleaned)
                if scraped_result:
                    return scraped_result
                return (
                    "<svg style='width: 20px; height: 20px; fill: #ff9500; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2l-2.81 6.63L2 9.24l5.46 4.73L5.82 21z'/></svg> <strong>NEU World Ranking</strong><br><br>"
                    "For current NEU rankings and recognition:<br><br>"
                    "<svg style='width: 18px; height: 18px; fill: #007aff; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M3 9h4V5H3v4zm0 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm-10 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm5-14v4h4V5h-4zm0 9h4v-4h-4v4z'/></svg> <strong><a href='https://neu.edu.tr/en/about-us/world-ranking/' target='_blank'>View NEU World Rankings</a></strong><br><br>"
                    "Near East University is recognized in various international university ranking systems including:<br>"
                    "• QS World University Rankings<br>"
                    "• Times Higher Education Rankings<br>"
                    "• Regional Rankings<br><br>"
                    "<svg style='width: 18px; height: 18px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z'/></svg> Contact: +90 392 680 20 00<br>"
                    "<svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z'/></svg> Email: info@neu.edu.tr"
                )
        
        # Accommodation queries - check early
        if any(word in msg_lower for word in ["accommodation", "accommodations", "konaklama", "accomodation"]):
            scraped_result = self._scrape_neu_website(message_cleaned)
            if scraped_result:
                return scraped_result
            return (
                "<svg style='width: 20px; height: 20px; fill: #34c759; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'/></svg> <strong>Accommodation Information</strong><br><br>"
                "For dormitory and housing options at NEU:<br><br>"
                "<svg style='width: 18px; height: 18px; fill: #007aff; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/></svg> <strong><a href='https://neu.edu.tr/en/student/accommodation/' target='_blank'>View Accommodation Options</a></strong><br><br>"
                "NEU offers various accommodation options:<br>"
                "• On-campus dormitories<br>"
                "• Different room types (single, double, triple)<br>"
                "• All utilities included<br>"
                "• 24/7 security<br><br>"
                "<svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z'/></svg> Contact: +90 392 680 20 00<br>"
                "<svg style='width: 18px; height: 18px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> Email: accommodation@neu.edu.tr"
            )
        
        # Calendar queries - exclude if asking about events/tournaments
        if (any(word in msg_lower for word in ["calendar", "takvim", "semester dates", "academic calendar"]) or 
            ("schedule" in msg_lower and not any(word in msg_lower for word in ["tournament", "event", "competition"]))):
            # Exclude if it's about events
            if not any(word in msg_lower for word in ["event", "tournament", "competition", "turnuva", "etkinlik"]):
                scraped_result = self._scrape_neu_website(message_cleaned)
                if scraped_result:
                    return scraped_result
                return (
                    "<svg style='width: 20px; height: 20px; fill: #ff9500; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z'/></svg> <strong>Academic Calendar Information</strong><br><br>"
                    "For current semester dates, holidays, and academic schedule:<br><br>"
                    "<svg style='width: 18px; height: 18px; fill: #007aff; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M3 9h4V5H3v4zm0 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm-10 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm5-14v4h4V5h-4zm0 9h4v-4h-4v4z'/></svg> <strong><a href='https://neu.edu.tr/en/academic/academic-calendar/' target='_blank'>View Academic Calendar</a></strong><br><br>"
                    "This includes:<br>"
                    "• Semester start and end dates<br>"
                    "• Registration periods<br>"
                    "• Exam schedules<br>"
                    "• Public holidays<br>"
                    "• Important academic deadlines<br><br>"
                    "<svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z'/></svg> Contact: +90 392 680 20 00"
                )
        
        # Events and tournaments - exclude if asking about location
        if any(word in msg_lower for word in ["tournament", "event", "competition", "turnuva", "etkinlik"]):
            # Exclude if asking for location of event
            if not any(phrase in msg_lower for phrase in ["where is the event", "event location", "where is the tournament", "tournament location"]):
                scraped_result = self._scrape_neu_website(message_cleaned)
                if scraped_result:
                    return scraped_result
                return (
                    "<svg style='width: 20px; height: 20px; fill: #ff9500; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'/></svg> <strong>Events & Tournaments</strong><br><br>"
                    "For current events, tournaments, and activities at NEU:<br><br>"
                    "• <a href='https://neu.edu.tr/en/announcements/' target='_blank'>NEU Announcements</a><br>"
                    "• <a href='https://neu.edu.tr/en/events/' target='_blank'>NEU Events Calendar</a><br>"
                    "• <a href='https://neu.edu.tr/en/campus-life/sports/' target='_blank'>Sports & Activities</a><br><br>"
                    "<svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z'/></svg> Contact: Department of Health, Culture and Sports<br>"
                    "<svg style='width: 18px; height: 18px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> Email: info@neu.edu.tr"
                )

        # Priority handling for dean queries - ALWAYS scrape website for accurate info
        # Exclude if query is about events/tournaments (like "inter faculty tournament")
        if (any(word in msg_lower for word in ["dean of", "dekan", "faculty dean", "head of faculty", "faculty head"]) and 
            not any(word in msg_lower for word in ["tournament", "event", "competition", "turnuva", "etkinlik", "inter faculty"])):
            # Check if asking about specific faculty
            faculty_pages = {
                "medicine": "https://neu.edu.tr/en/academic/faculties/faculty-of-medicine/",
                "pharmacy": "https://neu.edu.tr/en/academic/faculties/faculty-of-pharmacy/",
                "health sciences": "https://neu.edu.tr/en/academic/faculties/faculty-of-health-sciences/",
                "engineering": "https://neu.edu.tr/en/academic/faculties/faculty-of-engineering/",
                "law": "https://neu.edu.tr/en/academic/faculties/faculty-of-law/",
                "architecture": "https://neu.edu.tr/en/academic/faculties/faculty-of-architecture/",
                "economics": "https://neu.edu.tr/en/academic/faculties/faculty-of-economics-and-administrative-sciences/",
                "arts": "https://neu.edu.tr/en/academic/faculties/faculty-of-arts-and-sciences/",
                "education": "https://neu.edu.tr/en/academic/faculties/ataturk-faculty-of-education/",
                "communication": "https://neu.edu.tr/en/academic/faculties/faculty-of-communication/",
                "dentistry": "https://neu.edu.tr/en/academic/faculties/faculty-of-dentistry/",
                "veterinary": "https://neu.edu.tr/en/academic/faculties/faculty-of-veterinary-medicine/",
                "tourism": "https://neu.edu.tr/en/academic/faculties/faculty-of-tourism/",
                "maritime": "https://neu.edu.tr/en/academic/faculties/faculty-of-maritime/",
            }
            
            # Try to find specific faculty page
            for faculty_name, faculty_url in faculty_pages.items():
                if faculty_name in msg_lower:
                    scraped_result = self._fetch_page_content(faculty_url, message_cleaned)
                    if scraped_result:
                        return scraped_result
                    # If scraping fails, return link to faculty page
                    return (
                        f"For current dean information and faculty details, please visit:<br><br>"
                        f"<svg style='width: 20px; height: 20px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'/></svg> <strong><a href='{faculty_url}' target='_blank'>{faculty_name.title()} Faculty Page</a></strong><br><br>"
                        f"You can find:<br>"
                        f"• Current dean contact information<br>"
                        f"• Department heads<br>"
                        f"• Faculty office details<br>"
                        f"• Academic staff directory<br><br>"
                        f"<svg style='width: 18px; height: 18px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> For urgent inquiries: info@neu.edu.tr"
                    )
            
            # General dean query - return all faculties page
            return (
                "<svg style='width: 20px; height: 20px; fill: #5856d6; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z'/></svg> <strong>Faculty Deans & Leadership</strong><br><br>"
                "For current and accurate information about all faculty deans, please visit:<br><br>"
                "<svg style='width: 18px; height: 18px; fill: #ff9500; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z'/></svg> <strong><a href='https://neu.edu.tr/en/academic/faculties/' target='_blank'>View All Faculties & Their Deans</a></strong><br><br>"
                "This page provides:<br>"
                "• Complete list of all 16 faculties<br>"
                "• Current dean names and contact information<br>"
                "• Department heads and academic staff<br>"
                "• Faculty office locations and hours<br><br>"
                "<svg style='width: 18px; height: 18px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/></svg> <strong>Tip:</strong> You can ask about a specific faculty, for example:<br>"
                "• 'Who is the dean of Medicine?'<br>"
                "• 'Dean of Engineering faculty'<br>"
                "• 'Pharmacy faculty dean contact'<br><br>"
                "<svg style='width: 18px; height: 18px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> General inquiries: info@neu.edu.tr"
            )

        # Special handling for map/location queries with embedded map
        # Only trigger if it's actually asking for a location/direction
        # Exclude queries about events, tournaments, calendar, schedules
        is_location_query = (
            # Exclude calendar, event, tournament queries
            not any(word in msg_lower for word in ["tournament", "event", "competition", "calendar", "schedule", "when is", "when does", "starting"]) and
            (
                any(word in msg_lower for word in ["where is", "where's", "location of", "how to get to", "how do i get to", "directions to", "nerede"]) or
                ("map" in msg_lower and any(word in msg_lower for word in ["show", "campus", "building"])) or
                (any(word in msg_lower for word in ["pharmacy faculty", "medicine faculty", "engineering faculty", "law faculty", "cis faculty", 
                                                      "hospital", "library", "mosque", "bank", "dormitory"]) and 
                 any(word in msg_lower for word in ["where", "location", "find"]))
            )
        )
        
        if is_location_query:
            # Enhanced keyword matching for specific locations
            location_keywords = {
                "pharmacy": "pharmacy_faculty",
                "eczane": "pharmacy_faculty",
                "medicine": "medicine_faculty",
                "tip": "medicine_faculty",
                "medical": "medicine_faculty",
                "health sciences": "health_sciences_faculty",
                "saglik bilimleri": "health_sciences_faculty",
                "hospital": "neu_hospital",
                "grand hospital": "neu_hospital",
                "hastane": "neu_hospital",
                "library": "grand_library",
                "kütüphane": "grand_library",
                "kutuphan": "grand_library",
                "mosque": "neu_mosque",
                "cami": "neu_mosque",
                "prayer": "neu_mosque",
                "sports tower": "sports_tower",
                "spor kulesi": "sports_tower",
                "cis": "cis_faculty",
                "computer": "cis_faculty",
                "engineering": "engineering_faculty",
                "muhendislik": "engineering_faculty",
                "law": "law_faculty",
                "hukuk": "law_faculty",
                "architecture": "architecture_faculty",
                "mimarlik": "architecture_faculty",
                "bank": "near_east_bank_main",
                "banka": "near_east_bank_main",
                "dormitory": "dormitories",
                "dormitories": "dormitories",
                "yurt": "dormitories",
                "dorm": "dormitories",
                "sports": "sports_complex",
                "spor": "sports_complex",
                "pool": "olympic_pool",
                "swimming": "olympic_pool",
                "rectorate": "rectorate",
                "rektörlük": "rectorate",
                "administration": "rectorate",
                "international office": "international_office",
                "student affairs": "student_affairs",
            }
            
            # Check for keyword matches
            for keyword, loc_key in location_keywords.items():
                if keyword in msg_lower:
                    return self._get_map_link(loc_key)
            
            # Check for location name matches
            for loc_key in self.locations.keys():
                loc_name = self.locations[loc_key]["name"].lower()
                if any(word in msg_lower for word in loc_name.split()):
                    return self._get_map_link(loc_key)
            
            # Default to main campus map
            return self._get_map_link("neu_main")
        
        # Special handling for registration with enhanced formatting
        # Exclude if asking about course registration, events, or other unrelated topics
        if (any(word in msg_lower for word in ["register", "registration", "enroll", "enrollment"]) and 
            "course" not in msg_lower and
            not any(word in msg_lower for word in ["event", "tournament", "competition"])):
            steps = [
                {
                    "title": "Visit Uzebim Portal",
                    "description": "Go to <a href='https://uzebim.neu.edu.tr/' target='_blank' style='color: #667eea;'>uzebim.neu.edu.tr</a> and log in with your credentials"
                },
                {
                    "title": "Prepare Documents",
                    "description": "Have your passport, high school diploma, transcript, acceptance letter, and payment receipt ready"
                },
                {
                    "title": "Complete Registration Steps",
                    "description": "Follow the on-screen instructions to complete each registration section"
                },
                {
                    "title": "Get Help if Needed",
                    "description": "Visit the International Office (Rectorate Building, Ground Floor) for assistance"
                }
            ]
            
            follow_ups = ["What documents do I need?", "International Office location", "Tuition fees"]
            
            guide = self._create_step_guide("<svg style='width: 20px; height: 20px; fill: #667eea; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-8-6z'/></svg> Student Registration Process", steps, "<svg style='width: 18px; height: 18px; fill: #5856d6;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z'/></svg>")
            formatted = self._format_response(
                guide,
                response_type="academic",
                title="How to Register at NEU",
                follow_up_suggestions=follow_ups
            )
            return formatted
        
        # Special handling for tuition/fees
        # Exclude if asking about events, tournaments, or other unrelated topics
        if (any(word in msg_lower for word in ["tuition", "fee", "cost", "price"]) or
            ("payment" in msg_lower and any(word in msg_lower for word in ["how to pay", "payment method", "pay tuition"]))) and \
            not any(word in msg_lower for word in ["event", "tournament", "competition"]):
            info_card = self._create_info_card(
                "<svg style='width: 20px; height: 20px; fill: #34c759; vertical-align: middle; margin-right: 8px;' viewBox='0 0 24 24'><path d='M11.8 10.9c-2.27-.59-3-1.38-3-2.39 0-1.02.88-1.64 2.19-1.64 1.29 0 1.97.63 2.19 1.55h1.75c-.23-1.85-1.45-2.78-3.94-2.78-2.35 0-3.72 1.44-3.72 2.97 0 2.13 1.23 2.97 3.35 3.61 2.16.59 3.4 1.08 3.4 2.2 0 .98-.99 1.59-2.3 1.59s-2.42-.6-2.63-1.51H8.4c.21 1.62 1.38 2.77 3.6 2.77 2.3 0 3.72-1.44 3.72-2.8 0-2.06-1.12-2.65-3.84-3.37zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z'/></svg> Payment Information",
                {
                    "Payment Methods": "Near East Bank, POS at International Office, Bank Transfer",
                    "Payment Plans": "Full payment (with discount) or installment options available",
                    "Bank Location": "Near East Bank on campus (next to Rectorate Building)",
                    "Financial Office": "Check balances in Genius Portal under 'Financial' section"
                },
                "💰"
            )
            
            follow_ups = ["Near East Bank location", "Scholarship options", "Payment deadline"]
            
            return self._format_response(
                info_card + "<br>💡 <strong>Tip:</strong> Full payment often includes discounts. Ask the Financial Office for current rates!",
                response_type="info",
                title="Tuition & Fees Information",
                follow_up_suggestions=follow_ups
            )

        # PRIORITY WEB SCRAPING: For queries that need current/accurate info from website
        # These topics should ALWAYS check the website BEFORE using FAQ
        priority_scraping_keywords = [
            # Academic structure
            'vocational school', 'college', 'yüksekokul', 'meslek',
            'graduate institute', 'lisansüstü', 'postgraduate',
            'preparatory', 'hazırlık', 'prep school',
            'coordinator', 'koordinatör',
            
            # Services & Resources
            'library hours', 'library opening', 'kütüphane saatleri', 'grand library',
            'ects', 'credit transfer', 'credit system',
            'regulation', 'yönetmelik', 'policy',
            'distance education', 'online course', 'uzaktan eğitim',
            
            # Events & Activities (already handled above but adding for completeness)
            'announcement', 'duyuru',
            
            # Rankings & Recognition
            'ranking', 'world rank', 'sıralama',
            'accreditation', 'accredited', 'akreditasyon',
            'recognition', 'tanınma',
            
            # Research & Career
            'research center', 'araştırma merkezi',
            'career office', 'job placement', 'kariyer',
            'publication', 'research output',
            
            # Campus Services
            'sports facilities', 'gym', 'fitness center',
            'student club', 'kulüp', 'organization',
            'health service', 'medical center',
            
            # Contact & Info
            'phone number', 'contact information', 'address', 'iletişim',
            'email address', 'office hours',
            
            # Programs
            'program list', 'available programs', 'departments',
            'double major', 'minor program', 'çift anadal',
        ]
        
        # Check if query contains priority scraping keywords
        if any(keyword in msg_lower for keyword in priority_scraping_keywords):
            scraped_result = self._scrape_neu_website(message_cleaned)
            if scraped_result:
                return scraped_result
            # If scraping fails, still continue to FAQ check as fallback

        # Check FAQ database
        answer = self._find_best_match(message_cleaned)

        if answer:
            return answer

        # Try web scraping for anything not in FAQ
        scraped_result = self._scrape_neu_website(message_cleaned)
        if scraped_result:
            return scraped_result

        if language == "TR":
            return (
                "Bu konuda veritabanımda henüz özel bilgi yok, ancak size yardımcı olabilirim!<br><br>"
                "<strong><svg style='width: 20px; height: 20px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'/></svg> Önemli Kaynaklar:</strong><br>"
                "• <a href='https://neu.edu.tr' target='_blank'>NEU Resmi Web Sitesi</a><br>"
                "• <a href='https://neu.edu.tr/en/academic/' target='_blank'>Akademik (Fakülteler, Programlar, Takvim)</a><br>"
                "• <a href='https://neu.edu.tr/en/student/' target='_blank'>Öğrenci Servisleri</a><br>"
                "• <a href='https://neu.edu.tr/en/academic/library/' target='_blank'>Kütüphane</a><br>"
                "• <a href='https://uzebim.neu.edu.tr' target='_blank'>Uzebim Portalı</a> - Öğrenci Sistemi<br>"
                "• <a href='https://register.neu.edu.tr' target='_blank'>Genius Portalı</a> - Ders Kaydı<br><br>"
                "<strong><svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20.01 15.38c-1.23 0-2.42-.2-3.53-.56-.35-.12-.74-.03-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z'/></svg> İletişim:</strong><br>"
                "<svg style='width: 16px; height: 16px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm0-13c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z'/></svg> Yakın Doğu Bulvarı, PK: 99138, Lefkoşa / KKTC<br>"
                "<svg style='width: 16px; height: 16px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z'/></svg> +90 392 223 64 64 / +90 392 680 20 00<br>"
                "<svg style='width: 16px; height: 16px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> info@neu.edu.tr<br><br>"
                "<strong><svg style='width: 18px; height: 18px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z'/></svg> Popüler Konular:</strong> Fakülteler, Dekanlar, Kayıt, Kütüphane, ECTS, Akademik Takvim, Yurtlar, Burslar, Programlar"
            )
        
        return (
            "I couldn't find specific information about that, but here are helpful resources:<br><br>"
            "<strong><svg style='width: 20px; height: 20px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'/></svg> Essential Links:</strong><br>"
            "• <a href='https://neu.edu.tr/en' target='_blank'>NEU Official Website</a><br>"
            "• <a href='https://neu.edu.tr/en/academic/' target='_blank'>Academic (Faculties, Programs, Calendar)</a><br>"
            "• <a href='https://neu.edu.tr/en/student/' target='_blank'>Student Services</a><br>"
            "• <a href='https://neu.edu.tr/en/academic/library/' target='_blank'>Grand Library</a><br>"
            "• <a href='https://uzebim.neu.edu.tr' target='_blank'>Uzebim Portal</a> - Student System<br>"
            "• <a href='https://register.neu.edu.tr' target='_blank'>Genius Portal</a> - Course Registration<br><br>"
            "<strong><svg style='width: 18px; height: 18px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20.01 15.38c-1.23 0-2.42-.2-3.53-.56-.35-.12-.74-.03-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z'/></svg> Contact Information:</strong><br>"
            "<svg style='width: 16px; height: 16px; fill: #ff2d55; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm0-13c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z'/></svg> Near East Boulevard, PK: 99138, Nicosia / TRNC<br>"
            "<svg style='width: 16px; height: 16px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z'/></svg> +90 392 223 64 64 / +90 392 680 20 00<br>"
            "<svg style='width: 16px; height: 16px; fill: #5856d6; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V6c0-1.1-.9-2-2-2zm-2 12H4V6h14v10z'/></svg> info@neu.edu.tr<br><br>"
            "<strong><svg style='width: 18px; height: 18px; fill: #34c759; vertical-align: middle; margin-right: 6px;' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z'/></svg> Popular Topics:</strong> Faculties, Deans, Registration, Library, ECTS, Academic Calendar, Dormitories, Scholarships, Programs"
        )

    def get_session_history(self, session_id: str) -> List[str]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

bot = BotLogic()
