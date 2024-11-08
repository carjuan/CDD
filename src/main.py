import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def init(config):
    OPENAI_API_KEY = os.getenv("API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError(
            "The OpenAI API key must be set in config.json before proceeding to requests. field must be set as 'api_key'"
        )

    URL = config.get("url")

    HEADERS = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    PAYLOAD = {
        "prompt": config["payload"]["prompt"],
        "size": config["payload"]["size"],
        "model": config["payload"]["model"],
        "n": config["payload"]["n"],
    }

    r = requests.post(URL, headers=HEADERS, json=PAYLOAD)

    if r.status_code == 200:
        images = r.json().get("data", [])
        for idx, image in enumerate(images):
            image_url = image.get("url")

            if image_url:
                print(f"image id: {idx}")
                print(f"image url: {image_url}")
                print("About to download this image...")
                img_data = requests.get(image_url).content
                with open(
                    f"generated_images/generated_image_{idx + 1}.png", "wb"
                ) as img_file:
                    img_file.write(img_data)
                print(f"Image {idx + 1} saved as generated_image_{idx + 1}.png")

    else:
        print(f"Failed to generate image: {r.status_code} - {r.text}")


if __name__ == "__main__":
    with open("config.json", "r") as config:
        config = json.load(config)
    init(config)
