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
[{"description": "Heart of the big apple.", "location:": "New York City"}]
"""[1:-1]

output_exmaple = r"""
[{"location": "New York City"}]
"""[1:-1]

user_loc_requirements = [   
                        f'The input is a list of dictionary elements, e.g.: {user_loc_input_example}',
                        f'The input is a list of dictionary elements, e.g.: {output_exmaple}',
                        'Make sure the output element count is the same as the input. If you cannot find or determine a location, return {"location": ""} for that tweet.',
                        'If the description contradict to the self-reported home location, return the self-reported home location.',
                        'If the location is longitude and latitude, return them as "longitude, latitude".',  
                        'Keep the original language of extracted location name.',
                        'If the extracted location is a nick, return the standard name for accessbility, such as return "New York City" for "Big apple".',
                      ]
 
# print(output_exmaple)