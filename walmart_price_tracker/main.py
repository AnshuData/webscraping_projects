import time
import pandas as pd
from src.price_track import price_check, initialize_csv_file

def main():
    """
    Main function to perform price tracking and update the CSV file.

    The function initializes a CSV file, reads its content, performs price tracking,
    and prints the file content before and after the update.

    Returns:
        pd.DataFrame: Updated DataFrame after price tracking.
    """
    # Path to the CSV file
    csv_file = "./files/price_check.csv"

    # Initialize the CSV file with a header
    initialize_csv_file(filename=csv_file, header=["book_title", "price", "date"])

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    #this is to make sure code runs every day; we can deploy this to AWS Lambda and set it up to be triggered daily.
    n = 1 
    while n < 3:
        # Comment/Uncomment the line below to add a delay between price checks (e.g., sleep for 9600 seconds)
        time.sleep(9600)

        # Perform price tracking
        price_check()
        n += 1

    return df

if __name__ == "__main__":
    # Call the main function if the script is executed directly
    main()
