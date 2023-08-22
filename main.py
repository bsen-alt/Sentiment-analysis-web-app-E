import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def convert_to_df(sentiment):
    sentiment_dict = {'polarity': sentiment.polarity,
                      'subjectivity': sentiment.subjectivity}
    sentiment_df = pd.DataFrame(
        sentiment_dict.items(), columns=['metric', 'value'])
    return sentiment_df


def analyze_token_sentiment(docx):
    analyzer = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []

    for i in docx.split():
        res = analyzer.polarity_scores(i)['compound']
        if res > 0.1:
            pos_list.append(i)
            pos_list.append(res)
        elif res <= -0.1:
            neg_list.append(i)
            neg_list.append(res)
        else:
            neu_list.append(i)

    result = {'positives': pos_list,
              'negatives': neg_list, 'neutral': neu_list}
    return result


def main():
    st.title("Sentiment Analysis from text")
    # st.subheader("Hello Streamlit")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        with st.form(key='nlpForm'):
            raw_text = st.text_area("Enter Text here")
            submit_button = st.form_submit_button(label='Analyze')

        # layout
        col1, col2 = st.columns(2)
        if submit_button:

            with col1:
                st.info("Results")
                sentiment = TextBlob(raw_text).sentiment
                st.write(sentiment)

                # emoji
                if sentiment.polarity > 0:
                    st.markdown("Sentiment:: Positive :smiley: ")
                elif sentiment.polarity < 0:
                    st.markdown("Sentiment:: Negative :angry: ")
                else:
                    st.markdown("Sentiment:: Neutral 😐 ")

                # dtaframe
                result_df = convert_to_df(sentiment)
                st.dataframe(result_df)

                # visualization
                c = alt.Chart(result_df).mark_bar().encode(
                    x='metric',
                    y='value',
                    color='metric'
                )
                st.altair_chart(c, use_container_width=True)

            with col2:
                st.info("Token Sentiment")
                token_sentiment = analyze_token_sentiment(raw_text)
                st.write(token_sentiment)

    else:
        st.subheader("About")
        st.info("This application demonstrates the sentiment analysis of input texts from user, and to analyze the polarity and subjectivity to be able to determine if the input is positive, negative or neutral, using technologies such as vaderSentiment, Streamlit, pandas, altair and textBlob")
        st.markdown("Developed for learning and experimenting by _Bawanga Senevirathne_")

    st.sidebar.markdown("Experimental demo by _Bawanga Senevirathne_")

if __name__ == '__main__':
    main()
