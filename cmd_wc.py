import argparse
import string
from collections import Counter

def count_words(text, ignore_case=True, ignore_stop_words=False):
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Convert to lowercase if ignore_case is True
    if ignore_case:
        text = text.lower()
    
    # Split the text into words
    words = text.split()
    
    # Remove stop words if ignore_stop_words is True
    if ignore_stop_words:
        stop_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with'])
        words = [word for word in words if word.lower() not in stop_words]
    
    # Count word occurrences using Counter
    return Counter(words)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Count word occurrences in a text.")
    parser.add_argument("text", help="The text to analyze")
    parser.add_argument("-c", "--case-sensitive", action="store_true", help="Enable case-sensitive counting")
    parser.add_argument("-s", "--ignore-stop-words", action="store_true", help="Ignore common stop words")
    parser.add_argument("-n", "--top-n", type=int, default=None, help="Show only the top N most common words")
    parser.add_argument("-o", "--output", choices=['text', 'csv'], default='text', help="Output format (text or csv)")
    
    # Parse arguments
    args = parser.parse_args()
    print(args.top_n)
    
    # Count words
    result = count_words(args.text, not args.case_sensitive, args.ignore_stop_words)
    
    # Sort results
    sorted_results = sorted(result.items(), key=lambda x: x[1], reverse=True)
    
    # Limit to top N if specified
    if args.top_n:
        sorted_results = sorted_results[:args.top_n]
    def writing():
        pass
    def write_to_file():
        pass
    
    # Print results
    parser.add_argument("-o", "--output", choices=['text', 'csv'], default='text', help="Output format (text or csv)")
    if args.output == 'text':
        writing(result, args.top_n)
    elif args.output == 'csv':
        write_to_file()

if __name__ == "__main__":
    main()