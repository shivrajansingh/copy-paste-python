import os
import pyautogui
from datetime import datetime
import pytesseract
from PIL import Image
from mistralai import Mistral
from dotenv import load_dotenv
import requests
import json
import streamlit as st
import time 

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def take_screenshot():
    # Create the 'images' directory if it doesn't exist
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Generate a timestamp for unique screenshot filenames
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Define the full path for saving the screenshot
    screenshot_path = os.path.join(images_dir, f'screenshot_{timestamp}.png')

    # Take a screenshot and save it
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    return screenshot_path



def extract_text_from_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    
    return text


def generate_response(prompt):
    api_key = os.environ.get("MISTRAL_API_KEY")
    model = "codestral-latest"
    url = "https://codestral.mistral.ai/v1/chat/completions"

    payload = json.dumps({
    "model": model,
    "messages": [
        {
        "role": "user",
        "content": prompt
        }
    ]
    })
    headers = {
    'Authorization': 'Bearer '+api_key,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    return res['choices'][0]['message']['content']

def findAnswer():
    screenshot_path = take_screenshot()
    text = extract_text_from_image(screenshot_path)
    res2 = generate_response("this text is extracted from the html, avoid unnecessary text or word and Generate the proper answer or code to this question:  "+text)
    st.chat_message("assistant").write(res2)

def findOutput():
    screenshot_path = take_screenshot()
    text = extract_text_from_image(screenshot_path)
    res1 = generate_response("find the code snippet from the given text:  "+text)
    st.chat_message("user").write(res1)
    instruction ="Find the output of the code snippet"
    res2 = generate_response(instruction+" "+res1)
    st.chat_message("assistant").write(res2)

def executeInLoop():
    temp = ""
    while True:
        screenshot_path = take_screenshot()
        text = extract_text_from_image(screenshot_path)
        instruction = "find the answer of the given text: "
        if text != temp:
            st.chat_message("user").write(instruction+" "+text)
            res = generate_response(text)
            st.chat_message("assistant").write(res)
            temp = text
            time.sleep(60)
                
if __name__ == '__main__':
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        answerBtn = st.button("Answer it")
    with col2:
        outputBtn = st.button("Find Output")
    with col3:
        executeBtn = st.button("execute every 1 min")
    with col4:
        recordBtn = st.button("record")
        
    if answerBtn:
        findAnswer()
    elif outputBtn:
        findOutput()
    elif executeBtn:
        executeInLoop()