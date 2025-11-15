from google import genai
import os

# print("GEMINI_API_KEY =", repr(os.getenv("GEMINI_API_KEY")))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

uploaded_file1 = client.files.upload(file = "pizza.jpg")
uploaded_file2 = client.files.upload(file = "King_Arthur.png")

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = ["Can you make up a short story based off these two images", uploaded_file1, uploaded_file2]
)

story_text = response.text

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(story_text)

print(response.text)
