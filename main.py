# from flask import Flask, request, jsonify
# from flask_cors import CORS  # <-- NEW
# from astrology_tool import AstrologyTool
# import os

# app = Flask(__name__)
# CORS(app, origins=["https://teal-brioche-d37e12.netlify.app"])  # <-- NEW: allows Netlify frontend

# tool = AstrologyTool()

# @app.route('/birth-chart', methods=['POST'])
# def birth_chart():
#     data = request.get_json()

#     try:
#         birth_date = tuple(data['birth_date'])       # e.g., [1990, 6, 28]
#         birth_time = tuple(data['birth_time'])       # e.g., [14, 30, 0]
#         birth_place = data['birth_place']            # e.g., "Paris, France"
#         gender = data.get('gender', 'Other')         # optional, default to "Other"

#         result = tool.create_birth_chart(birth_date, birth_time, birth_place, gender)
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/compatibility', methods=['POST'])
# def compatibility():
#     data = request.get_json()

#     try:
#         # Person 1
#         birth_date1 = tuple(data['person1']['birth_date'])
#         birth_time1 = tuple(data['person1']['birth_time'])
#         birth_place1 = data['person1']['birth_place']
#         gender1 = data['person1'].get('gender', 'Other')

#         # Person 2
#         birth_date2 = tuple(data['person2']['birth_date'])
#         birth_time2 = tuple(data['person2']['birth_time'])
#         birth_place2 = data['person2']['birth_place']
#         gender2 = data['person2'].get('gender', 'Other')

#         # Create charts
#         chart1 = tool.create_birth_chart(birth_date1, birth_time1, birth_place1, gender1)
#         chart2 = tool.create_birth_chart(birth_date2, birth_time2, birth_place2, gender2)

#         # Analyze compatibility
#         result = tool.analyze_compatibility(chart1, chart2)

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))  # use Render's port or default to 5000
#     app.run(host="0.0.0.0", port=port, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from astrology_tool import AstrologyTool
from horoscope_generator import ProfessionalHoroscopeGenerator
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app, origins=["https://teal-brioche-d37e12.netlify.app"])

tool = AstrologyTool()
horoscope_generator = ProfessionalHoroscopeGenerator()

@app.route('/birth-chart', methods=['POST'])
def birth_chart():
    data = request.get_json()

    try:
        birth_date = tuple(data['birth_date'])
        birth_time = tuple(data['birth_time'])
        birth_place = data['birth_place']
        gender = data.get('gender', 'Other')

        result = tool.create_birth_chart(birth_date, birth_time, birth_place, gender)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/compatibility', methods=['POST'])
def compatibility():
    data = request.get_json()

    try:
        birth_date1 = tuple(data['person1']['birth_date'])
        birth_time1 = tuple(data['person1']['birth_time'])
        birth_place1 = data['person1']['birth_place']
        gender1 = data['person1'].get('gender', 'Other')

        birth_date2 = tuple(data['person2']['birth_date'])
        birth_time2 = tuple(data['person2']['birth_time'])
        birth_place2 = data['person2']['birth_place']
        gender2 = data['person2'].get('gender', 'Other')

        chart1 = tool.create_birth_chart(birth_date1, birth_time1, birth_place1, gender1)
        chart2 = tool.create_birth_chart(birth_date2, birth_time2, birth_place2, gender2)

        result = tool.analyze_compatibility(chart1, chart2)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/horoscope/daily', methods=['GET'])
def daily_horoscope():
    sign = request.args.get("sign")
    date_str = request.args.get("date")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    data = horoscope_generator.generate_daily_horoscopes(date)
    all_horoscopes = json.loads(data)

    if sign:
        sign = sign.capitalize()
        if sign not in all_horoscopes:
            return jsonify({"error": "Invalid zodiac sign"}), 400
        return jsonify({sign: all_horoscopes[sign]})

    return jsonify(all_horoscopes)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
