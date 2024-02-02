from getpass4 import getpass
from requests_toolbelt.multipart.encoder import MultipartEncoder
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googlesearch import search
import requests, json, sys, os, glob, fnmatch


# API endpoint for the Garnish web service
url_garn_srv = 'https://xyz.azurewebsites.net/'

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('bert-base-nli-mean-tokens')

def create_transcript(yt_url):
    """
    Fetches the transcript and timestamps of a YouTube video using the Garnish web service.

    Args:
    - yt_url (str): YouTube video URL.

    Returns:
    - dict: JSON data containing the transcript and timestamps.
    """

    # Read JWT token from file for authentication
    with open("JWTtoken", "r") as jwt_file:
        username = jwt_file.readline().replace("\n","")
        jwt_token = jwt_file.readline()
        
    
    # Request transcript and timestamps from Garnish web service
    interactive = True
    yt_vid = requests.post(url_garn_srv+'yturl', headers={"authorization" : "Bearer " + jwt_token}, data={'url': yt_url})
    json_data = json.loads(yt_vid.content)
    return json_data



def create_yt_url_at_given_timestamp(url, topic):
    """
    Returns the YouTube URL with timestamp where a specific topic is mentioned.

    Args:
    - url (str): YouTube video URL related to the topic.
    - topic (str): Topic of interest.

    Returns:
    - str: YouTube URL with timestamp where the topic is mentioned.
    """

    # Get transcript and timestamps using Garnish web service
    json_data = create_transcript(url)

    # transcript chuncks
    index_to_topic_dict = json_data['document_text']

    # timestamp corresponding to above transcript chunks 
    index_to_timstamp_dict = json_data['timestamps']

    # list of transcript chuncks
    topics_list = list(index_to_topic_dict.values())

    # sentence embedding of every transcript chuncks
    sentence_embeddings = model.encode(topics_list)
    topic_of_interest = model.encode(topic)

    # similarity between topic and chuncks of transcript to find the the timestamp 
    # at which the topic of interest is described in the youtube url
    similarity_measure = cosine_similarity([topic_of_interest],sentence_embeddings[:])
    similarity_measure_list = similarity_measure.tolist()[0]
    index = similarity_measure_list.index(max(similarity_measure_list))
    time_stamp = index_to_timstamp_dict[str(index)]["start"]

    # Construct the YouTube URL with the timestamp
    youtube_url_timestamp =  url + "&t=" + time_stamp + 's'
    
    return youtube_url_timestamp




