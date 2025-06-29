# from flask import Flask, request, jsonify
# from astrology_tool import AstrologyTool
# import os

# app = Flask(__name__)
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

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))  # use Render's port or default to 5000
#     app.run(host="0.0.0.0", port=port, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- NEW
from astrology_tool import AstrologyTool
import os

app = Flask(__name__)
CORS(app, origins=["https://teal-brioche-d37e12.netlify.app"])  # <-- NEW: allows Netlify frontend

tool = AstrologyTool()

@app.route('/birth-chart', methods=['POST'])
def birth_chart():
    data = request.get_json()

    try:
        birth_date = tuple(data['birth_date'])       # e.g., [1990, 6, 28]
        birth_time = tuple(data['birth_time'])       # e.g., [14, 30, 0]
        birth_place = data['birth_place']            # e.g., "Paris, France"
        gender = data.get('gender', 'Other')         # optional, default to "Other"

        result = tool.create_birth_chart(birth_date, birth_time, birth_place, gender)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # use Render's port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
