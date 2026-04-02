import requests
import os

def test_solve_image():
    url = "http://127.0.0.1:8081/solve/image"
    image_path = r"C:\Users\1\.gemini\antigravity\brain\71f493f7-77e8-4fe8-8465-07a921bc2b5b\physics_problem_test_1775118715748.png"
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "image/png")}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_solve_image()
