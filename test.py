import argparse



parser = argparse.ArgumentParser(description="Count word occurrences in a text.")
parser.add_argument("text", help="The text to analyze")
parser.add_argument("-n", "--top-n", type=int, default=10, help="Show only the top N most common words")

# py test1.py "asdfljl"

args = parser.parse_args()


# result = word_conunt(args.text)
# writing(result)



def writing(result, n):
    freq = list(result.items())

    for j in freq[:n]:
        print(j)


writing({"a": 1, "b": 2, "c": 9138459}, args.top_n)