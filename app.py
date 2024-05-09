import streamlit as st
import pandas as pd
from pandas.core.frame import DataFrame
from youtube_comment_downloader import *

def youtube_url_to_df(Youtube_URL: str) -> DataFrame:
        """Function to execute """
        try:
                # Initiate Downloader and Youtube_url
                downloader = YoutubeCommentDownloader()
                Youtube_URL = #Input Youtube video URL that you want to extract it's comment
                comments = downloader.get_comments_from_url(Youtube_URL, sort_by=SORT_BY_POPULAR)
                
                # Initiate a dictionary to save all comments from Youtube Video
                all_comments_dict = {
                        'cid': [],
                        'text': [],
                        'time': [],
                        'author': [],
                        'channel': [],
                        'votes': [],
                        'replies': [],
                        'photo': [],
                        'heart': [],
                        'reply': [],
                        'time_parsed': []
                }
                
                # Take all comment and save it in dictionary using for loop
                for comment in comments:
                        for key in all_comments_dict.keys():
                                all_comments_dict[key].append(comment[key])
                
                # Convert Dictionary to Dataframe using Pandas
                comments_df = pd.DataFrame(all_comments_dict)

                # Return df
                return comments_df
        
        except Exception as error:
                st.exception(error)
                return

def main():
        st.header("Youtube Comments Downloader Streamlit App")
        st.write("Download Comments from Youtube Video without difficulty")
        st.divider()
        url_text = st.text_input("Input Youtube URL")
        st.write(url_text)

main()
