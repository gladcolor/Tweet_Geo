import Tweet_Geo_constants as constants
import helper
import os
import requests
import pandas as pd
# import geopandas as gpd
# from pyvis.network import Network
import openai
import pickle
import time
import sys
import traceback



class Localization():
    
    def __init__(self,
        
                user_df,
                model='gpt-3.5-turbo-0613',
                max_tweet=100,
                used_cols=['id', 'description', 'location'],
                  
                ):
        assert len(user_df) <= max_tweet, f"The tweet count is {len(user_df)}; it should <= {max_tweet}!"
        self.user_df = user_df
        self.used_cols = used_cols
        self.prompt_for_user_localization = self.get_prompt_for_user_localization()
        
        self.use_loc_LLM_response = ""
        self.model = model
 
     
    def get_prompt_for_user_localization(self):        
        user_loc_requirement_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(constants.user_loc_requirements)])
        list_of_dict = self.user_df[self.used_cols].to_dict('records')

        user_loc_prompt = f"Your role: {constants.user_loc_role} \n" + \
                          f"Your task: {constants.user_loc_task_prefix} \n" + \
                          f"Requirement:\n{user_loc_requirement_str} \n" + \
                          f"List of user discription and self-report home location:\n{list_of_dict}"
        
        return user_loc_prompt
        
        # self.prompt_for_user_localization = user_loc_prompt

    def get_LLM_user_loc_response(self):
        user_loc_LLM_response = helper.get_LLM_reply(
                          prompt=self.prompt_for_user_localization,
                          system_role=constants.user_loc_role,
                          model=self.model,
                          # model=r"gpt-4",
                         )
        self.use_loc_LLM_response = user_loc_LLM_response
          
        return self.use_loc_LLM_response
# class Tweet():
#     """
#     """
    
#     pass
    
    
    
# class User():
#     """
#     """
    
#     pass


# class Media():
#     """
#     """
    
#     pass


# class Place():
#     """
#     """
    
#     pass

# class Poll():
#     """
#     """
    
#     pass