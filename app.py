
import streamlit as st
import pandas as pd
from io import StringIO
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title(" Chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # it convert to string

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show anaylsis"):
        

        num_messages , words , num_media_message, links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1 ,col2 ,col3 ,col4 = st.columns(4)

        with col1:
            st.header("Total meassage")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Share image")
            st.title(num_media_message)
        with col4:
            st.header("NO. LINKS")
            st.title(links)

        #timeline
        st.title("Monthly Timeline")
        timeline =helper.monthly_timeline(selected_user,df)
        fig , ax =plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='red')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #dailytimeline
        st.title("Daily Timeline")
        daily_timeline =helper.daily_timeline(selected_user,df)
        fig , ax =plt.subplots()
        ax.plot(daily_timeline['daily_date'],daily_timeline['message'],color = 'blue')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1 , col2 = st.columns(2)

        with col1 :
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig , ax =plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig) 

        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig , ax =plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig) 

        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig , ax =plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        




        # finding users in group level
        if selected_user == "Overall":
            st.title("most busy user")
            x ,new_df=  helper.most_busy_users(df)
            fig , ax =plt.subplots()

            col1 ,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig , ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


    
        # most comman words
        most_common_df = helper.most_column_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most common words')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)
        st.title("Emoji Analysis")
        col1 ,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels = emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)

        st.dataframe(most_common_df)

      