from flask import Flask, render_template, request, redirect
import requests
from selenium import webdriver
import json

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['link']

        driver = webdriver.Chrome()
        driver.get(link)

        text_file = open("random.txt", "w")
        element = driver.find_element("xpath", "/html/body")
        text_file.write(element.text)
        text_file.close()

        driver.close()

        return redirect('/result')
    return render_template('index.html')


@app.route('/result')
def result():
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Retrieve the content from the previously submitted link
    text_file = open("random.txt", "r")
    website_text = text_file.read()
    text_file.close()
    
    # Close the file and the driver
    driver.close()

    # API endpoint URL
    url = "https://api.openai.com/v1/chat/completions"

    # Your API key
    api_key = "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"

    # Headers containing the Authorization and Content-Type
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Prompt for the conversation
    prompt = "Give me the ingredient list from the following text from a recipe site:\n" + website_text
    prompt2 = "Similarly, give me the instructions from the same recipe site earlier. Do not number the instructions but put them in new lines instead. I repeat, do NOT number the items. Especially, do NOT number the instructions in the form of 1...; 2...; 3... and so on. Instead, do them in the form X, Y, and Z:\n" 

    # Generate a response
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": prompt}],
        "max_tokens": 100
    }
    data2 = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": prompt2}],
        "max_tokens": 300
    }

    # Send the API request
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    response_2 = requests.post(url, headers=headers, json=data2)
    response_json2 = response_2.json()

    # Extract the reply from the response
    reply = response_json['choices'][0]['message']['content']
    reply2 = response_json2['choices'][0]['message']['content']

    # Print the reply
    reply_var = reply.split("\n")
    reply_var2 = reply2.split("\n")
    print(reply)
    print(reply_var)
    print("")
    print(reply2)
    print("")
    print(reply_var2)
    return render_template('result.html', reply_var=reply_var, reply_var2=reply_var2)

if __name__ == "__main__":
    app.run(debug=True)