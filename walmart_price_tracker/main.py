import time
import pandas as pd


from src.price_track import price_check, initialize_csv_file


def main():
    """

    """
    csv_file = "./files/price_check.csv"

    initialize_csv_file(filename=csv_file, header=["book_title", "price", "date"])

    df = pd.read_csv(csv_file)
    print('file content from yesterday:  ', df)

    n = 1 
    while n < 3:
        #time.sleep(9600)
        price_check()
        n+=1

    print('file updated today:  ', df)
    return df


if __name__ == main:
     main()
