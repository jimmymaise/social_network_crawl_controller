import boto3


class SQSHandler:
    def __init__(self, region_name=None):
        self.sqs_client = boto3.client('sqs', region_name=region_name) if region_name else boto3.client('sqs')

    def send_sqs_message(self, message_body, queue_name):
        sqs_queue_url = self.sqs_client.get_queue_url(QueueName=queue_name)
        response_msg = self.sqs_client.send_message(QueueUrl=sqs_queue_url,
                                                    MessageBody=message_body,
                                                    )
        return response_msg

    def retrieve_sqs_messages(self, queue_name, num_msg=1, wait_time=0, visibility_time=3600, ):
        if not 1 <= num_msg <= 10:
            raise ValueError('Num msgs must be >=1 and <=10')
        sqs_queue_url = self.sqs_client.get_queue_url(QueueName=queue_name)
        response_messages = self.sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                                            AttributeNames=['All'],
                                                            MaxNumberOfMessages=num_msg,
                                                            MessageAttributeNames=['All'],
                                                            WaitTimeSeconds=wait_time,
                                                            VisibilityTimeout=visibility_time)
        return response_messages

    def retrieve_first_sqs_message(self, queue_name, visibility_time=3600):
        msg_list = self.retrieve_sqs_messages(queue_name=queue_name, visibility_time=visibility_time)
        return msg_list[0] if msg_list else None

    def delete_sqs_message(self, queue_name, msg_receipt_handle):
        sqs_queue_url = self.sqs_client.get_queue_url(QueueName=queue_name)
        delete_response = self.sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=msg_receipt_handle)
        return delete_response
