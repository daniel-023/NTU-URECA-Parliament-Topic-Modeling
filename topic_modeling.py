from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# Model Training
vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")
topic_model = BERTopic(vectorizer_model=vectorizer_model, min_topic_size=10, nr_topics=20)
topics, probabilities = topic_model.fit_transform(df['main_text'])
# Saving Topic Model
topic_model.save("parliament_topic_model")

loaded_model = BERTopic.load("parliament_topic_model")

custom_topic_names = {
    0: 'National Service',
    1: 'Healthcare',
    2: 'Media',
    3: 'National Identity/Immigration',
    4: 'Industry Safety',
    5: 'Taxation',
    6: 'Legislative Procedures',
    7: 'Transportation',
    8: 'Urban Development',
    9: 'Education',
    10: 'Expenditure',
    11: 'Departmental Budget'
}

# Topic Extraction
topic_info = loaded_model.get_topic_info().set_index('Topic')[['Count', 'Name', 'Representation']]

for topic_num in topic_info.index:
    if topic_num in custom_topic_names:
        topic_info.at[topic_num, 'Name'] = custom_topic_names[topic_num]

topic_info.to_html('Output/topic_info_table.html')

# Topic Visualisation
fig = loaded_model.visualize_topics()
fig.write_html("Output/topic_model_visualisation.html")

# Bar Chart
freq = loaded_model.get_topic_info()

# Sorting the topics by 'Count' to get the most discussed topics
freq_sorted = freq.sort_values(by='Count', ascending=False)

# Visualize top topic keywords
fig = loaded_model.visualize_barchart(top_n_topics=12)
fig.write_html("Output/top_topic_keywords.html")

