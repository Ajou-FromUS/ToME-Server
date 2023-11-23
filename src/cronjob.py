from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 한글 폰트 패스로 지정
import matplotlib.font_manager as fm
import re
import collections
import glob
from datetime import datetime
import numpy as np
import schedule
import time
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
import os

from core.config import Settings


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=Settings.S3_ACCESS_KEY,
                             aws_secret_access_key=Settings.S3_SECRET_KEY,
                             region_name=Settings.S3_REGION)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

def get_all_logs_with_uid_and_month(text_log_base_path:str,uid:str,year:str,month:str)->str:
    text_log_path = "/".join([text_log_base_path,uid])
    text_log_name = "-".join([year,month,"*"])+".txt"
    path = text_log_path+"/"+text_log_name

    total_string = ""

    for filename in glob.glob(path):
        file = open(filename,'r')
        for line in file.readlines():
            content = line.split('-')[1]
            total_string=total_string+"\n"+content
        file.close()
    
    return total_string

def get_uid_list(text_log_base_path:str)->list:
    uid_list=[]
    for uid_path in glob.glob(text_log_base_path+"/*"):
        uid=uid_path.split('/')[-1]
        uid_list.append(uid)

    return uid_list

def color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl({:d},{:d}%, {:d}%)".format(np.random.randint(227,228),np.random.randint(82,100),np.random.randint(62,95)))
    
def create_wordcloud(wc:WordCloud,uid:str,log_content:str,year:str,month:str):
    wc.generate(log_content)

    plt.figure(figsize=(10,8))
    plt.imshow(wc)
    plt.tight_layout(pad=0)
    plt.axis('off')
    dir_path=Settings.KEYWORD_IMG_PATH+"/"+uid+"/"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = year+"-"+month+'.png'
    plt.savefig(dir_path+file_path)

    upload_file(dir_path+file_path,Settings.S3_BUCKET_NAME,"keywords/"+uid+"/"+file_path)

def make_img_job():
    print(datetime.now(),"MAKE IMG JOB START")
    text_log_base_path=Settings.CHAT_LOG_PATH

    now = datetime.now()
    year = str(now.year)
    month = str(now.month)

    spwords=set(STOPWORDS)
    wc=WordCloud(max_font_size=200,stopwords=spwords,background_color="white",
                 width=480,height=360,font_path="AjouTTF.ttf",
                 color_func=color_func,max_words=10,
                 margin=25)

    uid_list=get_uid_list(text_log_base_path)

    for uid in uid_list:
        log_content=get_all_logs_with_uid_and_month(text_log_base_path,uid,year,month)
        create_wordcloud(wc,uid,log_content,year,month)
    
    print(datetime.now(),"MAKE IMG JOB DONE")


if __name__ == "__main__":
    schedule.every().day.at("00:00").do(make_img_job)
    while 1:
        schedule.run_pending()
        time.sleep(60)
    # make_img_job()