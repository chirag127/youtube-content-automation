import webbrowser

syllabus = "Arithmetic logic unit,Look ahead carries adders,Multiplication,Signed operand,multiplication using Booths algorithm,array multiplier,Division & logic operations,Floating point arithmetic operation,Arithmetic & logic unit design,IEEE Standard for Floating Point Numbers,"

topic_list = syllabus.split(",")

# define the functiont to search all item the topic-list on youtube

topic_list_len = len(topic_list)

for i in range(0, topic_list_len):
    topic = topic_list[i]
    search_url = f"https://www.youtube.com/results?search_query={topic}&sp=EgIQAQ%253D%253D"
    webbrowser.open(search_url)
