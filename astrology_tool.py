import datetime
import pytz
import math
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import swisseph as swe
import matplotlib.pyplot as plt
import numpy as np


class AstrologyTool:
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path()  # Uses default ephemeris path
        print("Swiss Ephemeris initialized.")

        # Define planets
        self.planets = {
            swe.SUN: "Sun",
            swe.MOON: "Moon",
            swe.MERCURY: "Mercury",
            swe.VENUS: "Venus",
            swe.MARS: "Mars",
            swe.JUPITER: "Jupiter",
            swe.SATURN: "Saturn",
            swe.URANUS: "Uranus",
            swe.NEPTUNE: "Neptune",
            swe.PLUTO: "Pluto"
        }
        print("Planets defined.")

        # Define zodiac signs
        self.signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        print("Zodiac signs defined.")

        # Define sign rulers (traditional)
        self.sign_rulers = {
            "Aries": "Mars",
            "Taurus": "Venus",
            "Gemini": "Mercury",
            "Cancer": "Moon",
            "Leo": "Sun",
            "Virgo": "Mercury",
            "Libra": "Venus",
            "Scorpio": "Mars/Pluto",
            "Sagittarius": "Jupiter",
            "Capricorn": "Saturn",
            "Aquarius": "Saturn/Uranus",
            "Pisces": "Jupiter/Neptune"
        }
        print("Sign rulers defined.")

        # Define sign elements
        self.sign_elements = {
            "Aries": "Fire",
            "Taurus": "Earth",
            "Gemini": "Air",
            "Cancer": "Water",
            "Leo": "Fire",
            "Virgo": "Earth",
            "Libra": "Air",
            "Scorpio": "Water",
            "Sagittarius": "Fire",
            "Capricorn": "Earth",
            "Aquarius": "Air",
            "Pisces": "Water"
        }
        print("Sign elements defined.")

        # Define sign qualities
        self.sign_qualities = {
            "Aries": "Cardinal",
            "Taurus": "Fixed",
            "Gemini": "Mutable",
            "Cancer": "Cardinal",
            "Leo": "Fixed",
            "Virgo": "Mutable",
            "Libra": "Cardinal",
            "Scorpio": "Fixed",
            "Sagittarius": "Mutable",
            "Capricorn": "Cardinal",
            "Aquarius": "Fixed",
            "Pisces": "Mutable"
        }
        print("Sign qualities defined.")

        # Define house meanings
        self.house_meanings = {
            1: "Self, appearance, beginnings",
            2: "Values, possessions, resources",
            3: "Communication, siblings, short trips",
            4: "Home, family, roots",
            5: "Creativity, romance, children",
            6: "Health, service, daily routine",
            7: "Partnerships, marriage, open enemies",
            8: "Transformation, shared resources, death",
            9: "Higher education, philosophy, long journeys",
            10: "Career, public reputation, authority",
            11: "Friends, groups, hopes and wishes",
            12: "Subconscious, isolation, hidden enemies"
        }
        print("House meanings defined.")

        # Define planet meanings
        self.planet_meanings = {
            "Sun": "Core identity, life purpose, vitality",
            "Moon": "Emotions, instincts, subconscious patterns",
            "Mercury": "Communication, thinking, learning",
            "Venus": "Love, beauty, values, attraction",
            "Mars": "Action, desire, energy, assertion",
            "Jupiter": "Expansion, growth, abundance, wisdom",
            "Saturn": "Structure, limitations, responsibility, time",
            "Uranus": "Innovation, rebellion, sudden change",
            "Neptune": "Dreams, spirituality, illusion, dissolution",
            "Pluto": "Transformation, power, elimination, rebirth"
        }
        print("Planet meanings defined.")

        # Define major aspects and their orbs
        self.aspects = {
            "Conjunction": {"angle": 0, "orb": 8, "nature": "Intensification"},
            "Opposition": {"angle": 180, "orb": 8, "nature": "Tension, awareness"},
            "Trine": {"angle": 120, "orb": 8, "nature": "Harmony, flow"},
            "Square": {"angle": 90, "orb": 7, "nature": "Challenge, action"},
            "Sextile": {"angle": 60, "orb": 6, "nature": "Opportunity, ease"}
        }
        print("Major aspects defined.")

    def get_coordinates(self, location):
        """Convert location name to latitude and longitude"""
        geolocator = Nominatim(user_agent="astrology_tool")
        try:
            location_data = geolocator.geocode(location)
            if location_data:
                print(f"Coordinates found for {location}: {location_data.latitude}, {location_data.longitude}")
                return location_data.latitude, location_data.longitude
            else:
                raise ValueError(f"Could not find coordinates for location: {location}")
        except Exception as e:
            raise ValueError(f"Error getting coordinates: {e}")

    def get_timezone(self, latitude, longitude):
        """Get timezone for given coordinates"""
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        if not timezone_str:
            raise ValueError("Could not determine timezone for the provided coordinates")
        print(f"Timezone determined: {timezone_str}")
        return timezone_str

    def calculate_julian_day(self, birth_date, birth_time, latitude, longitude):
        """Calculate Julian day for the birth date and time"""
        # Get timezone for the location
        timezone_str = self.get_timezone(latitude, longitude)
        timezone = pytz.timezone(timezone_str)

        # Combine date and time
        year, month, day = birth_date
        hour, minute, second = birth_time

        # Create datetime object
        local_datetime = datetime.datetime(year, month, day, hour, minute, second)

        # Convert to UTC
        local_datetime = timezone.localize(local_datetime)
        utc_datetime = local_datetime.astimezone(pytz.UTC)

        # Calculate Julian day
        jd = swe.julday(utc_datetime.year, utc_datetime.month, utc_datetime.day,
                        utc_datetime.hour + utc_datetime.minute / 60.0 + utc_datetime.second / 3600.0)

        print(f"Julian Day calculated: {jd}")
        return jd, timezone_str

    def calculate_houses(self, jd, latitude, longitude):
        """Calculate the house cusps using Placidus system"""
        # Set geographic position
        geolat, geolon = latitude, longitude

        # Calculate houses
        houses = swe.houses(jd, geolat, geolon)[0]

        # Calculate Ascendant and Midheaven
        ascendant = houses[0]
        midheaven = houses[9]

        print(f"Houses calculated: Ascendant {ascendant}, Midheaven {midheaven}")
        return houses, ascendant, midheaven

    def calculate_planet_positions(self, jd):
        """Calculate positions of planets at given Julian day"""
        planet_positions = {}

        for planet_id, planet_name in self.planets.items():
            # Calculate planet's position
            result, _ = swe.calc_ut(jd, planet_id)
            print(f"Result for {planet_name}: {result}")  # Debugging line

            # Ensure result is a tuple and has the expected structure
            if isinstance(result, tuple) and len(result) > 0:
                longitude = result[0]  # Extract the longitude from the nested tuple

                # Determine zodiac sign and degree
                sign_num = int(longitude / 30)
                sign_deg = longitude % 30

                planet_positions[planet_name] = {
                    "longitude": longitude,
                    "sign": self.signs[sign_num],
                    "degree": sign_deg
                }
            else:
                print(f"Unexpected result format for {planet_name}: {result}")

        print("Planet positions calculated.")
        return planet_positions

    def calculate_aspects(self, planet_positions):
        """Calculate aspects between planets"""
        aspects_list = []

        # Get list of planets
        planets = list(planet_positions.keys())

        # Check each planet pair for aspects
        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]

                # Calculate the angle between planets
                long1 = planet_positions[planet1]["longitude"]
                long2 = planet_positions[planet2]["longitude"]

                # Find the shortest angle
                angle = abs(long1 - long2)
                if angle > 180:
                    angle = 360 - angle

                # Check if this angle forms an aspect
                for aspect_name, aspect_info in self.aspects.items():
                    aspect_angle = aspect_info["angle"]
                    orb = aspect_info["orb"]

                    # Check if the angle is within the orb
                    if abs(angle - aspect_angle) <= orb:
                        aspects_list.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "aspect": aspect_name,
                            "orb": round(abs(angle - aspect_angle), 2),
                            "nature": aspect_info["nature"]
                        })

        print("Aspects calculated.")
        return aspects_list

    def assign_planets_to_houses(self, planet_positions, houses):
        """Assign planets to houses"""
        planets_in_houses = {}

        for house_num in range(1, 13):
            planets_in_houses[house_num] = []

            # House boundaries
            house_start = houses[house_num - 1]
            house_end = houses[house_num % 12]  # Wrap around to house 1 for house 12

            # Handle house spanning 0° Aries
            if house_end < house_start:
                house_end += 360

            # Check each planet
            for planet, data in planet_positions.items():
                planet_long = data["longitude"]

                # Adjust longitude if house spans 0° Aries
                if house_end > 360 and planet_long < house_end - 360:
                    adjusted_long = planet_long + 360
                else:
                    adjusted_long = planet_long

                # Check if planet is in this house
                if house_start <= adjusted_long < house_end:
                    planets_in_houses[house_num].append(planet)

        print("Planets assigned to houses.")
        return planets_in_houses

    def interpret_sun_sign(self, sign, gender):
        """Basic Sun sign interpretation with gender considerations"""
        base_traits = {
            "Aries": "courageous, energetic, and pioneering. You have a strong drive to initiate and lead. You're direct, enthusiastic, and can be impulsive at times.",
            "Taurus": "reliable, patient, and practical. You value stability and comfort. You can be stubborn but also incredibly loyal and determined.",
            "Gemini": "versatile, curious, and communicative. You love learning and sharing ideas. You seek variety and can adapt quickly to new situations.",
            "Cancer": "nurturing, intuitive, and protective. You have strong emotional awareness and value security. Your home and family are central to your identity.",
            "Leo": "confident, generous, and dramatic. You have natural leadership qualities and love to be appreciated. You're warm-hearted and enjoy creative expression.",
            "Virgo": "analytical, meticulous, and practical. You have an eye for detail and a strong desire to be of service. You strive for improvement and perfection.",
            "Libra": "diplomatic, fair-minded, and sociable. You seek harmony and balance in all things. Relationships and beauty are highly important to you.",
            "Scorpio": "intense, passionate, and resourceful. You have powerful emotions and desires. You seek truth beneath the surface and can be transformative.",
            "Sagittarius": "optimistic, freedom-loving, and philosophical. You seek meaning and adventure. You're honest, open-minded, and enjoy exploring new horizons.",
            "Capricorn": "ambitious, disciplined, and responsible. You have strong determination and organizational skills. You're practical and work toward long-term goals.",
            "Aquarius": "independent, original, and humanitarian. You think in innovative ways and value your uniqueness. You're drawn to progressive ideas and causes.",
            "Pisces": "compassionate, imaginative, and intuitive. You're highly sensitive to energies around you. You're spiritual and can be artistic or musical."
        }

        # Gender-specific traits (simplified and generalized)
        gender_traits = {
            "Male": {
                "Aries": "You may express your Aries energy through direct action and leadership.",
                "Taurus": "Your Taurus nature might manifest in a provider role and material security focus.",
                "Gemini": "As a Gemini man, you may channel your communication skills into intellectual debates.",
                "Cancer": "Your Cancer traits might be expressed through protective instincts and emotional depth.",
                "Leo": "Your Leo qualities may show through pride in accomplishments and desire for recognition.",
                "Virgo": "As a Virgo man, you might focus your analytical skills on practical problem-solving.",
                "Libra": "Your Libra traits may appear in diplomatic approaches to relationships.",
                "Scorpio": "Your Scorpio intensity might express through ambition and strategic thinking.",
                "Sagittarius": "As a Sagittarius man, you may seek freedom through adventure and exploration.",
                "Capricorn": "Your Capricorn nature might focus on career advancement and authority.",
                "Aquarius": "Your Aquarius qualities may show through intellectual independence.",
                "Pisces": "As a Pisces man, you might express your sensitivity through creative or spiritual pursuits."
            },
            "Female": {
                "Aries": "You may express your Aries energy through pioneering initiatives and independence.",
                "Taurus": "Your Taurus nature might manifest in appreciating beauty and creating comfort.",
                "Gemini": "As a Gemini woman, you may use your communication skills in social connections.",
                "Cancer": "Your Cancer traits might appear through nurturing and intuitive understanding.",
                "Leo": "Your Leo qualities may show through creative self-expression and warm leadership.",
                "Virgo": "As a Virgo woman, you might channel your detailed analysis into helping others.",
                "Libra": "Your Libra traits may appear in creating harmony and aesthetic appreciation.",
                "Scorpio": "Your Scorpio intensity might express through emotional depth and perception.",
                "Sagittarius": "As a Sagittarius woman, you may seek truth through educational pursuits.",
                "Capricorn": "Your Capricorn nature might focus on structured achievement and responsibility.",
                "Aquarius": "Your Aquarius qualities may show through social activism and progressive thinking.",
                "Pisces": "As a Pisces woman, you might express your compassion through empathy and intuition."
            },
            "Other": {
                # Gender-neutral interpretations
                "Aries": "Your Aries energy can manifest through self-directed initiative and courage.",
                "Taurus": "Your Taurus nature might express through appreciation of sensory experiences.",
                "Gemini": "Your Gemini traits can appear through versatile communication and adaptability.",
                "Cancer": "Your Cancer qualities might show through emotional intelligence and creating safety.",
                "Leo": "Your Leo energy can manifest through authentic self-expression and generosity.",
                "Virgo": "Your Virgo traits might appear through skillful analysis and practical helpfulness.",
                "Libra": "Your Libra nature can express through creating balance and fair mediation.",
                "Scorpio": "Your Scorpio qualities might show through transformative insight and resourcefulness.",
                "Sagittarius": "Your Sagittarius energy can manifest through philosophical exploration.",
                "Capricorn": "Your Capricorn traits might appear through structured approach and integrity.",
                "Aquarius": "Your Aquarius nature can express through innovative thinking and community focus.",
                "Pisces": "Your Pisces qualities might show through intuitive understanding and compassion."
            }
        }

        # Combine base interpretation with gender-specific nuance
        if gender.lower() in ["male", "m"]:
            gender_key = "Male"
        elif gender.lower() in ["female", "f"]:
            gender_key = "Female"
        else:
            gender_key = "Other"

        interpretation = f"As a {sign} Sun, you are {base_traits[sign]} {gender_traits[gender_key][sign]}"
        print(f"Sun sign interpretation for {sign} ({gender}): {interpretation}")
        return interpretation

    def interpret_moon_sign(self, sign):
        """Basic Moon sign interpretation"""
        interpretations = {
            "Aries": "Your emotions are dynamic and quickly expressed. You react instinctively and may become impatient with subtle feelings. You need independence to process emotions.",
            "Taurus": "Your emotional nature seeks stability and comfort. You process feelings slowly and thoroughly. Security and physical comfort help you feel emotionally balanced.",
            "Gemini": "Your emotions connect to your thoughts. You process feelings through conversation and intellectual understanding. Emotional variety keeps you engaged.",
            "Cancer": "Your emotional responses are deep and protective. You're highly sensitive to moods around you. Family connections provide emotional security.",
            "Leo": "Your emotions are expressed dramatically and warmly. You need recognition for your feelings. Creative expression helps process emotional experiences.",
            "Virgo": "Your emotional nature is careful and analytical. You process feelings by organizing and understanding them. Small acts of service help you feel emotionally balanced.",
            "Libra": "Your emotions are tied to harmony in relationships. You process feelings through connection with others. Balance and beauty help calm emotional turbulence.",
            "Scorpio": "Your emotional responses are intense and transformative. You feel deeply and may keep emotions private. Emotional truth and intimacy are essential to you.",
            "Sagittarius": "Your emotional nature seeks meaning and expansion. You process feelings through philosophical understanding. Freedom helps you manage emotions.",
            "Capricorn": "Your emotions are controlled and structured. You process feelings through practical action. Achievement helps you feel emotionally secure.",
            "Aquarius": "Your emotional responses are unique and detached. You process feelings through intellectual understanding. Friendship and community support your emotional wellbeing.",
            "Pisces": "Your emotional nature is fluid and compassionate. You absorb feelings from your environment. Spiritual connection helps you process emotional experiences."
        }
        print(f"Moon sign interpretation for {sign}: {interpretations[sign]}")
        return interpretations[sign]

    def interpret_ascendant(self, sign):
        """Basic Ascendant interpretation"""
        interpretations = {
            "Aries": "You appear direct, energetic, and self-motivated. First impressions show your confidence and pioneering spirit. You approach new situations with enthusiasm.",
            "Taurus": "You appear reliable, steady, and practical. First impressions show your grounded nature. You approach new situations with patience and consideration.",
            "Gemini": "You appear versatile, communicative, and curious. First impressions show your mental agility. You approach new situations with adaptability and questions.",
            "Cancer": "You appear sensitive, nurturing, and protective. First impressions show your caring nature. You approach new situations with caution and emotional awareness.",
            "Leo": "You appear confident, warm, and dramatic. First impressions show your expressive personality. You approach new situations with enthusiasm and creativity.",
            "Virgo": "You appear analytical, helpful, and detailed. First impressions show your practical intelligence. You approach new situations with careful observation.",
            "Libra": "You appear diplomatic, charming, and balanced. First impressions show your social grace. You approach new situations with fairness and consideration.",
            "Scorpio": "You appear intense, mysterious, and perceptive. First impressions show your depth. You approach new situations with strategic awareness.",
            "Sagittarius": "You appear optimistic, straightforward, and adventurous. First impressions show your expansive outlook. You approach new situations with enthusiasm.",
            "Capricorn": "You appear responsible, ambitious, and reserved. First impressions show your composed nature. You approach new situations with strategic planning.",
            "Aquarius": "You appear unique, innovative, and independent. First impressions show your originality. You approach new situations with fresh perspective.",
            "Pisces": "You appear compassionate, dreamy, and gentle. First impressions show your sensitivity. You approach new situations with intuitive understanding."
        }
        print(f"Ascendant interpretation for {sign}: {interpretations[sign]}")
        return interpretations[sign]

    def interpret_mercury(self, sign):
        """Basic Mercury sign interpretation"""
        interpretations = {
            "Aries": "Your communication style is direct and assertive. You think quickly and enjoy mental challenges. You learn best through active engagement and competition.",
            "Taurus": "Your communication style is deliberate and practical. You think thoroughly and value sensory information. You learn best through hands-on experience.",
            "Gemini": "Your communication style is versatile and quick. You think in varied ways and enjoy gathering information. You learn best through conversation and variety.",
            "Cancer": "Your communication style is empathetic and protective. You think with emotional awareness. You learn best in nurturing environments where you feel safe.",
            "Leo": "Your communication style is expressive and confident. You think creatively and enjoy being heard. You learn best when recognized for your ideas.",
            "Virgo": "Your communication style is precise and analytical. You think critically and notice details. You learn best through organized systems and practical application.",
            "Libra": "Your communication style is diplomatic and considerate. You think with awareness of others' perspectives. You learn best through discussion and cooperation.",
            "Scorpio": "Your communication style is intense and probing. You think deeply and seek hidden truths. You learn best through investigation and transformation.",
            "Sagittarius": "Your communication style is enthusiastic and expansive. You think philosophically and optimistically. You learn best through exploration and meaning.",
            "Capricorn": "Your communication style is structured and purposeful. You think strategically with long-term goals. You learn best through established methods.",
            "Aquarius": "Your communication style is inventive and objective. You think in original ways that may seem unconventional. You learn best through experimentation.",
            "Pisces": "Your communication style is intuitive and compassionate. You think imaginatively and absorb information. You learn best through creative association."
        }
        print(f"Mercury sign interpretation for {sign}: {interpretations[sign]}")
        return interpretations[sign]

    def generate_basic_chart_interpretation(self, planet_positions, ascendant_sign, houses, planets_in_houses, aspects, gender):
        """Generate a basic interpretation of the birth chart"""
        sun_sign = planet_positions["Sun"]["sign"]
        moon_sign = planet_positions["Moon"]["sign"]
        mercury_sign = planet_positions["Mercury"]["sign"]

        interpretation = []

        # Sun sign interpretation
        sun_interp = self.interpret_sun_sign(sun_sign, gender)
        interpretation.append(f"SUN IN {sun_sign}:\n{sun_interp}")

        # Moon sign interpretation
        moon_interp = self.interpret_moon_sign(moon_sign)
        interpretation.append(f"MOON IN {moon_sign}:\n{moon_interp}")

        # Ascendant interpretation
        asc_interp = self.interpret_ascendant(ascendant_sign)
        interpretation.append(f"ASCENDANT IN {ascendant_sign}:\n{asc_interp}")

        # Mercury interpretation
        merc_interp = self.interpret_mercury(mercury_sign)
        interpretation.append(f"MERCURY IN {mercury_sign}:\n{merc_interp}")

        # House analysis
        interpretation.append("PLANETARY HOUSE PLACEMENTS:")
        for house, planets in planets_in_houses.items():
            if planets:
                planets_str = ", ".join(planets)
                interpretation.append(f"House {house} ({self.house_meanings[house]}): {planets_str}")

        # Major aspects
        interpretation.append("SIGNIFICANT PLANETARY ASPECTS:")
        for aspect in aspects:
            if aspect["aspect"] in ["Conjunction", "Opposition", "Square"]:
                interpretation.append(f"{aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (orb: {aspect['orb']}°)")
                interpretation.append(f"  This indicates {aspect['nature']} between your {self.planet_meanings[aspect['planet1']].split(',')[0].lower()} and {self.planet_meanings[aspect['planet2']].split(',')[0].lower()}.")

        print("Basic chart interpretation generated.")
        return "\n\n".join(interpretation)

    def create_birth_chart(self, birth_date, birth_time, birth_place, gender):
        """Create a birth chart from the provided information"""
        try:
            # Parse input
            year, month, day = birth_date
            hour, minute, second = birth_time

            # Get coordinates for birth place
            latitude, longitude = self.get_coordinates(birth_place)

            # Calculate Julian day
            jd, timezone = self.calculate_julian_day((year, month, day), (hour, minute, second), latitude, longitude)

            # Calculate houses and angles
            houses, ascendant, midheaven = self.calculate_houses(jd, latitude, longitude)

            # Determine ascendant sign
            asc_sign_num = int(ascendant / 30)
            ascendant_sign = self.signs[asc_sign_num]

            # Calculate planet positions
            planet_positions = self.calculate_planet_positions(jd)

            # Calculate aspects
            aspects = self.calculate_aspects(planet_positions)

            # Assign planets to houses
            planets_in_houses = self.assign_planets_to_houses(planet_positions, houses)

            # Generate interpretation
            interpretation = self.generate_basic_chart_interpretation(
                planet_positions, ascendant_sign, houses, planets_in_houses, aspects, gender
            )

            # Prepare result
            result = {
                "birth_info": {
                    "date": f"{day}/{month}/{year}",
                    "time": f"{hour:02d}:{minute:02d}:{second:02d}",
                    "place": birth_place,
                    "coordinates": f"{latitude:.4f}, {longitude:.4f}",
                    "timezone": timezone
                },
                "chart_data": {
                    "julian_day": jd,
                    "ascendant": {
                        "degree": ascendant,
                        "sign": ascendant_sign
                    },
                    "midheaven": {
                        "degree": midheaven,
                        "sign": self.signs[int(midheaven / 30)]
                    },
                    "houses": {i+1: houses[i] for i in range(12)},
                    "planets": planet_positions,
                    "aspects": aspects
                },
                "interpretation": interpretation
            }

            print("Birth chart created successfully.")
            return result

        except Exception as e:
            print(f"Error creating birth chart: {e}")
            return {"error": str(e)}

    
    def generate_weekly_prediction(self, birth_chart_data, start_date=None):
        """Generate a comprehensive weekly prediction based on birth chart and transits for each day of the week"""
        # Use current date as start date if not provided
        if start_date is None:
            start_date = datetime.datetime.now().replace(hour=12, minute=0, second=0)
        else:
            # Ensure we have a datetime object with noon time
            start_date = start_date.replace(hour=12, minute=0, second=0)
        
        # Create a list of dates for the week (7 days from start date)
        week_dates = [start_date + datetime.timedelta(days=i) for i in range(7)]
        
        # Get natal chart planets
        natal_planets = birth_chart_data["chart_data"]["planets"]
        
        # Track all transit aspects across the week
        all_week_aspects = []
        daily_transits = {}
        
        # Calculate transits for each day
        for day_date in week_dates:
            day_key = day_date.strftime("%A, %b %d")  # Format: Monday, Jan 15
            
            # Calculate Julian day for current date
            day_jd = swe.julday(day_date.year, day_date.month, day_date.day,
                        day_date.hour + day_date.minute / 60.0 + day_date.second / 3600.0)
            
            # Get planetary positions for this day
            day_planets = self.calculate_planet_positions(day_jd)
            
            # Calculate transit aspects (current planets to natal planets)
            day_transit_aspects = []
            for transit_planet, transit_data in day_planets.items():
                for natal_planet, natal_data in natal_planets.items():
                    # Calculate angle between transit planet and natal planet
                    angle = abs(transit_data["longitude"] - natal_data["longitude"])
                    if angle > 180:
                        angle = 360 - angle
                        
                    # Check for significant aspects
                    for aspect_name, aspect_info in self.aspects.items():
                        aspect_angle = aspect_info["angle"]
                        orb = aspect_info["orb"] * 0.8  # Tighter orbs for transits
                        
                        if abs(angle - aspect_angle) <= orb:
                            # Check if this aspect is applying or separating
                            is_applying = self._is_aspect_applying(
                                transit_planet, natal_planet, angle, aspect_angle, day_date
                            )
                            
                            day_transit_aspects.append({
                                "transit_planet": transit_planet,
                                "natal_planet": natal_planet,
                                "aspect": aspect_name,
                                "orb": round(abs(angle - aspect_angle), 2),
                                "is_applying": is_applying,
                                "date": day_date
                            })
            
            # Store transits for this day
            daily_transits[day_key] = day_transit_aspects
            all_week_aspects.extend(day_transit_aspects)
        
        # Get current planetary positions (for general week overview)
        start_jd = swe.julday(start_date.year, start_date.month, start_date.day,
                        start_date.hour + start_date.minute / 60.0 + start_date.second / 3600.0)
        current_planets = self.calculate_planet_positions(start_jd)
        
        # Generate week-long prediction
        prediction = self._interpret_weekly_transits_improved(
            all_week_aspects, daily_transits, natal_planets, current_planets, week_dates
        )
        
        return prediction

    def _is_aspect_applying(self, transit_planet, natal_planet, current_angle, aspect_angle, date):
        """Determine if an aspect is applying (getting closer) or separating (moving apart)"""
        # Calculate planet positions tomorrow
        tomorrow = date + datetime.timedelta(days=1)
        tomorrow_jd = swe.julday(tomorrow.year, tomorrow.month, tomorrow.day, 12.0)
        
        # Get transit planet position tomorrow
        tomorrow_planets = self.calculate_planet_positions(tomorrow_jd)
        if transit_planet not in tomorrow_planets:
            return False  # Cannot determine, assume separating
        
        tomorrow_pos = tomorrow_planets[transit_planet]["longitude"]
        
        # Get natal planet position (doesn't change)
        natal_pos = 0
        for planet, data in self.planets.items():
            if data == natal_planet:
                result, _ = swe.calc_ut(tomorrow_jd, planet)
                if isinstance(result, tuple) and len(result) > 0:
                    natal_pos = result[0]
                    break
        
        # Calculate tomorrow's angle
        tomorrow_angle = abs(tomorrow_pos - natal_pos)
        if tomorrow_angle > 180:
            tomorrow_angle = 360 - tomorrow_angle
        
        # Calculate orbs
        current_orb = abs(current_angle - aspect_angle)
        tomorrow_orb = abs(tomorrow_angle - aspect_angle)
        
        # If tomorrow's orb is smaller, the aspect is applying
        return tomorrow_orb < current_orb

    def _interpret_weekly_transits_improved(self, all_aspects, daily_transits, natal_planets, current_planets, week_dates):
        """Interpret transit aspects for a comprehensive weekly prediction"""
        predictions = []
        
        # Format date range for the week
        start_date_str = week_dates[0].strftime("%B %d")
        end_date_str = week_dates[-1].strftime("%B %d, %Y")
        
        predictions.append(f"WEEKLY PREDICTION: {start_date_str} - {end_date_str}")
        
        # General tone for the week based on sun and moon positions
        sun_sign = current_planets["Sun"]["sign"]
        moon_sign = current_planets["Moon"]["sign"]
        
        predictions.append(f"\nOVERVIEW: The Sun is in {sun_sign} this week, bringing focus to {self._get_house_theme_by_sign(sun_sign, natal_planets)}.")
        
        # Find key planetary events during the week
        retrograde_planets = self._check_retrograde_planets(week_dates)
        if retrograde_planets:
            predictions.append(f"\nNOTE: {', '.join(retrograde_planets)} {'is' if len(retrograde_planets) == 1 else 'are'} retrograde this week, which may impact related areas of life.")
        
        # Group aspects by planet to identify themes
        planet_aspects = {}
        for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
            planet_aspects[planet] = [a for a in all_aspects if a["transit_planet"] == planet]
        
        # Identify significant days
        significant_days = self._identify_significant_days(daily_transits)
        if significant_days:
            predictions.append("\nKEY DAYS THIS WEEK:")
            for day, significance in significant_days.items():
                predictions.append(f"• {day}: {significance}")
        
        # Generate daily insights
        predictions.append("\nDAILY INSIGHTS:")
        for day, aspects in daily_transits.items():
            if aspects:
                day_mood = self._get_day_mood(aspects)
                most_important = self._get_most_important_aspect(aspects)
                predictions.append(f"\n{day}: {day_mood}")
                if most_important:
                    predictions.append(f"  Focus: {self._interpret_transit_aspect(most_important, detailed=True)}")
        
        # Life area predictions based on the week's transits
        life_areas = {
            "Career & Goals": self._interpret_career_transits(all_aspects),
            "Relationships": self._interpret_relationship_transits(all_aspects),
            "Communication": self._interpret_communication_transits(all_aspects),
            "Home & Family": self._interpret_home_transits(all_aspects),
            "Personal Growth": self._interpret_growth_transits(all_aspects)
        }
        
        predictions.append("\nLIFE AREA FORECASTS:")
        for area, forecast in life_areas.items():
            if forecast:
                predictions.append(f"\n{area}: {forecast}")
        
        # Weekly advice based on dominant aspects
        predictions.append("\nWEEKLY ADVICE:")
        predictions.append(self._generate_weekly_advice_improved(all_aspects))
        
        return "\n".join(predictions)

    def _get_house_theme_by_sign(self, sign, natal_planets):
        """Get thematic focus based on sign relation to natal chart"""
        themes = {
            "Aries": "personal initiative and new beginnings",
            "Taurus": "resources and values",
            "Gemini": "communication and learning",
            "Cancer": "home and emotional foundations",
            "Leo": "creative expression and joy",
            "Virgo": "work and health routines",
            "Libra": "relationships and partnerships",
            "Scorpio": "transformation and shared resources",
            "Sagittarius": "expansion and belief systems",
            "Capricorn": "career and public standing",
            "Aquarius": "social connections and future goals",
            "Pisces": "spiritual growth and integration"
        }
        return themes[sign]

    def _check_retrograde_planets(self, week_dates):
        """Check which planets are retrograde during the week"""
        retrograde_planets = []
        
        # Check common retrograde planets - Mercury, Venus, Mars, Jupiter, Saturn
        planets_to_check = [swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]
        planet_names = {
            swe.MERCURY: "Mercury", 
            swe.VENUS: "Venus", 
            swe.MARS: "Mars",
            swe.JUPITER: "Jupiter", 
            swe.SATURN: "Saturn"
        }
        
        # Use the middle of the week to check
        mid_week = week_dates[3]
        mid_jd = swe.julday(mid_week.year, mid_week.month, mid_week.day, 12.0)
        
        for planet_id in planets_to_check:
            res, _ = swe.calc_ut(mid_jd, planet_id)
            if isinstance(res, tuple) and len(res) >= 4 and res[3] < 0:  # Negative speed indicates retrograde
                retrograde_planets.append(planet_names[planet_id])
        
        return retrograde_planets

    def _identify_significant_days(self, daily_transits):
        """Identify and explain particularly significant days in the week"""
        significant_days = {}
        
        for day, aspects in daily_transits.items():
            # Count aspects by type
            aspect_types = {}
            for a in aspects:
                aspect_types[a["aspect"]] = aspect_types.get(a["aspect"], 0) + 1
            
            # Check for days with many challenging aspects
            challenging = aspect_types.get("Square", 0) + aspect_types.get("Opposition", 0)
            flowing = aspect_types.get("Trine", 0) + aspect_types.get("Sextile", 0)
            
            # Check for moon aspects
            moon_aspects = [a for a in aspects if a["transit_planet"] == "Moon"]
            
            # Identify significant days
            if challenging >= 3 and flowing == 0:
                significant_days[day] = "Challenging day - prepare for obstacles"
            elif flowing >= 3 and challenging == 0:
                significant_days[day] = "Flowing day - good for important activities"
            elif len(moon_aspects) >= 3:
                significant_days[day] = "Emotionally significant day"
            
            # Check for Mercury aspects (communication days)
            mercury_aspects = [a for a in aspects if a["transit_planet"] == "Mercury"]
            if len(mercury_aspects) >= 2:
                significant_days[day] = "Important day for communication and decisions"
        
        return significant_days

    def _get_day_mood(self, aspects):
        """Determine the general mood or energy of a day based on its aspects"""
        # Count aspect types
        challenging = len([a for a in aspects if a["aspect"] in ["Square", "Opposition"]])
        flowing = len([a for a in aspects if a["aspect"] in ["Trine", "Sextile"]])
        neutral = len([a for a in aspects if a["aspect"] == "Conjunction"])
        
        # Check planetary influence
        has_moon = any(a["transit_planet"] == "Moon" for a in aspects)
        has_mars = any(a["transit_planet"] == "Mars" for a in aspects)
        has_venus = any(a["transit_planet"] == "Venus" for a in aspects)
        
        # Determine mood
        if challenging > flowing + 1:
            mood = "Challenging but productive" if has_mars else "Potentially difficult"
        elif flowing > challenging + 1:
            mood = "Harmonious and creative" if has_venus else "Smooth and flowing" 
        elif neutral > challenging and neutral > flowing:
            mood = "Intense and focused"
        elif has_moon:
            mood = "Emotionally significant"
        else:
            mood = "Relatively balanced"
            
        return mood

    def _get_most_important_aspect(self, aspects):
        """Determine the most important aspect of the day"""
        if not aspects:
            return None
            
        # Priority order of planets
        planet_priority = {
            "Sun": 10, "Moon": 9, "Mercury": 8, "Venus": 7, "Mars": 6,
            "Jupiter": 5, "Saturn": 4, "Uranus": 3, "Neptune": 2, "Pluto": 1
        }
        
        # Priority order of aspects
        aspect_priority = {
            "Conjunction": 5, "Opposition": 4, "Square": 3, "Trine": 2, "Sextile": 1
        }
        
        # Find aspect with highest priority
        highest_score = -1
        most_important = None
        
        for aspect in aspects:
            # Score based on planet and aspect type
            planet_score = planet_priority.get(aspect["transit_planet"], 0)
            aspect_score = aspect_priority.get(aspect["aspect"], 0)
            applying_bonus = 3 if aspect.get("is_applying", False) else 0
            orb_score = (1 - min(aspect["orb"], 8) / 8) * 2  # Tighter orbs get higher score
            
            total_score = planet_score + aspect_score + applying_bonus + orb_score
            
            if total_score > highest_score:
                highest_score = total_score
                most_important = aspect
                
        return most_important

    def _interpret_transit_aspect(self, aspect, detailed=False):
        """Interpret a single transit aspect with option for more detail"""
        transit_planet = aspect["transit_planet"]
        natal_planet = aspect["natal_planet"]
        aspect_type = aspect["aspect"]
        is_applying = aspect.get("is_applying", False)
        
        # Basic descriptions for aspect types
        aspect_meaning = {
            "Conjunction": "intensifies and activates",
            "Opposition": "creates tension and awareness with",
            "Trine": "flows harmoniously with",
            "Square": "challenges and motivates action with",
            "Sextile": "creates opportunities related to"
        }
        
        # Basic interpretation
        if transit_planet in self.planet_meanings and natal_planet in self.planet_meanings:
            transit_meaning = self.planet_meanings[transit_planet].split(',')[0].lower()
            natal_meaning = self.planet_meanings[natal_planet].split(',')[0].lower()
            
            basic = f"Transit {transit_planet} {aspect_type} {aspect_meaning[aspect_type]} your natal {natal_planet}"
            
            if not detailed:
                return basic
                
            # Add timing insight
            timing = "increasing in influence" if is_applying else "beginning to fade"
            
            # Add detailed meaning based on planets involved
            detail = f"This {aspect_type.lower()} brings {transit_meaning} into {aspect_meaning[aspect_type].split()[0]} relationship with your {natal_meaning}."
            
            return f"{basic} ({timing}). {detail}"
        else:
            return f"Transit {transit_planet} {aspect_type} natal {natal_planet}."

    def _interpret_career_transits(self, all_aspects):
        """Interpret transits related to career and public standing"""
        # Career related planets and houses
        career_planets = ["Sun", "Saturn", "Jupiter", "Mars"]
        career_aspects = []
        
        # Filter relevant aspects
        for aspect in all_aspects:
            if aspect["transit_planet"] in career_planets or aspect["natal_planet"] in career_planets:
                career_aspects.append(aspect)
        
        if not career_aspects:
            return "No significant career developments this week."
        
        # Count aspect types to determine overall tone
        challenging = len([a for a in career_aspects if a["aspect"] in ["Square", "Opposition"]])
        flowing = len([a for a in career_aspects if a["aspect"] in ["Trine", "Sextile"]])
        
        # Generate interpretation
        if challenging > flowing:
            interpretation = "You may face challenges in your professional life. Stay focused on long-term goals rather than immediate obstacles."
        elif flowing > challenging:
            interpretation = "Professional opportunities flow more easily this week. Take advantage of favorable conditions for advancement."
        else:
            interpretation = "Mixed career influences suggest staying adaptable while maintaining focus on current projects."
        
        # Add specific planet insights if present
        if any(a["transit_planet"] == "Saturn" for a in career_aspects):
            interpretation += " Authority figures or responsibilities require attention."
        if any(a["transit_planet"] == "Jupiter" for a in career_aspects):
            interpretation += " Look for growth opportunities or chances to expand your professional influence."
        
        return interpretation

    def _interpret_relationship_transits(self, all_aspects):
        """Interpret transits related to relationships and connections"""
        # Relationship related planets
        relationship_planets = ["Venus", "Mars", "Moon", "Jupiter"]
        relationship_aspects = []
        
        # Filter relevant aspects
        for aspect in all_aspects:
            if aspect["transit_planet"] in relationship_planets or aspect["natal_planet"] in relationship_planets:
                relationship_aspects.append(aspect)
        
        if not relationship_aspects:
            return "Relationships continue along established patterns this week."
        
        # Count aspect types
        challenging = len([a for a in relationship_aspects if a["aspect"] in ["Square", "Opposition"]])
        flowing = len([a for a in relationship_aspects if a["aspect"] in ["Trine", "Sextile"]])
        
        # Generate interpretation
        if challenging > flowing + 1:
            interpretation = "Relationship tensions may arise this week. Clear communication helps navigate differences."
        elif flowing > challenging + 1:
            interpretation = "Harmonious relationship energy supports deepening connections and resolving past issues."
        else:
            interpretation = "Balanced relationship influences suggest both meaningful connections and minor adjustments."
        
        # Add specific planet insights
        venus_aspects = [a for a in relationship_aspects if a["transit_planet"] == "Venus"]
        mars_aspects = [a for a in relationship_aspects if a["transit_planet"] == "Mars"]
        
        if venus_aspects:
            interpretation += " Pay attention to what brings joy and value in your connections."
        if mars_aspects:
            interpretation += " Physical energy and assertiveness play a role in your interactions."
        
        return interpretation

    def _interpret_communication_transits(self, all_aspects):
        """Interpret transits related to communication and learning"""
        # Communication related planets
        communication_planets = ["Mercury", "Moon", "Jupiter"]
        communication_aspects = []
        
        # Filter relevant aspects
        for aspect in all_aspects:
            if aspect["transit_planet"] in communication_planets:
                communication_aspects.append(aspect)
        
        if not communication_aspects:
            return "Communications proceed normally without significant cosmic influence."
        
        # Check for Mercury retrograde
        mercury_aspects = [a for a in communication_aspects if a["transit_planet"] == "Mercury"]
        is_mercury_retrograde = False  # This would need proper implementation
        
        # Generate interpretation
        if is_mercury_retrograde:
            interpretation = "With Mercury retrograde, double-check details and expect potential miscommunications."
        else:
            # Count aspect types
            challenging = len([a for a in communication_aspects if a["aspect"] in ["Square", "Opposition"]])
            flowing = len([a for a in communication_aspects if a["aspect"] in ["Trine", "Sextile"]])
            
            if challenging > flowing:
                interpretation = "Communication may require extra effort. Be mindful of how your words are received."
            elif flowing > challenging:
                interpretation = "Ideas flow more easily. This is a good time for writing, speaking, or important conversations."
            else:
                interpretation = "Mixed communication influences suggest balancing listening and expressing yourself."
        
        # Add specific insights
        if any(a["natal_planet"] == "Moon" for a in mercury_aspects):
            interpretation += " Emotions may color your communication style."
        if any(a["natal_planet"] == "Saturn" for a in mercury_aspects):
            interpretation += " Structured, serious discussions yield the best results."
        
        return interpretation

    def _interpret_home_transits(self, all_aspects):
        """Interpret transits related to home and family"""
        # Home related planets
        home_planets = ["Moon", "Venus", "Saturn"]
        home_aspects = []
        
        # Filter relevant aspects
        for aspect in all_aspects:
            if aspect["transit_planet"] in home_planets:
                home_aspects.append(aspect)
        
        if not home_aspects:
            return "Home and family matters continue along their current course."
        
        # Count aspect types
        challenging = len([a for a in home_aspects if a["aspect"] in ["Square", "Opposition"]])
        flowing = len([a for a in home_aspects if a["aspect"] in ["Trine", "Sextile"]])
        
        # Generate interpretation
        if challenging > flowing:
            interpretation = "Home or family situations may require extra attention and patience this week."
        elif flowing > challenging:
            interpretation = "Domestic harmony flows more easily. A good time for home improvements or family gatherings."
        else:
            interpretation = "Balance between comfort and responsibility characterizes your home environment."
        
        # Add specific insights
        moon_aspects = [a for a in home_aspects if a["transit_planet"] == "Moon"]
        if moon_aspects:
            interpretation += " Emotional needs connected to security and belonging are highlighted."
        
        return interpretation

    def _interpret_growth_transits(self, all_aspects):
        """Interpret transits related to personal growth and spirituality"""
        # Growth related planets
        growth_planets = ["Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        growth_aspects = []
        
        # Filter relevant aspects
        for aspect in all_aspects:
            if aspect["transit_planet"] in growth_planets:
                growth_aspects.append(aspect)
        
        if not growth_aspects:
            return "Focus on existing personal development paths this week."
        
        # Count aspect types by planet
        jupiter_aspects = [a for a in growth_aspects if a["transit_planet"] == "Jupiter"]
        saturn_aspects = [a for a in growth_aspects if a["transit_planet"] == "Saturn"]
        outer_aspects = [a for a in growth_aspects if a["transit_planet"] in ["Uranus", "Neptune", "Pluto"]]
        
        # Generate interpretation
        if jupiter_aspects and saturn_aspects:
            interpretation = "Balance expansion with structure in your personal growth. Learn from challenges while remaining optimistic."
        elif jupiter_aspects:
            interpretation = "Opportunities for expansion and meaningful growth appear this week. Follow your inspirations."
        elif saturn_aspects:
            interpretation = "Focus on discipline and making your growth practical and sustainable."
        elif outer_aspects:
            interpretation = "Deeper transformative processes are active. Pay attention to insights and subtle shifts."
        else:
            interpretation = "Mixed influences support steady progress on your personal journey."
        
        return interpretation

    def _generate_weekly_advice_improved(self, all_aspects):
        """Generate practical advice based on the week's overall transit pattern"""
        # Count aspects by type and planet
        aspect_counts = {}
        planet_counts = {}
        for aspect in all_aspects:
            aspect_counts[aspect["aspect"]] = aspect_counts.get(aspect["aspect"], 0) + 1
            planet_counts[aspect["transit_planet"]] = planet_counts.get(aspect["transit_planet"], 0) + 1
        
        # Determine dominant aspect type and planet
        dominant_aspect = max(aspect_counts.items(), key=lambda x: x[1])[0] if aspect_counts else None
        dominant_planet = max(planet_counts.items(), key=lambda x: x[1])[0] if planet_counts else None
        
        # Base advice on dominant aspect
        aspect_advice = {
            "Conjunction": "Focus your energy on new beginnings and developing clear intentions. Pay attention to what emerges strongly in your awareness.",
            "Opposition": "Seek balance between competing priorities. Be willing to see both sides of situations and find middle ground through compromise.",
            "Trine": "Take advantage of natural flow and harmony this week. Activities that usually feel challenging may come more easily now.",
            "Square": "Transform tension into productive action. Challenges this week contain hidden opportunities for growth if approached with flexibility.",
            "Sextile": "Look for small opportunities that could lead to larger developments. Making small efforts now can yield significant results."
        }
        
        # Additional advice based on dominant planet
        planet_advice = {
            "Sun": "Focus on authentic self-expression and your core purpose. Let your unique light shine.",
            "Moon": "Honor your emotional needs and intuitive insights. Create space for reflection and emotional processing.",
            "Mercury": "Pay special attention to communication and information. Express yourself clearly and listen carefully.",
            "Venus": "Cultivate harmony, pleasure, and appreciation in your life. Focus on what you truly value.",
            "Mars": "Channel your energy and initiative into meaningful action. Be direct but avoid unnecessary conflict.",
            "Jupiter": "Expand your horizons and look for opportunities for growth. Be optimistic but realistic.",
            "Saturn": "Focus on structure, discipline, and long-term planning. Take responsibility for your path."
        }
        
        # Generate comprehensive advice
        advice = []
        if dominant_aspect and dominant_aspect in aspect_advice:
            advice.append(aspect_advice[dominant_aspect])
        
        if dominant_planet and dominant_planet in planet_advice:
            advice.append(planet_advice[dominant_planet])
        
        # Add practical recommendation
        self_care_advice = "Make time for self-care practices that balance mind, body, and spirit. Small daily rituals can make a significant difference in navigating this week's energies."
        advice.append(self_care_advice)
        
        return " ".join(advice)

    def add_compatibility_analysis(self):
        """Add methods for compatibility analysis to the AstrologyTool class"""
        
        # Element compatibility scores (out of 10)
        self.element_compatibility = {
            ("Fire", "Fire"): 8,    # Enthusiastic but can burn out
            ("Fire", "Earth"): 4,   # Can be challenging but grounding
            ("Fire", "Air"): 9,     # Excellent synergy and stimulation
            ("Fire", "Water"): 3,   # Can create steam or extinguish
            
            ("Earth", "Fire"): 4,   # Earth can contain fire or smother it
            ("Earth", "Earth"): 7,  # Stable but can be too rigid
            ("Earth", "Air"): 3,    # Difficult combination
            ("Earth", "Water"): 8,  # Productive and nurturing
            
            ("Air", "Fire"): 9,     # Air feeds fire, creates inspiration
            ("Air", "Earth"): 3,    # Communication challenges
            ("Air", "Air"): 7,      # Intellectual but may lack grounding
            ("Air", "Water"): 5,    # Can be refreshing or stormy
            
            ("Water", "Fire"): 3,   # Water can extinguish fire's enthusiasm
            ("Water", "Earth"): 8,  # Nurturing and productive
            ("Water", "Air"): 5,    # Emotional understanding challenges
            ("Water", "Water"): 9,  # Deep emotional connection but can be overwhelming
        }
        
        # Quality compatibility scores (out of 10)
        self.quality_compatibility = {
            ("Cardinal", "Cardinal"): 5,  # Dynamic but challenging
            ("Cardinal", "Fixed"): 7,     # Balance between action and stability
            ("Cardinal", "Mutable"): 8,   # Action and adaptation work well
            
            ("Fixed", "Cardinal"): 7,     # Provides structure to initiative
            ("Fixed", "Fixed"): 4,        # Stable but stubborn combination
            ("Fixed", "Mutable"): 6,      # Balance between stability and flexibility
            
            ("Mutable", "Cardinal"): 8,   # Adaptability supports action
            ("Mutable", "Fixed"): 6,      # Flexibility meets determination
            ("Mutable", "Mutable"): 7,    # Adaptable but can lack direction
        }
        
        # Special aspects for relationships and their weights
        self.relationship_aspects = {
            # Sun-Moon connections are crucial for basic compatibility
            "Sun-Moon": 15,
            # Venus connections indicate love and attraction
            "Venus-Venus": 12,
            "Venus-Mars": 10,
            "Venus-Sun": 8,
            "Venus-Moon": 8,
            # Mars connections indicate physical chemistry
            "Mars-Mars": 7,
            "Mars-Moon": 6,
            "Mars-Sun": 6,
            # Mercury connections indicate communication
            "Mercury-Mercury": 9,
            "Mercury-Sun": 5,
            "Mercury-Moon": 5,
        }
        
        # Aspect weights for relationship compatibility
        self.aspect_weights = {
            "Conjunction": 10,
            "Opposition": 5,
            "Trine": 8,
            "Square": 3,
            "Sextile": 7
        }

    def analyze_compatibility(self, chart1, chart2):
        """Analyze compatibility between two birth charts
        
        Args:
            chart1: First person's chart data (from create_birth_chart)
            chart2: Second person's chart data (from create_birth_chart)
            
        Returns:
            Dictionary with compatibility analysis
        """
        if not hasattr(self, 'element_compatibility'):
            self.add_compatibility_analysis()
        
        # Extract relevant data from charts
        person1_planets = chart1["chart_data"]["planets"]
        person2_planets = chart2["chart_data"]["planets"]
        
        person1_sun = person1_planets["Sun"]["sign"]
        person1_moon = person1_planets["Moon"]["sign"]
        person1_mercury = person1_planets["Mercury"]["sign"]
        person1_venus = person1_planets["Venus"]["sign"]
        person1_mars = person1_planets["Mars"]["sign"]
        person1_ascendant = chart1["chart_data"]["ascendant"]["sign"]
        
        person2_sun = person2_planets["Sun"]["sign"]
        person2_moon = person2_planets["Moon"]["sign"]
        person2_mercury = person2_planets["Mercury"]["sign"]
        person2_venus = person2_planets["Venus"]["sign"]
        person2_mars = person2_planets["Mars"]["sign"]
        person2_ascendant = chart2["chart_data"]["ascendant"]["sign"]
        
        # Calculate synastry aspects between charts
        synastry_aspects = self.calculate_synastry_aspects(person1_planets, person2_planets)
        
        # Calculate element compatibility
        element_score = self.calculate_element_compatibility(person1_planets, person2_planets)
        
        # Calculate sign compatibility
        sign_score = self.calculate_sign_compatibility(
            person1_sun, person1_moon, person1_venus, person1_mars, person1_ascendant,
            person2_sun, person2_moon, person2_venus, person2_mars, person2_ascendant
        )
        
        # Calculate house overlays
        house_score = self.calculate_house_overlay_compatibility(chart1, chart2)
        
        # Calculate aspect compatibility
        aspect_score = self.calculate_aspect_compatibility(synastry_aspects)
        
        # Calculate special planetary relationships
        special_score = self.calculate_special_relationships(
            person1_sun, person1_moon, person1_mercury, person1_venus, person1_mars,
            person2_sun, person2_moon, person2_mercury, person2_venus, person2_mars
        )
        
        # Calculate overall compatibility percentage
        overall_score = self.calculate_overall_compatibility(
            element_score, sign_score, house_score, aspect_score, special_score
        )
        
        # Generate detailed interpretation
        interpretation = self.interpret_compatibility(
            person1_sun, person1_moon, person1_venus, person1_mars,
            person2_sun, person2_moon, person2_venus, person2_mars,
            synastry_aspects, overall_score
        )
        
        # Compile results
        compatibility_result = {
            "overall_compatibility": overall_score,
            "element_compatibility": element_score,
            "sign_compatibility": sign_score,
            "house_compatibility": house_score,
            "aspect_compatibility": aspect_score,
            "special_compatibility": special_score,
            "synastry_aspects": synastry_aspects,
            "interpretation": interpretation
        }
        
        return compatibility_result

    def calculate_synastry_aspects(self, person1_planets, person2_planets):
        """Calculate aspects between planets of two different charts"""
        synastry_aspects = []
        
        # Check aspects between each planet in person1's chart to each planet in person2's chart
        for planet1_name, planet1_data in person1_planets.items():
            for planet2_name, planet2_data in person2_planets.items():
                # Calculate the angle between planets
                long1 = planet1_data["longitude"]
                long2 = planet2_data["longitude"]
                
                # Find the shortest angle
                angle = abs(long1 - long2)
                if angle > 180:
                    angle = 360 - angle
                
                # Check if this angle forms an aspect
                for aspect_name, aspect_info in self.aspects.items():
                    aspect_angle = aspect_info["angle"]
                    orb = aspect_info["orb"]
                    
                    # Check if the angle is within the orb
                    if abs(angle - aspect_angle) <= orb:
                        synastry_aspects.append({
                            "person1_planet": planet1_name,
                            "person2_planet": planet2_name,
                            "aspect": aspect_name,
                            "orb": round(abs(angle - aspect_angle), 2),
                            "nature": aspect_info["nature"]
                        })
        
        return synastry_aspects

    def calculate_element_compatibility(self, person1_planets, person2_planets):
        """Calculate compatibility based on elements of key planets"""
        # Extract elements
        p1_sun_element = self.sign_elements[person1_planets["Sun"]["sign"]]
        p1_moon_element = self.sign_elements[person1_planets["Moon"]["sign"]]
        p1_venus_element = self.sign_elements[person1_planets["Venus"]["sign"]]
        
        p2_sun_element = self.sign_elements[person2_planets["Sun"]["sign"]]
        p2_moon_element = self.sign_elements[person2_planets["Moon"]["sign"]]
        p2_venus_element = self.sign_elements[person2_planets["Venus"]["sign"]]
        
        # Calculate element compatibility scores (weighted)
        sun_sun_score = self.element_compatibility[(p1_sun_element, p2_sun_element)] * 2
        sun_moon_score = self.element_compatibility[(p1_sun_element, p2_moon_element)] * 1.5
        moon_sun_score = self.element_compatibility[(p1_moon_element, p2_sun_element)] * 1.5
        moon_moon_score = self.element_compatibility[(p1_moon_element, p2_moon_element)] * 1.8
        venus_venus_score = self.element_compatibility[(p1_venus_element, p2_venus_element)] * 1.5
        
        # Calculate weighted average (out of 10)
        total_weight = 2 + 1.5 + 1.5 + 1.8 + 1.5
        element_score = (sun_sun_score + sun_moon_score + moon_sun_score + moon_moon_score + venus_venus_score) / total_weight
        
        # Convert to percentage
        element_percentage = (element_score / 10) * 100
        
        return round(element_percentage)

    def calculate_sign_compatibility(self, p1_sun, p1_moon, p1_venus, p1_mars, p1_asc, 
                                p2_sun, p2_moon, p2_venus, p2_mars, p2_asc):
        """Calculate compatibility based on sign relationships"""
        # Calculate position relationships
        compatibility_scores = []
        
        # Sun sign compatibility (traditional astrology uses polarity and angles)
        sun_compatibility = self._sign_relationship_score(p1_sun, p2_sun)
        compatibility_scores.append(sun_compatibility * 2)  # Double weight for Sun signs
        
        # Moon sign compatibility
        moon_compatibility = self._sign_relationship_score(p1_moon, p2_moon)
        compatibility_scores.append(moon_compatibility * 1.8)  # High weight for emotional harmony
        
        # Venus sign compatibility (love style)
        venus_compatibility = self._sign_relationship_score(p1_venus, p2_venus)
        compatibility_scores.append(venus_compatibility * 1.5)
        
        # Mars compatibility (sexual/energy harmony)
        mars_compatibility = self._sign_relationship_score(p1_mars, p2_mars)
        compatibility_scores.append(mars_compatibility * 1.3)
        
        # Venus-Mars cross compatibility (sexual attraction)
        venus_mars_compatibility = self._sign_relationship_score(p1_venus, p2_mars)
        mars_venus_compatibility = self._sign_relationship_score(p1_mars, p2_venus)
        compatibility_scores.append(venus_mars_compatibility * 1.4)
        compatibility_scores.append(mars_venus_compatibility * 1.4)
        
        # Sun-Moon cross compatibility (basic harmony)
        sun_moon_compatibility = self._sign_relationship_score(p1_sun, p2_moon)
        moon_sun_compatibility = self._sign_relationship_score(p1_moon, p2_sun)
        compatibility_scores.append(sun_moon_compatibility * 1.7)
        compatibility_scores.append(moon_sun_compatibility * 1.7)
        
        # Ascendant compatibility (how they view each other)
        asc_compatibility = self._sign_relationship_score(p1_asc, p2_asc)
        compatibility_scores.append(asc_compatibility)
        
        # Calculate weighted average
        total_weights = 2 + 1.8 + 1.5 + 1.3 + 1.4 + 1.4 + 1.7 + 1.7 + 1
        weighted_sum = sum(compatibility_scores)
        sign_compatibility = (weighted_sum / total_weights) * 10  # Scale to percentage
        
        return round(sign_compatibility)

    def _sign_relationship_score(self, sign1, sign2):
        """Calculate relationship score between two signs (based on traditional astrology)"""
        # Get positions in zodiac (0-11)
        sign_positions = {sign: i for i, sign in enumerate(self.signs)}
        pos1 = sign_positions[sign1]
        pos2 = sign_positions[sign2]
        
        # Calculate number of signs apart
        distance = (pos2 - pos1) % 12
        
        # Assign compatibility score based on aspect pattern
        if distance == 0:  # Conjunction (same sign)
            return 0.9  # High compatibility but can be too similar
        elif distance == 1 or distance == 11:  # Semisextile/Quincunx (1 sign apart)
            return 0.5  # Awkward adjustment needed
        elif distance == 2 or distance == 10:  # Sextile/Quincunx (2 signs apart)
            return 0.7  # Positive opportunity
        elif distance == 3 or distance == 9:  # Square (3 signs apart)
            return 0.4  # Challenge but growth
        elif distance == 4 or distance == 8:  # Trine (4 signs apart)
            return 0.9  # Harmony and flow
        elif distance == 5 or distance == 7:  # Quincunx (5 signs apart)
            return 0.3  # Adjustment needed
        elif distance == 6:  # Opposition (opposite signs)
            return 0.6  # Tension but attraction and balance
        
        return 0.5  # Default

    def calculate_house_overlay_compatibility(self, chart1, chart2):
        """Calculate compatibility based on house overlays"""
        # This is a simplified version of house overlay analysis
        # In a full implementation, we would check where each person's planets 
        # fall in the other person's houses
        
        # For simplicity, we'll focus on key relationship houses: 1, 5, 7, 8
        relationship_houses = [1, 5, 7, 8]
        house_score = 60  # Base score
        
        # Check planets in relationship houses
        planets_in_houses1 = chart1.get("planets_in_houses", {})
        planets_in_houses2 = chart2.get("planets_in_houses", {})
        
        benefics = ["Venus", "Jupiter"]
        malefics = ["Saturn", "Mars"]
        
        # Score adjustments based on planet placements
        for house in relationship_houses:
            # Person 1's planets in Person 2's houses
            for planet in planets_in_houses1.get(str(house), []):
                if planet in benefics:
                    house_score += 5
                elif planet in malefics:
                    house_score -= 2
            
            # Person 2's planets in Person 1's houses
            for planet in planets_in_houses2.get(str(house), []):
                if planet in benefics:
                    house_score += 5
                elif planet in malefics:
                    house_score -= 2
        
        # Ensure the score stays within 0-100 range
        return max(0, min(100, house_score))

    def calculate_aspect_compatibility(self, synastry_aspects):
        """Calculate compatibility based on synastry aspects"""
        aspect_score = 50  # Base score
        
        for aspect in synastry_aspects:
            p1_planet = aspect["person1_planet"]
            p2_planet = aspect["person2_planet"]
            aspect_type = aspect["aspect"]
            
            # Check if this is a significant relationship aspect
            planet_pair = f"{p1_planet}-{p2_planet}"
            reverse_pair = f"{p2_planet}-{p1_planet}"
            
            weight = 1.0  # Default weight
            
            # Check if this is a key relationship aspect
            if planet_pair in self.relationship_aspects:
                weight = self.relationship_aspects[planet_pair] / 10
            elif reverse_pair in self.relationship_aspects:
                weight = self.relationship_aspects[reverse_pair] / 10
            
            # Adjust score based on aspect type and nature
            if aspect_type in self.aspect_weights:
                aspect_value = self.aspect_weights[aspect_type]
                
                # Beneficial aspects add to score, challenging aspects subtract
                if aspect["nature"] == "Harmonious":
                    aspect_score += aspect_value * weight
                elif aspect["nature"] == "Challenging":
                    aspect_score -= aspect_value * weight * 0.5  # Reduce penalty for challenging aspects
                else:  # Neutral
                    aspect_score += aspect_value * weight * 0.3
        
        # Ensure the score stays within 0-100 range
        return max(0, min(100, round(aspect_score)))

    def calculate_special_relationships(self, p1_sun, p1_moon, p1_mercury, p1_venus, p1_mars,
                                    p2_sun, p2_moon, p2_mercury, p2_venus, p2_mars):
        """Calculate compatibility based on special planetary relationships"""
        special_score = 60  # Base score
        
        # Check for elemental matches in key planets
        sun_element_match = self.sign_elements[p1_sun] == self.sign_elements[p2_sun]
        moon_element_match = self.sign_elements[p1_moon] == self.sign_elements[p2_moon]
        venus_element_match = self.sign_elements[p1_venus] == self.sign_elements[p2_venus]
        mars_element_match = self.sign_elements[p1_mars] == self.sign_elements[p2_mars]
        
        # Check for elemental compatibility between important planets
        sun_venus_compatibility = self._get_element_compatibility_score(p1_sun, p2_venus)
        moon_venus_compatibility = self._get_element_compatibility_score(p1_moon, p2_venus)
        venus_mars_compatibility = self._get_element_compatibility_score(p1_venus, p2_mars)
        
        # Add scores for matches and compatibility
        if sun_element_match:
            special_score += 5
        if moon_element_match:
            special_score += 8
        if venus_element_match:
            special_score += 6
        if mars_element_match:
            special_score += 4
            
        # Add scores for cross-compatibility
        special_score += sun_venus_compatibility * 0.7
        special_score += moon_venus_compatibility * 0.8
        special_score += venus_mars_compatibility * 0.9
        
        # Check for same sign placements (can be both positive and negative)
        if p1_sun == p2_sun:
            special_score += 3
        if p1_moon == p2_moon:
            special_score += 5
        if p1_venus == p2_venus:
            special_score += 4
        if p1_mars == p2_mars:
            special_score += 2
        
        # Check for complementary communication styles
        if self._is_complementary(p1_mercury, p2_mercury):
            special_score += 6
        
        # Ensure the score stays within 0-100 range
        return max(0, min(100, round(special_score)))

    def _get_element_compatibility_score(self, sign1, sign2):
        """Get element compatibility score between two signs"""
        element1 = self.sign_elements[sign1]
        element2 = self.sign_elements[sign2]
        
        return self.element_compatibility[(element1, element2)]

    def _is_complementary(self, sign1, sign2):
        """Check if two signs are complementary (especially for Mercury)"""
        # Complementary pairs often involve different elements but compatible qualities
        element1 = self.sign_elements[sign1]
        element2 = self.sign_elements[sign2]
        
        quality1 = self.sign_qualities[sign1]
        quality2 = self.sign_qualities[sign2]
        
        # Different elements
        if element1 == element2:
            return False
        
        # Compatible qualities
        quality_compatibility = self.quality_compatibility[(quality1, quality2)]
        
        # Return true if quality compatibility is high
        return quality_compatibility >= 7

    def calculate_overall_compatibility(self, element_score, sign_score, house_score, aspect_score, special_score):
        """Calculate overall compatibility percentage"""
        # Weight the different components
        weights = {
            'element': 0.15,
            'sign': 0.25,
            'house': 0.15,
            'aspect': 0.30,
            'special': 0.15
        }
        
        # Calculate weighted score
        overall_score = (
            element_score * weights['element'] +
            sign_score * weights['sign'] +
            house_score * weights['house'] +
            aspect_score * weights['aspect'] +
            special_score * weights['special']
        )
        
        return round(overall_score)

    def interpret_compatibility(self, p1_sun, p1_moon, p1_venus, p1_mars,
                            p2_sun, p2_moon, p2_venus, p2_mars,
                            synastry_aspects, overall_score):
        """Generate detailed interpretation of the compatibility analysis"""
        interpretation = {}
        
        # Overall compatibility interpretation
        if overall_score >= 80:
            interpretation["overall"] = "Very high compatibility. This relationship has excellent potential with natural harmony and understanding."
        elif overall_score >= 70:
            interpretation["overall"] = "Strong compatibility. This relationship has good potential with some areas of natural connection."
        elif overall_score >= 60:
            interpretation["overall"] = "Moderate compatibility. This relationship has potential but may require work in certain areas."
        elif overall_score >= 50:
            interpretation["overall"] = "Average compatibility. This relationship may face challenges but also has strengths to build upon."
        else:
            interpretation["overall"] = "Challenging compatibility. This relationship may require significant effort and understanding to overcome differences."
        
        # Sun sign compatibility
        interpretation["sun_signs"] = f"Your {p1_sun} Sun and their {p2_sun} Sun indicates {self._interpret_sign_pair(p1_sun, p2_sun)}."
        
        # Moon sign compatibility
        interpretation["moon_signs"] = f"Your {p1_moon} Moon and their {p2_moon} Moon suggests {self._interpret_sign_pair(p1_moon, p2_moon)} on an emotional level."
        
        # Venus compatibility
        interpretation["venus"] = f"Your {p1_venus} Venus and their {p2_venus} Venus shows {self._interpret_sign_pair(p1_venus, p2_venus)} in terms of affection and values."
        
        # Mars compatibility
        interpretation["mars"] = f"Your {p1_mars} Mars and their {p2_mars} Mars indicates {self._interpret_sign_pair(p1_mars, p2_mars)} regarding energy and passion."
        
        # Significant aspects
        interpretation["key_aspects"] = self._interpret_key_aspects(synastry_aspects)
        
        return interpretation

    def _interpret_sign_pair(self, sign1, sign2):
        """Generate interpretation for a pair of signs"""
        # Get elements and qualities
        element1 = self.sign_elements[sign1]
        element2 = self.sign_elements[sign2]
        
        quality1 = self.sign_qualities[sign1]
        quality2 = self.sign_qualities[sign2]
        
        # Calculate elemental compatibility
        elem_score = self.element_compatibility[(element1, element2)]
        quality_score = self.quality_compatibility[(quality1, quality2)]
        
        # Generate interpretation based on scores
        if elem_score >= 8:
            element_text = "strong natural harmony"
        elif elem_score >= 6:
            element_text = "good compatibility"
        elif elem_score >= 4:
            element_text = "moderate interaction"
        else:
            element_text = "potential challenges"
        
        if quality_score >= 7:
            quality_text = "complementary approaches"
        elif quality_score >= 5:
            quality_text = "workable dynamics"
        else:
            quality_text = "potential friction in approaches"
        
        return f"{element_text} with {quality_text}"

    def _interpret_key_aspects(self, synastry_aspects):
        """Interpret the most significant aspects in the synastry"""
        key_interpretations = []
        
        # Find the most significant aspects
        significant_aspects = []
        for aspect in synastry_aspects:
            p1_planet = aspect["person1_planet"]
            p2_planet = aspect["person2_planet"]
            aspect_type = aspect["aspect"]
            
            # Check if this is a key relationship aspect
            planet_pair = f"{p1_planet}-{p2_planet}"
            reverse_pair = f"{p2_planet}-{p1_planet}"
            
            significance = 0
            
            if planet_pair in self.relationship_aspects:
                significance = self.relationship_aspects[planet_pair]
            elif reverse_pair in self.relationship_aspects:
                significance = self.relationship_aspects[reverse_pair]
            
            if significance > 0:
                significant_aspects.append((aspect, significance))
        
        # Sort by significance
        significant_aspects.sort(key=lambda x: x[1], reverse=True)
        
        # Take the top 5 most significant aspects
        for aspect_info, _ in significant_aspects[:5]:
            aspect = aspect_info["aspect"]
            p1_planet = aspect_info["person1_planet"]
            p2_planet = aspect_info["person2_planet"]
            nature = aspect_info["nature"]
            
            # Generate interpretation
            if nature == "Harmonious":
                aspect_text = "harmonious"
            elif nature == "Challenging":
                aspect_text = "challenging"
            else:
                aspect_text = "neutral"
            
            interpretation = f"Your {p1_planet} {aspect} their {p2_planet}: {self._get_aspect_meaning(p1_planet, p2_planet, aspect, nature)}"
            key_interpretations.append(interpretation)
        
        return key_interpretations

    def _get_aspect_meaning(self, planet1, planet2, aspect, nature):
        """Get the specific meaning of an aspect between two planets in synastry"""
        # This would ideally be a comprehensive dictionary of aspect interpretations
        # For now, we'll provide some examples for common combinations
        
        aspect_meanings = {
            "Sun-Moon-Conjunction": "Strong emotional connection and mutual understanding.",
            "Sun-Moon-Trine": "Natural flow of energy between identity and emotions.",
            "Sun-Moon-Square": "Tension between needs and expression that can lead to growth.",
            "Sun-Venus-Conjunction": "Strong attraction and harmony in values.",
            "Moon-Venus-Conjunction": "Deep emotional connection and shared sense of beauty.",
            "Venus-Mars-Conjunction": "Powerful physical and romantic attraction.",
            "Venus-Mars-Trine": "Natural flow of give and take in the relationship.",
            "Venus-Mars-Square": "Passionate but potentially challenging romantic dynamic.",
            "Mercury-Mercury-Conjunction": "Like-minded thinking and easy communication.",
            "Mercury-Mercury-Opposition": "Different perspectives that can complement each other.",
            "Mercury-Mercury-Square": "Communication challenges that require patience."
        }
        
        # Check for specific interpretation
        key = f"{planet1}-{planet2}-{aspect}"
        reverse_key = f"{planet2}-{planet1}-{aspect}"
        
        if key in aspect_meanings:
            return aspect_meanings[key]
        elif reverse_key in aspect_meanings:
            return aspect_meanings[reverse_key]
        
        # Generic interpretation based on planets and aspect nature
        return f"A {nature.lower()} {aspect.lower()} suggesting {self._generic_planet_interaction(planet1, planet2, nature)}"

    def _generic_planet_interaction(self, planet1, planet2, nature):
        """Generate generic interpretation for planet interaction"""
        planet_domains = {
            "Sun": "identity and vitality",
            "Moon": "emotions and needs",
            "Mercury": "communication and thinking",
            "Venus": "love and values",
            "Mars": "action and desire",
            "Jupiter": "growth and expansion",
            "Saturn": "structure and responsibility",
            "Uranus": "innovation and freedom",
            "Neptune": "dreams and spirituality",
            "Pluto": "transformation and power"
        }
        
        domain1 = planet_domains.get(planet1, "expression")
        domain2 = planet_domains.get(planet2, "reception")
        
        if nature == "Harmonious":
            return f"positive flow between {domain1} and {domain2}"
        elif nature == "Challenging":
            return f"growth opportunity through tension between {domain1} and {domain2}"
        else:
            return f"dynamic interaction between {domain1} and {domain2}"

    def plot_astral_chart(self, chart_data):
        """Plot the astral chart with planets, houses, and aspect lines."""
        planets = chart_data["planets"]
        houses = chart_data["houses"]
        ascendant = chart_data["ascendant"]
        midheaven = chart_data["midheaven"]
        aspects = chart_data["aspects"]

        # Create a polar plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))

        # Plot the houses
        for i in range(1, 13):
            start_angle = np.deg2rad(houses[i])  # Access houses using the correct key (1-12)
            end_angle = np.deg2rad(houses[(i % 12) + 1])  # Wrap around for the last house
            ax.bar(start_angle, 1, width=end_angle - start_angle, alpha=0.2, label=f'House {i}')

        # Plot the planets
        for planet, data in planets.items():
            angle = np.deg2rad(data["longitude"])
            ax.plot(angle, 0.9, 'o', markersize=10, label=planet)

        # Plot the Ascendant and Midheaven
        ax.plot(np.deg2rad(ascendant["degree"]), 1, 's', markersize=10, label='Ascendant')
        ax.plot(np.deg2rad(midheaven["degree"]), 1, 'd', markersize=10, label='Midheaven')

        # Define aspect colors and styles
        aspect_colors = {
            "Conjunction": "red",
            "Opposition": "blue",
            "Trine": "green",
            "Square": "orange",
            "Sextile": "purple"
        }

        # Draw aspect lines between planets
        for aspect in aspects:
            planet1 = aspect["planet1"]
            planet2 = aspect["planet2"]
            aspect_type = aspect["aspect"]

            # Get the angles of the two planets
            angle1 = np.deg2rad(planets[planet1]["longitude"])
            angle2 = np.deg2rad(planets[planet2]["longitude"])

            # Draw a line between the two planets
            ax.plot([angle1, angle2], [0.9, 0.9], color=aspect_colors[aspect_type], linestyle='-', linewidth=2, 
                    label=f'{planet1}-{planet2} {aspect_type}')

        # Set the direction of the plot (clockwise)
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')

        # Add labels and legend
        ax.set_title("Astral Chart with Aspects", va='bottom')
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

        # Show the plot
        plt.show()


def get_individual_chart(tool):
    """Get birth information and generate birth chart"""
    print("\nEnter birth date:")
    year = int(input("Year (e.g., 1990): "))
    month = int(input("Month (1-12): "))
    day = int(input("Day (1-31): "))

    print("\nEnter birth time:")
    hour = int(input("Hour (0-23): "))
    minute = int(input("Minute (0-59): "))
    second = int(input("Second (0-59, or 0 if unknown): "))

    birth_place = input("\nEnter birth place (City, Country): ")
    gender = input("\nEnter gender (Male/Female/Other): ")

    # Generate chart
    print("\nGenerating birth chart...")
    return tool.create_birth_chart((year, month, day), (hour, minute, second), birth_place, gender)


def display_individual_results(tool, result):
    """Display individual birth chart results"""
    if "error" in result:
        print(f"\nError: {result['error']}")
        return

    print("\n=== Birth Chart ===")
    print(f"\nBirth Information:")
    print(f"Date: {result['birth_info']['date']}")
    print(f"Time: {result['birth_info']['time']}")
    print(f"Place: {result['birth_info']['place']}")
    print(f"Coordinates: {result['birth_info']['coordinates']}")
    print(f"Timezone: {result['birth_info']['timezone']}")

    print("\n=== Chart Interpretation ===")
    print(result['interpretation'])

    # Ask for weekly prediction
    weekly_pred_response = input("\nWould you like a prediction for the coming week? (y/n): ")
    weekly_prediction = None
    if weekly_pred_response.lower() == 'y':
        print("\nGenerating weekly prediction...")
        weekly_prediction = tool.generate_weekly_prediction(result)
        print("\n=== Your Weekly Prediction ===")
        print(weekly_prediction)

    # Save to file option
    save = input("\nWould you like to save this interpretation to a file? (y/n): ")
    if save.lower() == 'y':
        # Ensure the date is correctly formatted
        year, month, day = result['birth_info']['date'].split("/")
        filename = f"birthchart_{year}_{month}_{day}.txt"
        with open(filename, 'w') as f:
            f.write("=== BIRTH CHART INTERPRETATION ===\n\n")
            f.write(f"Birth Date: {result['birth_info']['date']}\n")
            f.write(f"Birth Time: {result['birth_info']['time']}\n")
            f.write(f"Birth Place: {result['birth_info']['place']}\n\n")
            f.write(result['interpretation'])

            # Include weekly prediction in file if it was generated
            if weekly_prediction:
                f.write("\n\n=== WEEKLY PREDICTION ===\n\n")
                f.write(weekly_prediction)

        print(f"\nInterpretation saved to {filename}")


def display_compatibility_results(compatibility, chart1, chart2):
    """Display compatibility analysis results"""
    person1_name = input("\nEnter name for first person: ")
    person2_name = input("Enter name for second person: ")
    
    print(f"\n=== Compatibility Analysis: {person1_name} & {person2_name} ===")
    
    # Overall compatibility
    print(f"\nOverall Compatibility: {compatibility['overall_compatibility']}%")
    print(compatibility['interpretation']['overall'])
    
    # Element compatibility
    print(f"\nElemental Compatibility: {compatibility['element_compatibility']}%")
    
    # Sign compatibility
    print(f"\nSign Compatibility: {compatibility['sign_compatibility']}%")
    print(f"* Sun Signs: {compatibility['interpretation']['sun_signs']}")
    print(f"* Moon Signs: {compatibility['interpretation']['moon_signs']}")
    print(f"* Venus: {compatibility['interpretation']['venus']}")
    print(f"* Mars: {compatibility['interpretation']['mars']}")
    
    # Key aspects
    print("\nKey Aspects in Your Relationship:")
    for aspect in compatibility['interpretation']['key_aspects']:
        print(f"* {aspect}")
    
    # Save option
    save = input("\nWould you like to save this compatibility analysis to a file? (y/n): ")
    if save.lower() == 'y':
        filename = f"compatibility_{person1_name}_{person2_name}.txt"
        with open(filename, 'w') as f:
            f.write(f"=== COMPATIBILITY ANALYSIS: {person1_name.upper()} & {person2_name.upper()} ===\n\n")
            
            # Birth information
            f.write("--- Birth Information ---\n\n")
            f.write(f"{person1_name}:\n")
            f.write(f"Date: {chart1['birth_info']['date']}\n")
            f.write(f"Time: {chart1['birth_info']['time']}\n")
            f.write(f"Place: {chart1['birth_info']['place']}\n\n")
            
            f.write(f"{person2_name}:\n")
            f.write(f"Date: {chart2['birth_info']['date']}\n")
            f.write(f"Time: {chart2['birth_info']['time']}\n")
            f.write(f"Place: {chart2['birth_info']['place']}\n\n")
            
            # Compatibility scores
            f.write("--- Compatibility Scores ---\n\n")
            f.write(f"Overall Compatibility: {compatibility['overall_compatibility']}%\n")
            f.write(f"Element Compatibility: {compatibility['element_compatibility']}%\n")
            f.write(f"Sign Compatibility: {compatibility['sign_compatibility']}%\n")
            f.write(f"House Compatibility: {compatibility['house_compatibility']}%\n")
            f.write(f"Aspect Compatibility: {compatibility['aspect_compatibility']}%\n")
            f.write(f"Special Compatibility: {compatibility['special_compatibility']}%\n\n")
            
            # Interpretation
            f.write("--- Interpretation ---\n\n")
            f.write(f"Overall: {compatibility['interpretation']['overall']}\n\n")
            f.write(f"Sun Signs: {compatibility['interpretation']['sun_signs']}\n")
            f.write(f"Moon Signs: {compatibility['interpretation']['moon_signs']}\n")
            f.write(f"Venus: {compatibility['interpretation']['venus']}\n")
            f.write(f"Mars: {compatibility['interpretation']['mars']}\n\n")
            
            # Key aspects
            f.write("Key Aspects:\n")
            for aspect in compatibility['interpretation']['key_aspects']:
                f.write(f"* {aspect}\n")
                
        print(f"\nCompatibility analysis saved to {filename}")
    
    # Option to go back to the main menu
    go_back = input("\nWould you like to return to the main menu? (y/n): ")
    if go_back.lower() == 'y':
        generate_astrological_profile()


def generate_astrological_profile():
    """Interactive function to generate an astrological profile, plot the chart, and analyze compatibility."""
    print("=== Astrological Birth Chart Generator ===")
    print("1. Generate individual birth chart")
    print("2. Analyze compatibility between two people")
    choice = input("Choose an option (1 or 2): ")
    
    # Create astrology tool
    tool = AstrologyTool()
    
    if choice == "1":
        # Generate individual birth chart
        result = get_individual_chart(tool)
        if "error" not in result:
            display_individual_results(tool, result)
            # Plot the astral chart
            tool.plot_astral_chart(result["chart_data"])
        else:
            print(f"\nError: {result['error']}")
    
    elif choice == "2":
        # Generate compatibility analysis
        print("\n=== Compatibility Analysis ===")
        print("\nEnter details for the first person:")
        result1 = get_individual_chart(tool)
        
        print("\nEnter details for the second person:")
        result2 = get_individual_chart(tool)
        
        # Check if both charts were generated successfully
        if "error" not in result1 and "error" not in result2:
            print("\nCalculating compatibility...")
            compatibility = tool.analyze_compatibility(result1, result2)
            display_compatibility_results(compatibility, result1, result2)
        else:
            if "error" in result1:
                print(f"\nError in first chart: {result1['error']}")
            if "error" in result2:
                print(f"\nError in second chart: {result2['error']}")
    
    else:
        print("Invalid option selected.")

