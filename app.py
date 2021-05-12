import streamlit as st
import datetime
import requests
import json
import os
import time
import re

def get_vaccine_details(pincode, age=25):
	centers_data = get_response(pincode, age)
	i=0
	for center in centers_data['centers']:
		for session in center['sessions']:
			if session['available_capacity'] > 0 and session['min_age_limit'] <= age:
				i+=1
				result = f"{center['name']} has {session['available_capacity']} slots"
				st.text(result)
	if i == 0:
		st.text('No slots available near this pincode for this age range currently. Please check again or check nearby pincodes.')

@st.cache
def get_response(pincode, age):
	url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
	querystring = {"pincode": pincode,"date":"12-05-2021"}
	headers = {
		'authority': "cdn-api.co-vin.in",
		'accept': "application/json, text/plain, */*",
		'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
		'sec-fetch-site': "cross-site",
		'sec-fetch-mode': "cors",
		'sec-fetch-dest': "empty"
		}
	response = requests.request("GET", url, headers=headers, params=querystring).json()
	# st.text('Fetched')
	# centers_data = json.loads(response.text)
	return response

def keep_checking():
	st.title('COVID-19 Vaccine availability checker for India.')
	Your_City_pincode = st.number_input('Input pincode', min_value=0, max_value=999999, value=460001, step=1, help="Input the pincode you wish to check vaccine availablity at..")
	age = st.number_input('Enter your age', min_value=0, max_value=120, value=45, step=1, help="Input your age as vaccine availability depends on age bracket..")
	check_again = st.button('Check vaccine availability now', False)
	if check_again:
		if isValidPinCode(str(Your_City_pincode)):
			st.text(f"Checked at {datetime.datetime.now()}")
			get_vaccine_details(Your_City_pincode, age)
		else:
			st.text('Enter a valid pincode please.')

	st.markdown('''---''')
	st.markdown('Contributors')
	st.markdown('Neel Shah - https://github.com/neelshah16')
	st.markdown('Supan Shah - https://github.com/Supan14')

def isValidPinCode(pinCode):
	regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"; 
  
	p = re.compile(regex);

	if (pinCode == ''):
		return False;
		  
	m = re.match(p, pinCode);
	  
	if m is None:
		return False
	else:
		return True

if __name__ == '__main__':
	keep_checking()