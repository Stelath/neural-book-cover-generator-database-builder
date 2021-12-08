import argparse
import time
import urllib.request
import csv
from tqdm import tqdm
from random import randint
import pickle
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="The CSV file to scrape (the csv file must be formatted as so: isbn, title, subtitle, catagories, description, thumbnail)", required=True, type=str)
    parser.add_argument("--output", help="The output folder", required=True, type=str)
    return parser.parse_args()

def main():
    args = get_args()
    start_time = time.time()
    
    os.makedirs(f'{args.output}/text', exist_ok=True)
    os.makedirs(f'{args.output}/images', exist_ok=True)
    os.makedirs(f'{args.output}/train', exist_ok=True)
    os.makedirs(f'{args.output}/test', exist_ok=True)
    
    train_files = []
    val_files = []
    
    with open(args.file, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for line in tqdm(list(reader)[1:]):
            isbn, title, subtitle, categories, description, thumbnail = tuple(line)\
            
            # Get images from Google Books
            urllib.request.urlretrieve(thumbnail, f'{args.output}/images/{isbn}.jpg')
            
            # Save book info to file
            with open(f'{args.output}/text/{isbn}.txt', 'w', encoding='utf8') as f:
                f.write(f'{title}, {subtitle}, {categories}, {description}\n'.lower())
            
            # Set to training or testing data
            if randint(0, 3) == 0:
                val_files.append(isbn)
            else:
                train_files.append(isbn)
            
        # Save training and testing data
        with open(f'{args.output}/train/filenames.pickle', 'wb') as f:
            pickle.dump(train_files, f)
        
        with open(f'{args.output}/test/filenames.pickle', 'wb') as f:
            pickle.dump(val_files, f)
        
    print('Train Files:', len(train_files))
    print('Val Files:', len(val_files))
    print('Total Files:', len(train_files) + len(val_files))
    
    print(f"Time taken: {time.time() - start_time}")

if __name__ == '__main__':
    main()
