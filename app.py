import streamlit as st
import pandas as pd
from pandas.core.frame import DataFrame
from youtube_comment_downloader import *
import io

@st.cache
def youtube_url_to_df(Youtube_URL: str) -> DataFrame:
        """Function to execute """
        try:
                # Initiate Downloader and Youtube_url
                downloader = YoutubeCommentDownloader()
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
                if Youtube_URL is not "":
                        st.exception(error)
                return None

def download_df(df: DataFrame, label: str) -> None:
        """Function to add button to download df"""
        # Option for download format
        format_download = st.radio("Pilih format download:", ['CSV', 'Excel'])
        
        # User option
        if format_download == 'CSV':
            download_format = 'text/csv'
            file_extension = 'csv'
        elif format_download == 'Excel':
            download_format = 'application/vnd.ms-excel'
            file_extension = 'xlsx'
        
        # Add download button from dataframe
        try:
                st.download_button(label=f"Download {label} DataFrame ({format_download})", data=df.to_csv(index=False) if format_download == 'CSV' else df.to_excel(index=False, engine='xlsxwriter'), file_name=f'dataframe.{file_extension}', mime=download_format)
        except Exception as error:
                st.exception(error)
        # csv_button, excel_button = st.columns(2)
        # with csv_button:
        #         st.download_button(label=f"Download {label} dataframe in CSV", data=df.to_csv(index=False), file_name = f'dataframe.csv', mime = 'text/csv')
        # with excel_button:
        #         buffer = io.BytesIO()
        #         # Create a Pandas Excel writer using XlsxWriter as the engine.
        #         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        #                 # Write each dataframe to a different worksheet.
        #                 df.to_excel(writer, sheet_name='Sheet1')
                                               
        #                 # Close the Pandas Excel writer and output the Excel file to the buffer
        #                 writer.save()
                        
        #                 st.download_button(
        #                         label=f"Download {label} dataframe in Excel",
        #                         data=buffer,
        #                         file_name="dataframe.xlsx",
        #                         mime="application/vnd.ms-excel"
        #                 )
        
def main():
        st.header("Youtube Comments Downloader Streamlit App")
        st.write("Download Comments from Youtube Video without difficulty")
        st.divider()
        url_text = st.text_input("Input Youtube URL")
        raw_df = youtube_url_to_df(url_text)
        
        if raw_df is None or False or "":
                st.info('Please enter the correct YouTube link')
        else:
                download_df(raw_df, "Raw")
                st.dataframe(raw_df)
main()
