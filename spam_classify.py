import json
import boto3
import email
import datetime
import os

import sms_spam_classifier_utilities as utilities


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # bucket = "spam-store-xyzz"
    # key = "ej7dotrac0gfp3b5q1h97l4rbatvlvsvq02pfa81"
    session = boto3.Session()
    s3_session = session.client('s3')
    response = s3_session.get_object(Bucket=bucket, Key=key)
    email_obj = email.message_from_bytes(response['Body'].read())
    from_email = email_obj.get('From')
    body = email_obj.get_payload()[0].get_payload()    
    ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
    runtime = session.client('runtime.sagemaker')
    vocabulary_length = 9013
    input_mail = [body.strip()]
    temp_1 = utilities.one_hot_encode(input_mail, vocabulary_length)
    input_mail = utilities.vectorize_sequences(temp_1, vocabulary_length)
    date = email_obj["Date"]
    print(date)
    data = json.dumps(input_mail.tolist())
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType='application/json', Body=data)
    res = json.loads(response["Body"].read())

    if res['predicted_label'][0][0] == 0:
        label = 'Ok'
    else:
        label = 'Spam'
    score = round(res['predicted_probability'][0][0], 4)
    score = score*100


    message = "We received your email sent at " + str(email_obj.get('To')) + " on date " + date  + " with the subject " + str(email_obj.get('Subject')) + ".\nHere \
is a 240 character sample of the email body:\n\n" + body[:240] + "\nThe email was \
categorized as " + str(label) + " with a " + str(score) + "% confidence."

    email_client = session.client('ses')
    response_email = email_client.send_email(
        Destination={'ToAddresses': [from_email]},
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Spam analysis of your email',
            },
        },
        Source=str(email_obj.get('To')),
    )
    print(response_email)
    return {}
    
    
    
    
# event = []
# context = []
# lambda_handler(event, context)


