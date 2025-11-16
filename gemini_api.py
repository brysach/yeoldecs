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



    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = ["Can you make up a three paragraph fantasy story based off these images, focusing on the items", images_array]
    )

    story_text = response.text

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(story_text)

    return response

if __name__ == "__main__":
    generateFantasyStory()
