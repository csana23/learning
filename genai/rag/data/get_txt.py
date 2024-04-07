import requests

# URL of the website
url = "https://www.gutenberg.org/files/132/132-h/132-h.htm"

# Send a GET request to the URL
response = requests.get(url)

# Extract the content from the response
content = response.text

# Find the starting point of the desired section
start_index = content.find("Chapter I. LAYING PLANS")

# Extract the relevant text
desired_text = content[start_index:]

# Save the text to a .txt file
with open("The_Art_of_War.txt", "w", encoding="utf-8") as file:
    file.write(desired_text)

print("Text downloaded and saved as The_Art_of_War.txt")
