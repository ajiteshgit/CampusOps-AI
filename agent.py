import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Attendance Calculation Tool
def calculate_attendance(attended: int, total_held: int, target_pct: float = 75.0):
    """Calculates attendance percentage and margins."""
    current_pct = (attended / total_held) * 100 if total_held > 0 else 0

    if current_pct >= target_pct:
        bunkable = 0
        while ((attended) / (total_held + bunkable + 1)) * 100 >= target_pct:
            bunkable += 1
        return f"Current Attendance: {current_pct:.2f}% (SAFE). You can skip the next {bunkable} class(es)."
    else:
        required = 0
        while ((attended + required) / (total_held + required)) * 100 < target_pct:
            required += 1
        return f"Current Attendance: {current_pct:.2f}% (DANGER). You must attend the next {required} consecutive class(es)."

def run_campus_agent(user_query: str):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=types.GenerateContentConfig(
            tools=[calculate_attendance],
            temperature=0.2
        )
    )
    return response.text

if __name__ == "__main__":
    query = "I have attended 14 out of 20 classes in Operating Systems. Target is 75%. Can I skip today's class?"
    print("User Query:", query)
    print("Agent Response:", run_campus_agent(query))
