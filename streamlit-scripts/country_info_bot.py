from typing import Generator
from countryinfo import CountryInfo
import streamlit as st
import time


def get_country_basic_information(country_name: str="france") -> str:
	"""
    Retrieves basic information about a specified country.

    Parameters:
        country_name (str): The name of the country (default is "france").

    Returns:
        str: A formatted string containing details such as the country's information. If the country is not found,
             an error message is returned.
    """
	try:
		info = CountryInfo(country_name=country_name).info()
		name = "Name: " + info['name']
		capital = "Capital: " + info['capital']
		capital_lat_long = "Capital coordinats(lat-long): {} {}".format(info['capital_latlng'][0], info['capital_latlng'][1])
		area = "Area: {} {}".format(info['area']," km²")
		alt_spelling = "Alternative spellings: {}".format(",".join(info['altSpellings']))
		borders = "Borders: {}".format(",".join(info['borders']))
		calling_codes = "Calling codes: {}".format(",".join(info['callingCodes']))
		capital_lat_long = "Capital coordinats(lat-long): {}<>{}".format(info['capital_latlng'][0], info['capital_latlng'][1])
		demonym = "Demonym: {}".format(info['demonym'])
		
		output_part_1 = name + " | " + capital + " | "  + capital_lat_long +  " | " + area + " | " + alt_spelling  + " | "
		output_part_2 = borders + " | " + calling_codes + " | " + demonym  +   " | "

		return output_part_1 + output_part_2
	except KeyError:
		return "Country not found." + " | " + "Please enter a valid country name in English."


def yield_formatted_output(string: str) -> Generator[str, None, None]:
	"""
	Yields formatted words from the input string.

	Args:
		string (str): The input string containing words separated by '|'.

	Yields:
		str: Formatted words with line breaks after each '|'.
	"""
	for word in string.split():
		if word.strip() != "|":
			yield word + " "
		else:
			yield "  \n"
		time.sleep(0.1)
def main():
	"""
	Main streamlit function.
	"""
	st.title("Country information")

	if "messages" not in st.session_state:
		st.session_state.messages = []

	# Display chat messages from history on app rerun
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])

	# Accept user input
	if prompt := st.chat_input("Type a country name in english ..."):
		st.session_state.messages.append({"role": "user", "content": prompt})
		with st.chat_message("user"):
			st.markdown(prompt)

		# Get country information
		country_info = get_country_basic_information(prompt)

		# Display assistant response in chat message container
		with st.chat_message("assistant"):
				st.write_stream( yield_formatted_output(country_info))
			
		# Add assistant response to chat history
		st.session_state.messages.append({"role": "assistant", "content": country_info.replace("|","  \n")})


if __name__ == "__main__":
	main()
