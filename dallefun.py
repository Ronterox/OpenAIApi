import os


def download_image_from_response(response, name, px):
    for i, result in enumerate(response['data']):
        image_url = result['url']
        image_name = f"images/{name}{px}x{px}n{i}.png"
        print(f"Image URL {i}: {image_url}")
        os.system(f"wget \"{image_url}\" -O {image_name} && code {image_name}")