import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# use your KEY.
OpenAI_key = config.get('API_Key', 'OpenAI_key')
# print("OpenAI_key:", OpenAI_key)



system_role = r'A professional Geographer who is extracting location information from tweet texts.'

# carefully change these prompt parts!   

#--------------- constants for user localization  ---------------
user_loc_role = system_role

user_loc_task_prefix = r'Extract Twitter user’s home location into country, first-level administrative divisions (i.e., State/province/equivalent), or city level based on their profile description and self-reported home location. '

user_loc_input_example = """
[{"id": 56332, "description": "Heart of the big apple.", "location:": "New York City"}, {"id": 635, "description": "Writer, house wife.", "location:": "Rural area"}]
"""[1:-1]

output_exmaple = r"""
56332:city,New York City, US;635:;
"""[1:-1]

user_loc_requirements = [   
                        f"The input is a list of dictionary elements, contains users' descriptions and self-reported home locations, e.g.: {user_loc_input_example}",
                        r"The extracted location name MUST be a real place. If the given self-reported location name contains text which does not look like a real location, e.g., 'ronnie from #bb11's house', return an empty string as the location name for that user. If you cannot determine the location, DO NOT make up a fake place.",
                        f'The output is a long English string, the format is: "id1:level_type,location1;id2:location2;". E.g.: {output_exmaple}. The "level_type" can be one of [country, subadmin, city, lonlat], the "subadmin" means the first-level administrative division (i.e., State/province/equivalent); the "lonlat" means the longitude,latitude, e.g., "14.535,23.3534" of the self-reported location. The ";" is used to separate the each user location; the "," is used to separate the location parts or levels. The output user order should be the same as the input, and the output count MUST equal to the input count.',
                        'level_types and their associated location format: "city,city_name,subadmin_name,country_name", "subadmin,subadmin_name,country_nam", "country,country_name',
                        'Return only one location for each user; if multiple location provided, return the fist one.',
                        'Return the location string only, DO NOT add explanation and description. All returned location name MUST be translated into English.',
                        'If the original location name is not English, translate them into English in the returned results.',
                        'The semicolon, ";", is not allow in the location name. Make sure the output element count is the same as the input. If you cannot find or determine a location, return an empty string as the location name for that user, DO NOT make up fake location names.',                       
                        'If the description contradict to the self-reported home location, return the self-reported home location.',
                        '";;" is an error in the returned location string. DO NOT return ";;". ',
                        'If the location is longitude and latitude, return them as decimal lon/lat, e.g.: "id:lonlat,longitude,latitude;". DO NOT use the direction letter (i.e., N, S, E, W), but use the minus sign "-" when necessary.',  
                        
                        'If the extracted location is a nickname, return the standard name for accessbility, such as return "New York City" for "Big apple".',
                        'If you can determine, return the city level location name. The extracted location needs to follow the fine-coarse order, e.g., city, state, country. If you can determine the state or province level, return them too; if there is not enough information to determine the city, state/province/equivalent, or country, DO NOT make up fake locations, stead, return an empty location try for that user. DO NOT return emojis in the result.',
                        'Use the abbreviation for US states, e.g., return SC, not South Carolina. For example, Columbia, SC, US.',
                        r'Use comma(",") to seprate the extracted location parts/levels. Other special charaters, such as "\" and "/", art not allowed in the locatio name.',
                        'If you can determine the country name, add it in the result using two letter code (e.g., CN, US). You can also add other levels of location names, such as province and city, if you can determine based on the input description and self-reported location. DO NOT make up fake location names.',
                        
                      ]
 
# Use double quote, i.e., ", not single quote, \'. 
# 'Keep the original language of extracted location name.',
# 'If the original location name is not English, translate them into English in the returned results.',
# 'DO NOT return abbreviation except for countries, e.g., return South Carolina, not SC; it is okay to return USA or UK.',