import re
# import openai
from collections import deque
import openai
# import networkx as nx
import logging
import time

import os
import requests
import networkx as nx
import pandas as pd
import geopandas as gpd
from pyvis.network import Network
 

import Tweet_Geo_constants as constants

def clean_tweet(tweet_text):
    # Remove URLs
    tweet_text = re.sub(r'http\S+|www.\S+', '', tweet_text, flags=re.MULTILINE)
    # Remove usernames/mentions
    
    tweet_text = re.sub(r'@\w+\s+', '', tweet_text)
    tweet_text = re.sub(r'@\w+[ ,]*', '', tweet_text)
    return tweet_text

    # Example usage:
    # tweet = "@user This is a tweet with a URL: http://example.com"
    # print(clean_tweet_text(tweet))
    
    
    
def get_LLM_reply(prompt="Provide Python code to read a CSV file from this URL and store the content in a variable. ",
                  system_role=r'You are a professional Geo-information scientist and developer.',
                  model=r"gpt-3.5-0613",
                  verbose=True,
                  temperature=1,
                  stream=True,
                  retry_cnt=3,
                  sleep_sec=10,
                  ):
    openai.api_key = constants.OpenAI_key

    # Generate prompt for ChatGPT
    # url = "https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv"
    # prompt = prompt + url

    # Query ChatGPT with the prompt
    # if verbose:
    #     print("Geting LLM reply... \n")
    count = 0
    isSucceed = False
    while (not isSucceed) and (count < retry_cnt):
        try:
            count += 1
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                stream=stream,
                )
        except Exception as e:
            # logging.error(f"Error in get_LLM_reply(), will sleep {sleep_sec} seconds, then retry {count}/{retry_cnt}: \n", e)
            print(f"Error in get_LLM_reply(), will sleep {sleep_sec} seconds, then retry {count}/{retry_cnt}: \n", e)
            time.sleep(sleep_sec)


    response_chucks = []
    if stream:
        for chunk in response:
            response_chucks.append(chunk)
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                if verbose:
                    print(content, end='')
    else:
        content = response["choices"][0]['message']["content"]
        # print(content)
    print('\n\n')
    # print("Got LLM reply.")
        
    response = response_chucks # good for saving
    
    return response


def extract_content_from_LLM_reply(response):
    stream = False
    if isinstance(response, list):
        stream = True
        
    content = ""
    if stream:       
        for chunk in response:
            chunk_content = chunk["choices"][0].get("delta", {}).get("content")         

            if chunk_content is not None:
                # print(chunk_content, end='')
                content += chunk_content
                # print(content)
        # print()
    else:
        content = response["choices"][0]['message']["content"]
        # print(content)
        
    return content

def location_str_to_list(location_str):
    loc_list = location_str.split(";")
    loc_list = [l.split(":") for l in loc_list]
    return loc_list