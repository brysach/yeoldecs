from google import genai
import os
from os import listdir
from PIL import Image

# print("GEMINI_API_KEY =", repr(os.getenv("GEMINI_API_KEY")))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

folder_dir = "./images"

images_array = []

def generateFantasyStory():
    global folder_dir
    images_array.clear()
    for image_name in os. listdir(folder_dir):
        if image_name.endswith(".png"):
            filename = os.path.join(folder_dir, image_name)
            images_array.append(Image.open(filename))
            os.remove(filename)

    prompt = (
        "You are a friendly storyteller for children.\n"
        "Write ONE short, kid-friendly fantasy paragraph (4–6 simple sentences) "
        "inspired by the objects in these images. "
        "Give the items magical roles in the story.\n"
        "Requirements:\n"
        "- Audience: kids around 7–10 years old.\n"
        "- Use simple, clear vocabulary and short sentences.\n"
        "- Keep the tone warm, positive, and hopeful.\n"
        "- No violence, horror, blood, death, or scary monsters.\n"
        "- Do NOT mention the images or filenames; just tell the story.\n"
    )

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = [prompt, images_array]
    )

    story_text = response.text

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(story_text)

    return response

if __name__ == "__main__":
    generateFantasyStory()
