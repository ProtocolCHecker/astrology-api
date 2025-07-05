from datetime import datetime
import random
import json

class ProfessionalHoroscopeGenerator:
    def __init__(self, latitude=40.7128, longitude=-74.0060):
        self.latitude = latitude
        self.longitude = longitude

        self.ZODIAC = {
            'Aries': {
                'traits': ['Bold', 'Courageous', 'Competitive', 'Impulsive', 'Independent'],
                'ruling_planet': 'Mars',
                'element': 'Fire',
                'quality': 'Cardinal',
                'house': 1,
                'dates': [(3, 21), (4, 19)]
            },
            'Taurus': {
                'traits': ['Grounded', 'Reliable', 'Patient', 'Sensual', 'Stubborn'],
                'ruling_planet': 'Venus',
                'element': 'Earth',
                'quality': 'Fixed',
                'house': 2,
                'dates': [(4, 20), (5, 20)]
            },
            'Gemini': {
                'traits': ['Curious', 'Adaptable', 'Communicative', 'Versatile', 'Restless'],
                'ruling_planet': 'Mercury',
                'element': 'Air',
                'quality': 'Mutable',
                'house': 3,
                'dates': [(5, 21), (6, 20)]
            },
            'Cancer': {
                'traits': ['Intuitive', 'Nurturing', 'Protective', 'Emotional', 'Loyal'],
                'ruling_planet': 'Moon',
                'element': 'Water',
                'quality': 'Cardinal',
                'house': 4,
                'dates': [(6, 21), (7, 22)]
            },
            'Leo': {
                'traits': ['Confident', 'Creative', 'Generous', 'Dramatic', 'Proud'],
                'ruling_planet': 'Sun',
                'element': 'Fire',
                'quality': 'Fixed',
                'house': 5,
                'dates': [(7, 23), (8, 22)]
            },
            'Virgo': {
                'traits': ['Practical', 'Analytical', 'Meticulous', 'Helpful', 'Critical'],
                'ruling_planet': 'Mercury',
                'element': 'Earth',
                'quality': 'Mutable',
                'house': 6,
                'dates': [(8, 23), (9, 22)]
            },
            'Libra': {
                'traits': ['Diplomatic', 'Social', 'Aesthetic', 'Balanced', 'Indecisive'],
                'ruling_planet': 'Venus',
                'element': 'Air',
                'quality': 'Cardinal',
                'house': 7,
                'dates': [(9, 23), (10, 22)]
            },
            'Scorpio': {
                'traits': ['Passionate', 'Resourceful', 'Intuitive', 'Mysterious', 'Intense'],
                'ruling_planet': 'Pluto',
                'element': 'Water',
                'quality': 'Fixed',
                'house': 8,
                'dates': [(10, 23), (11, 21)]
            },
            'Sagittarius': {
                'traits': ['Optimistic', 'Adventurous', 'Philosophical', 'Direct', 'Restless'],
                'ruling_planet': 'Jupiter',
                'element': 'Fire',
                'quality': 'Mutable',
                'house': 9,
                'dates': [(11, 22), (12, 21)]
            },
            'Capricorn': {
                'traits': ['Disciplined', 'Tenacious', 'Independent', 'Practical', 'Ambitious'],
                'ruling_planet': 'Saturn',
                'element': 'Earth',
                'quality': 'Cardinal',
                'house': 10,
                'dates': [(12, 22), (1, 19)]
            },
            'Aquarius': {
                'traits': ['Innovative', 'Original', 'Visionary', 'Independent', 'Detached'],
                'ruling_planet': 'Uranus',
                'element': 'Air',
                'quality': 'Fixed',
                'house': 11,
                'dates': [(1, 20), (2, 18)]
            },
            'Pisces': {
                'traits': ['Empathetic', 'Imaginative', 'Gentle', 'Intuitive', 'Dreamy'],
                'ruling_planet': 'Neptune',
                'element': 'Water',
                'quality': 'Mutable',
                'house': 12,
                'dates': [(2, 19), (3, 20)]
            }
        }

        self.PLANETS = {
            'Sun': {'themes': ['identity', 'vitality', 'purpose', 'ego', 'leadership'], 'cycle_days': 365.25},
            'Moon': {'themes': ['emotions', 'intuition', 'habits', 'security', 'nurturing'], 'cycle_days': 29.5},
            'Mercury': {'themes': ['communication', 'thinking', 'learning', 'travel', 'technology'], 'cycle_days': 88},
            'Venus': {'themes': ['love', 'beauty', 'relationships', 'values', 'harmony'], 'cycle_days': 225},
            'Mars': {'themes': ['action', 'energy', 'conflict', 'passion', 'courage'], 'cycle_days': 687},
            'Jupiter': {'themes': ['expansion', 'wisdom', 'luck', 'philosophy', 'growth'], 'cycle_days': 4333},
            'Saturn': {'themes': ['discipline', 'restrictions', 'lessons', 'responsibility', 'structure'], 'cycle_days': 10759},
            'Uranus': {'themes': ['innovation', 'rebellion', 'sudden change', 'freedom', 'technology'], 'cycle_days': 30687},
            'Neptune': {'themes': ['spirituality', 'illusion', 'creativity', 'compassion', 'dreams'], 'cycle_days': 60190},
            'Pluto': {'themes': ['transformation', 'power', 'rebirth', 'intensity', 'hidden truths'], 'cycle_days': 90560}
        }

        self.HOUSES = {
            1: {'themes': ['self', 'appearance', 'first impressions', 'new beginnings']},
            2: {'themes': ['money', 'possessions', 'values', 'self-worth']},
            3: {'themes': ['communication', 'siblings', 'short trips', 'learning']},
            4: {'themes': ['home', 'family', 'roots', 'emotional foundation']},
            5: {'themes': ['creativity', 'romance', 'children', 'fun', 'self-expression']},
            6: {'themes': ['work', 'health', 'daily routine', 'service']},
            7: {'themes': ['partnerships', 'marriage', 'open enemies', 'cooperation']},
            8: {'themes': ['transformation', 'shared resources', 'intimacy', 'mystery']},
            9: {'themes': ['philosophy', 'higher learning', 'travel', 'spiritual growth']},
            10: {'themes': ['career', 'reputation', 'authority', 'public image']},
            11: {'themes': ['friendships', 'groups', 'hopes', 'social networks']},
            12: {'themes': ['spirituality', 'hidden enemies', 'subconscious', 'sacrifice']}
        }

        self.ASPECTS = {
            'conjunction': {'angle': 0, 'orb': 8, 'nature': 'neutral', 'strength': 'very strong'},
            'sextile': {'angle': 60, 'orb': 6, 'nature': 'harmonious', 'strength': 'moderate'},
            'square': {'angle': 90, 'orb': 8, 'nature': 'challenging', 'strength': 'strong'},
            'trine': {'angle': 120, 'orb': 8, 'nature': 'harmonious', 'strength': 'strong'},
            'opposition': {'angle': 180, 'orb': 8, 'nature': 'challenging', 'strength': 'very strong'}
        }

        self.DAILY_INFLUENCES = {
            'Sun': {
                'Fire': "Solar energy ignites your fire sign passion—lead with confidence.",
                'Earth': "The Sun illuminates practical matters—focus on tangible achievements.",
                'Air': "Solar radiance enhances communication—share your ideas boldly.",
                'Water': "The Sun's warmth nurtures your emotional depth—trust your feelings."
            },
            'Moon': {
                'Fire': "Lunar energy may dampen your fire—channel emotions into creative action.",
                'Earth': "The Moon supports your grounded nature—trust your instincts about security.",
                'Air': "Lunar influence brings emotional depth to your thoughts—listen to your heart.",
                'Water': "The Moon amplifies your intuitive powers—go with the flow of your feelings."
            },
            'Mercury': {
                'Fire': "Mercury speeds up your thinking—act on your bright ideas quickly.",
                'Earth': "Mercury brings clarity to practical plans—organize your thoughts methodically.",
                'Air': "Mercury enhances your natural communication gifts—network and connect.",
                'Water': "Mercury stirs your emotional intelligence—express your feelings clearly."
            },
            'Venus': {
                'Fire': "Venus softens your fiery nature—approach conflicts with charm.",
                'Earth': "Venus highlights beauty and comfort—indulge in life's pleasures.",
                'Air': "Venus enhances your social magnetism—relationships flourish.",
                'Water': "Venus deepens emotional connections—open your heart to love."
            },
            'Mars': {
                'Fire': "Mars amplifies your natural drive—channel this energy constructively.",
                'Earth': "Mars pushes for action in practical matters—tackle your to-do list.",
                'Air': "Mars energizes your communication—speak up and be heard.",
                'Water': "Mars stirs deep emotions—find healthy outlets for intensity."
            },
            'Jupiter': {
                'Fire': "Jupiter expands your optimistic nature—take calculated risks.",
                'Earth': "Jupiter brings growth to practical ventures—invest in your future.",
                'Air': "Jupiter broadens your intellectual horizons—learn something new.",
                'Water': "Jupiter enhances your compassion—extend kindness to others."
            },
            'Saturn': {
                'Fire': "Saturn teaches patience—slow down and plan carefully.",
                'Earth': "Saturn supports your disciplined nature—build solid foundations.",
                'Air': "Saturn brings structure to your ideas—commit to your plans.",
                'Water': "Saturn encourages emotional maturity—face your feelings honestly."
            }
        }

    def calculate_planetary_position(self, planet, date):
        reference_date = datetime(2000, 1, 1)
        days_since_reference = (date - reference_date).days

        cycle_days = self.PLANETS[planet]['cycle_days']
        position = (days_since_reference % cycle_days) / cycle_days * 360

        return position % 360

    def calculate_lunar_phase(self, date):
        reference_new_moon = datetime(2000, 1, 6)
        days_since_new_moon = (date - reference_new_moon).days

        lunar_cycle = 29.5
        phase_position = (days_since_new_moon % lunar_cycle) / lunar_cycle

        if phase_position < 0.125:
            return "New Moon"
        elif phase_position < 0.375:
            return "Waxing Crescent"
        elif phase_position < 0.625:
            return "Full Moon"
        elif phase_position < 0.875:
            return "Waning Crescent"
        else:
            return "New Moon"

    def get_sign_from_position(self, position):
        sign_index = int(position // 30)
        signs = list(self.ZODIAC.keys())
        return signs[sign_index % 12]

    def calculate_daily_aspects(self, date):
        aspects = []
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

        positions = {}
        for planet in planets:
            positions[planet] = self.calculate_planetary_position(planet, date)

        for i, planet1 in enumerate(planets):
            for planet2 in planets[i+1:]:
                pos1 = positions[planet1]
                pos2 = positions[planet2]

                diff = abs(pos1 - pos2)
                if diff > 180:
                    diff = 360 - diff

                for aspect_name, aspect_data in self.ASPECTS.items():
                    target_angle = aspect_data['angle']
                    orb = aspect_data['orb']

                    if abs(diff - target_angle) <= orb:
                        aspects.append({
                            'planet1': planet1,
                            'planet2': planet2,
                            'aspect': aspect_name,
                            'nature': aspect_data['nature'],
                            'strength': aspect_data['strength']
                        })
                        break

        return aspects

    def get_daily_planetary_emphasis(self, date):
        day_of_year = date.timetuple().tm_yday

        weekday_rulers = {
            0: 'Moon',
            1: 'Mars',
            2: 'Mercury',
            3: 'Jupiter',
            4: 'Venus',
            5: 'Saturn',
            6: 'Sun'
        }

        primary_planet = weekday_rulers[date.weekday()]

        lunar_phase = self.calculate_lunar_phase(date)
        secondary_influences = {
            'New Moon': 'Saturn',
            'Waxing Crescent': 'Jupiter',
            'Full Moon': 'Moon',
            'Waning Crescent': 'Neptune'
        }

        secondary_planet = secondary_influences.get(lunar_phase, 'Mercury')

        return primary_planet, secondary_planet

    def generate_interpretation(self, sign, date):
        sign_data = self.ZODIAC[sign]

        primary_planet, secondary_planet = self.get_daily_planetary_emphasis(date)
        lunar_phase = self.calculate_lunar_phase(date)
        aspects = self.calculate_daily_aspects(date)

        interpretations = []

        if primary_planet in self.DAILY_INFLUENCES:
            element = sign_data['element']
            if element in self.DAILY_INFLUENCES[primary_planet]:
                interpretations.append(self.DAILY_INFLUENCES[primary_planet][element])

        ruling_planet = sign_data['ruling_planet']
        if ruling_planet == primary_planet:
            interpretations.append(f"Your ruling planet {ruling_planet} is especially active today, amplifying your natural {sign_data['element'].lower()} energy.")
        elif ruling_planet == secondary_planet:
            interpretations.append(f"Your ruling planet {ruling_planet} provides supportive energy for personal growth.")

        lunar_influences = {
            'New Moon': "New beginnings and fresh starts are highlighted—plant seeds for future growth.",
            'Waxing Crescent': "Building momentum and growing energy support your current projects.",
            'Full Moon': "Emotional intensity and culmination energy reach their peak—embrace transformation.",
            'Waning Crescent': "Release and letting go create space for renewal—clear away what no longer serves."
        }

        if lunar_phase in lunar_influences:
            interpretations.append(lunar_influences[lunar_phase])

        if aspects:
            harmonious_aspects = [a for a in aspects if a['nature'] == 'harmonious']
            challenging_aspects = [a for a in aspects if a['nature'] == 'challenging']

            if harmonious_aspects:
                interpretations.append("Harmonious planetary alignments support cooperation and positive outcomes.")

            if challenging_aspects:
                interpretations.append("Dynamic planetary tensions create opportunities for growth through challenge.")

        element_advice = {
            'Fire': "Channel your passionate energy into focused action—your enthusiasm is contagious.",
            'Earth': "Ground yourself in practical matters and steady progress—stability brings success.",
            'Air': "Communicate your ideas clearly and connect with others—collaboration is key.",
            'Water': "Trust your intuition and honor your emotional needs—feelings guide you wisely."
        }

        if sign_data['element'] in element_advice:
            interpretations.append(element_advice[sign_data['element']])

        quality_advice = {
            'Cardinal': "Take initiative and lead by example—your natural leadership shines.",
            'Fixed': "Stay committed to your goals and maintain steady progress—persistence pays off.",
            'Mutable': "Adapt to changing circumstances with flexibility—versatility is your strength."
        }

        if sign_data['quality'] in quality_advice:
            interpretations.append(quality_advice[sign_data['quality']])

        if len(interpretations) >= 3:
            main_theme = interpretations[0]
            supporting_elements = ' '.join(interpretations[1:3])
            conclusion = interpretations[-1] if len(interpretations) > 3 else "Trust in your natural wisdom."

            return f"{main_theme} {supporting_elements} {conclusion}"
        else:
            return ' '.join(interpretations) if interpretations else f"The cosmic energies support your {sign_data['element'].lower()} nature today. Trust in your natural strength and wisdom."

    def generate_daily_horoscopes(self, date=None):
        if date is None:
            date = datetime.now()

        lunar_phase = self.calculate_lunar_phase(date)
        primary_planet, secondary_planet = self.get_daily_planetary_emphasis(date)
        aspects = self.calculate_daily_aspects(date)

        daily_horoscopes = {}

        for sign in self.ZODIAC.keys():
            forecast = self.generate_interpretation(sign, date)

            daily_horoscopes[sign] = {
                'forecast': forecast,
                'lunar_phase': lunar_phase,
                'primary_planet': primary_planet,
                'secondary_planet': secondary_planet,
                'lucky_number': random.randint(1, 99),
                'lucky_color': self.get_lucky_color(sign, date)
            }

        return json.dumps(daily_horoscopes, indent=4)

    def get_lucky_color(self, sign, date):
        element_colors = {
            'Fire': ['Red', 'Orange', 'Gold', 'Crimson', 'Coral'],
            'Earth': ['Green', 'Brown', 'Beige', 'Olive', 'Tan'],
            'Air': ['Yellow', 'Silver', 'Light Blue', 'Lavender', 'White'],
            'Water': ['Blue', 'Purple', 'Turquoise', 'Navy', 'Aqua']
        }

        element = self.ZODIAC[sign]['element']
        colors = element_colors[element]

        color_index = (date.day + date.month) % len(colors)
        return colors[color_index]
