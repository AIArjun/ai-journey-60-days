def word_analyzer(words):
    longest_word = words[0]
    shortest_word = words[0]
    count = 0
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word
        if len(word) < len(shortest_word):
            shortest_word = word
        if len(word) > 4:
            count = count + 1
    return longest_word, shortest_word, count

words = ["python", "ai", "code", "engineering", "ml", "data"]
longest_word, shortest_word, count = word_analyzer(words)
print("Longest:", longest_word)
print("Shortest:", shortest_word)
print("Long words count:", count)