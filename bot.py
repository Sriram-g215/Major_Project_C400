from twilio.rest import Client
import google.generativeai as genai
import os

API_KEY = ""
genai.configure(api_key=API_KEY)
def fetch_logs():
	with open('stress_test.log', 'r') as file:
    	txt = file.read()
	return txt

def send_logs_to_api(logs):
	model = genai.GenerativeModel("gemini-1.5-flash")    
	response = model.generate_content(f"suggest troubleshooting steps in 150 words based on the given logs\n{logs}")
	print(response.text)
	return response.text

def send_whatsapp_message(message_body):
	account_sid = ""
	auth_token = ""
	client = Client(account_sid, auth_token)
	sent_message = client.messages.create(
    	body=message_body,
    	from_="whatsapp:",
    	to="whatsapp:"
	)
	print("WhatsApp message sent with SID:", sent_message.sid)
	return sent_message.sid


def main():
	logs = fetch_logs()
	analysis_result = send_logs_to_api(logs)

	if analysis_result:
    	send_whatsapp_message(analysis_result)

if __name__ == "__main__":
	main()
