import csv


with open('books.csv', 'r', encoding="utf8") as f:
    books = []
    failed_lines = 0
    
    reader = csv.reader(f)
    
    for line in reader:
            isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description, published_year, average_rating, num_pages, ratings_count = tuple(line)
            if isbn13 != '' and title != '' and authors != '' and categories != '' and description != '' and thumbnail != '':
                books.append([isbn13, title, subtitle, categories, description, thumbnail])
            else:
                failed_lines += 1
    
    print(f'Failed to parse {failed_lines} lines')

with open('books_formatted.csv', 'w', encoding="utf8", newline="") as f:
    writer = csv.writer(f)
    for row in books:
        writer.writerow(row)
