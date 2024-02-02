from src.content_gathering import read_ml_topics, generate_content_links, save_to_json



def main(filename_with_topics, start_index=0, end_index=5):
    """
    Generate content links for ML topics and save them to a JSON file.

    Args:
    - path_to_filename_with_topics (str): Path to the file containing ML-related topics.
    - start_index (int): Start index for slicing the ml_topics list. Default is 0.
    - end_index (int): End index for slicing the ml_topics list. Default is 5.

    Returns:
    - Dict[str, Dict[str, str]]: Dictionary containing ML topics as keys and corresponding content links as values.
    """
    ml_topics = read_ml_topics(filename_with_topics)
    topic_links = generate_content_links(ml_topics, start_index, end_index)
    save_to_json(topic_links)

    return topic_links


#Entrypoint
if __name__ == main()
    main("./input_topics/ML_topics.txt", start_index=20, end_index=25)