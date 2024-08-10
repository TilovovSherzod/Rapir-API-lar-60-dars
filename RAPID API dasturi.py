import http.client
import json

RAPIDAPI_KEY = "d02e9c7b74msh42b2b3f6c747efdp145053jsnb8fa4beb0854"

def translate_text_microsoft(text, source_lang, target_lang):
    conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

    payload = json.dumps([{
        "Text": text
    }])

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", f"/translate?api-version=3.0&from={source_lang}&to={target_lang}", payload, headers)

    res = conn.getresponse()
    data = res.read()

    try:
        translation = json.loads(data.decode("utf-8"))
        return translation[0]['translations'][0]['text']
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error during Microsoft translation: {e}, Response: {data.decode('utf-8')}")
        return "Tarjima qilingan matn topilmadi."

def translate_text_google(text, source_lang, target_lang):
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")

    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"q\"\r\n\r\n{text}\r\n-----011000010111000001101001--\r\n\r\n"

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "google-translate1.p.rapidapi.com",
        'Content-Type': "multipart/form-data; boundary=---011000010111000001101001",
        'Accept-Encoding': "application/gzip"
    }

    conn.request("POST", f"/language/translate/v2?source={source_lang}&target={target_lang}", payload, headers)

    res = conn.getresponse()
    data = res.read()

    try:
        translation = json.loads(data.decode("utf-8"))
        return translation['data']['translations'][0]['translatedText']
    except (KeyError, json.JSONDecodeError) as e:
        # print(f"Error during Google translation: {e}, Response: {data.decode('utf-8')}")
        return None  # Return None to indicate the translation failed

def chatgpt_query(query):
    conn = http.client.HTTPSConnection("chatgpt-api8.p.rapidapi.com")

    payload = json.dumps([
        {"content": "Hello! I'm an AI assistant bot based on ChatGPT 3. How may I help you?", "role": "system"},
        {"content": query, "role": "user"}
    ])

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "chatgpt-api8.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/", payload, headers)

    res = conn.getresponse()
    data = res.read()

    try:
        response = json.loads(data.decode("utf-8"))
        # print("ChatGPT API javobi:", response)
        return response['text']
    except (KeyError, json.JSONDecodeError) as e:
        # print(f"Error during ChatGPT query: {e}, Response: {data.decode('utf-8')}")
        return "Javobda mazmun topilmadi."

text_to_translate = input("Sizga qanday yordam bera olamiz? ")

source_language = "uz"
target_language = "en"
translated_text_Uzbek_to_English = translate_text_microsoft(text_to_translate, source_language, target_language)

chatgpt_response = chatgpt_query(translated_text_Uzbek_to_English)

translated_text_English_to_Uzbek = translate_text_google(chatgpt_response, "en", "uz")

if translated_text_English_to_Uzbek is None:
    translated_text_English_to_Uzbek = translate_text_microsoft(chatgpt_response, "en", "uz")

print(f"ChatGPT'dan olingan javob: {translated_text_English_to_Uzbek}")
