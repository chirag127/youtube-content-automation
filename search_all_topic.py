import webbrowser


# syllabus = """Virtual Instrumentation,Graphical programming techniques,Data types,Advantage of Virtual Instrumentation techniques,Concept of WHILE loop,FOR loop,Arrays,Clusters,graphs,Structure: Case,Structure: Sequence ,Structure: Formula nodes,Need of software based instruments for industrial automation."""

# Concept of Searching, Sequential search, Index Sequential Search, Binary Search.Concept of Hashing & Collision resolution Techniques used in Hashing. Sorting: Insertion Sort,Selection, Bubble Sort, Quick Sort, Merge Sort, Heap Sort and Radix Sort


syllabus = "concept of searching,sequential search,index sequential search,binary search,concept of hashing,collision resolution techniques used in hashing,insertion sort,selection,bubble sort,quick sort,merge sort,heap sort,radix sort"

topic_list = syllabus.split(",")

# define the functiont to search all item the topic-list on youtube

topic_list_len = len(topic_list)

for i in range(0, topic_list_len):
    topic = topic_list[i]
    search_url = f"https://www.youtube.com/results?search_query={topic}&sp=EgIQAQ%253D%253D"
    webbrowser.open(search_url)

