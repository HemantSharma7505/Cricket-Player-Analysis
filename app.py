import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json
import re  # Import regex for cleaning responses

# Load API Key
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        player = request.form["player"]
        ground = request.form["ground"]
        
        # Prompt for Gemini API
        prompt = f"""
        Provide the latest overall statistics for player {player} and latest statistics for player {player} at {ground} up to today's date.
        Ensure the data is accurate. Respond only with a JSON in this format:

        {{
            "international_stats": {{
                "matches": null,
                "innings": null,
                "runs": null,
                "highest_score": null,
                "average": null,
                "strike_rate": null,
                "100s": null,
                "50s": null
            }},
            "ground_specific_stats": {{
                "tests": {{
                    "matches": null,
                    "innings": null,
                    "runs": null,
                    "highest_score": null,
                    "average": null,
                    "strike_rate": null,
                    "100s": null,
                    "50s": null
                }},
                "odis": {{
                    "matches": null,
                    "innings": null,
                    "runs": null,
                    "highest_score": null,
                    "average": null,
                    "strike_rate": null,
                    "100s": null,
                    "50s": null
                }},
                "t20is": {{
                    "matches": null,
                    "innings": null,
                    "runs": null,
                    "highest_score": null,
                    "average": null,
                    "strike_rate": null,
                    "100s": null,
                    "50s": null
                }}
            }},
            "notes": ["Ensure that the statistics are up-to-date."]
        }}
        """


        # Fetch response from Gemini API
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        stats_data = response.text.strip()

        print("\n🚀 API Raw Response:\n", stats_data)  # Debugging Output

        # Extract only the JSON part using regex
        match = re.search(r"\{.*\}", stats_data, re.DOTALL)
        if match:
            stats_data = match.group(0)  # Extract JSON portion
        else:
            print("\n❌ No valid JSON found in response")
            return "Invalid response format from API", 500

        # Validate and parse JSON response
        try:
            stats = json.loads(stats_data)
            print("\n✅ Parsed JSON:", stats)  # Debugging Output
        except json.JSONDecodeError as e:
            print("\n❌ JSON Decode Error:", e)
            return "Invalid JSON response from API", 500

        # Check if required keys exist before accessing them
        international_stats = stats.get("international_stats", {})
        ground_stats = stats.get("ground_specific_stats", {})  # Corrected key name
        observations = stats.get("notes", ["No observations provided."])  # Default to an empty list

        return render_template(
            "result.html",
            player=player,
            ground=ground,
            international_stats=international_stats,
            ground_stats=ground_stats,
            observations=observations
        )

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
