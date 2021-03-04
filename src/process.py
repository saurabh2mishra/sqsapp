import os
import json 
import boto3
import pandas as pd
from datetime import datetime

from src.config import EndPointUrl, QueueUrl, outputfileloc
from src.logger import Logger, createdir



def get_all_messages(client, queue_url, logger, batch_size=10):
        """
        Functions to returns all consumed messages from sqs queue.
        
        :param client client: boto3 client instance.
        :param logger Logger: a logger instance
        :param int batch_size: batch size to fetch messages from queue.
        :returns list messages_list: a list of messages.
        """
        messages_list = []
        while True:
                logger.info('Consumptions started..')
                messages_consumed = []
                received_batch_messages = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=batch_size)
                try:
                        messages_list.append(
                                json.loads(
                                        received_batch_messages['Messages'][0]['Body']
                                        ))
                except KeyError:
                        logger.error("All messages are consumed. So, encountered - \
                                    Key Error while consuming the messages.", exc_info=True)
                        break
        # Commenting in order to not delete any messages from source queue.
        # delete_consumed_messages_from_queue(client, received_batch_messages, queue_url)

        return messages_list


def delete_consumed_messages_from_queue(client, received_batch_messages, queue_url):
        """
        Functions to delete all consumed messages from sqs queue.
        
        :param client client: boto3 client instance.
        :param list received_batch_messages: fetched messages
        :param string queue_url: batch size to fetch messages from queue.
        :returns Boolean : True if deletition of messages is successful.
        """
        
        entries = [{'Id': msg['MessageId'],
                        'ReceiptHandle': msg['ReceiptHandle']} 
                        for msg in received_batch_messages['Messages']]

        resp = client.delete_message_batch(QueueUrl=queue_url, Entries=entries)

        if len(resp['Successful']) != len(entries):
                error_msg =f"Failed to delete messages: entries={entries} resp={resp}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

        return True


def get_stats(messages, logger):
        """
        Functions to returns relevant stats from the received messages.
        
        :param list messages: a list of messages
        :param Logger logger: a logger instance
        :returns dict stats: a dict containing relevant stats.
        """
        if not isinstance(messages, list):
                logger.error("Invalid Type. Expected a list")
                raise TypeError("Invalid Type. Expected a list")

        messages_df = pd.DataFrame(messages)
        print(messages_df)
        messages_df['value'] = pd.to_numeric(messages_df.value, errors='coerce').fillna(0)
        df_stats = messages_df.groupby('type')['value'].agg(['count','sum']).reset_index()      
        return df_stats.to_dict(orient='records')


def write_out_file(messages, outputfileloc, logger, filename='out.txt'):
        """
        Functions to write messages in file. It creates folder on date wise and 
        write stats of the consumed messages from sqs app.
        
        :param list messages: a list of messages
        :param string outputfileloc: folder location to write the stats
        :param Logger logger: a logger instance
        :param string filename: filename to write stats on outputfileloc
        :returns None:
        """
        date_dir = datetime.today().strftime('%Y%m%d')
        path_of_outfile = os.path.join(os.sep, outputfileloc, date_dir)
        createdir(path_of_outfile)
        outfile = os.path.join(path_of_outfile, filename)
        with open(outfile, 'w') as f:
                for stat in messages_stats:
                        f.write("%s\n" % stat)
        logger.info("Stats is written in out file.")


if __name__ =='__main__':
        logger = Logger().get_logger()
        logger.info('Starting the sqs client..')
        client = boto3.client('sqs', endpoint_url=EndPointUrl)
        messages = get_all_messages(client, QueueUrl, logger)
        messages_stats = get_stats(messages, logger)
        write_out_file(messages_stats, outputfileloc, logger)
        
