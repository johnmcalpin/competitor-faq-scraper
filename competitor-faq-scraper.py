import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import bs4

keyword = 'best mattress for stomach sleepers'

def search_google(keyword):
    urls = []
    for url in search(keyword, stop=20):
        # Exclude URLs with patterns associated with search features
        if not re.search(r'(google\.|/search|\+/)', url) and '#' not in url:
            urls.append(url)
    return urls

def get_word_count(url):
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Remove header and footer tags
    for tag in soup(['header', 'footer']):
        tag.decompose()

    # Find all visible text content
    visible_text = soup.find_all(string=lambda text: not isinstance(text, bs4.element.Comment))

    # Extract the visible text from each tag and concatenate it
    visible_text = [tag.get_text(separator=' ') for tag in visible_text]

    # Concatenate all the visible text
    text = ' '.join(visible_text)

    # Split visible text into words and count them
    words = text.split()
    count = len(words)

    # Return the word count if it is greater than or equal to 1000
    if count >= 1000:
        return count
    else:
        return None

urls = search_google(keyword)

total_word_count = 0
counted_urls = 0
question_sentences = []
for url in urls:
    try:
        word_count = get_word_count(url)
        if word_count is not None:
            total_word_count += word_count
            counted_urls += 1
            print(url, ": ", word_count)
            # Find all question sentences in the page and append them to the list
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            for tag in soup(['h2', 'h3', 'h4']):
                for sentence in tag.strings:
                    if sentence.endswith('?'):
                        question_sentences.append(sentence)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

if counted_urls > 0:
    average_word_count = total_word_count / counted_urls
    print("Average word count across all", counted_urls, "URLs: ", average_word_count)
else:
    print("No URLs found for the specified keyword.")

# Export the question sentences to a txt file
if question_sentences:
    with open('question_sentences.txt', 'w') as f:
        for sentence in question_sentences:
            f.write(sentence + '\n')
        print('Question sentences saved to question_sentences.txt')
else:
    print('No question sentences found.')
