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

user_loc_task_prefix = r'Extract Twitter user’s home location based on their profile description and self-reported home location. '

user_loc_input_example = """
[{"id": 56332, "description": "Heart of the big apple.", "location:": "New York City"}, {"userid": 635, "description": "Writer, house wife.", "location:": "Rural area"}]
"""[1:-1]

output_exmaple = r"""
56332:New York City, US;635:;
"""[1:-1]

user_loc_requirements = [   
                        f'The input is a list of dictionary elements, e.g.: {user_loc_input_example}',
                        f'The output is a long string, the format is: "id1:location1;id2:location2;". E.g.: {output_exmaple}. The ";" is used to separate the each user location; the "," is used to separate the location parts or levels. The output user order should be the same as the input, and the output count MUST equal to the input count.',
                        'Return the location string only, DO NOT add explanation and description.',
                        'The semicolon, ";", is not allow in the location name. Make sure the output element count is the same as the input. If you cannot find or determine a location, return an empty string as the location name for that tweet, DO NOT make up fake location names.',
                        'If the description contradict to the self-reported home location, return the self-reported home location.',
                        'If the location is longitude and latitude, return them as: "id:longitude,latitude;". DO NOT use the direction letter (i.e., N, S, E, W), but use the minus sign "-" when necessary.',  
                        'Keep the original language of extracted location name.',
                        'If the extracted location is a nickname, return the standard name for accessbility, such as return "New York City" for "Big apple".',
                        'The extracted location needs to follow the fine-coarse order, e.g., city, state, county; DO NOT return emojis in the result.',
                        'DO NOT return abbreviation except for countries, e.g., return South Carolina, not SC; it is okay to return USA or UK.',
                        'Use comma, i.e., ",", to seprate the extracted location parts/levels. Other special charaters, such as \ and /, art not allowed in the locatio name.',
                        'If you can determine the country name, add it in the results. You can also add other levels of location names, such as province and city, if you can determine based on the input description and self-reported location. DO NOT make up fake location names.',
                        
                      ]
 
# Use double quote, i.e., ", not single quote, \'. 