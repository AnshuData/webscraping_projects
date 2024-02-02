from googlesearch import search
from collections import OrderedDict
import requests
import re
from bs4 import BeautifulSoup
import json
import os.path


def read_ml_topics(path_to_filename_with_topics):
    """
    Read ML-related topics from a file and return them as a list.

    Args:
    - path_to_filename_with_topics (str): Path to the file containing ML-related topics.

    Returns:
    - List[str]: List of ML-related topics.
    """
    with open(path_to_filename_with_topics, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        ml_topics = lines

    return ml_topics


def generate_content_links(ml_topics, start_index, end_index):
    """
    Generate content links for ML topics and store them in a dictionary.

    Args:
    - ml_topics (List[str]): List of ML-related topics.
    - start_index (int): Start index for slicing the ml_topics list.
    - end_index (int): End index for slicing the ml_topics list.

    Returns:
    - Dict[str, Dict[str, str]]: Dictionary containing ML topics as keys and corresponding content links as values.
    """
    # empty dictionary to store all the topics and respective content-urls
    topic_recommendations_library = {}

    # iterate through list of topics; start_index:end_index introduced to go through set of sample at a time; 
    # too many request at a time can block you from website scraping data from
    for topic in ml_topics[start_index:end_index]:
        new = {}

        # Prepare YouTube search query
        # split each topic and add "+" in between them to match the pattern for youtube search query
        youtube_topic = "+".join(topic.split(" "))
        youtube_urls = "https://www.youtube.com/results?search_query=" + youtube_topic
        params = {"q": youtube_topic, "safe": "active"}

        # Search for YouTube content

        # search the content for topic in youtube using requests library; 
        session = requests.Session()
        youtube_search = session.request(method="GET", url=youtube_urls, params=params)
        parsed_html = BeautifulSoup(youtube_search.text, "html.parser")

        # the above step gives html file which is parsed using beautifulsoup and ist video-id is extracted
        # video_id represents the 11-character unique ids which corresponds to the youtube videos upon query
        video_id = re.findall(r"watch\?v=(\S{11})", str(parsed_html))
        sorted_video_id = list(OrderedDict.fromkeys(video_id))
        new["youtube"] = "https://www.youtube.com/watch?v=" + sorted_video_id[0]

        # Search  for the contents for each topic in Medium site
        for medium_url in search(
            topic + "medium.com",
            tld="com",
            num=1,
            pause=10.0,
            stop=1,
            lang="eng",
            safe="on",
            ):
        
            new["medium"] = medium_url

        # Search  for the contents for each topic in TowardsDataScience site
        for datascience_url in search(
            topic + "towardsdatascience.com",
            tld="com",
            num=1,
            pause=10.0,
            stop=1,
            lang="eng",
            safe="on",
            ):
            new["towardsdatascience"] = datascience_url

        topic_recommendations_library[topic] = new

    return topic_recommendations_library


def save_to_json(data, json_file_path="./output/output.json"):
    """
    Save data to a JSON file.

    Args:
    - data (Dict): Data to be saved.
    - json_file_path (str): Path to the JSON file. Default is "my_file.json".
    """
    if os.path.isfile(json_file_path):
        with open(json_file_path, "r") as f:
            file_contents = json.load(f)
    else:
        file_contents = {}

    file_contents.update(data)

    with open(json_file_path, "w") as f:
        json.dump(file_contents, f, indent=4)


