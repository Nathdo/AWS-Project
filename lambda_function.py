import json
import boto3
import uuid
from datetime import datetime

sagemaker_client = boto3.client('sagemaker-runtime')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HarediPredictions')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        response = sagemaker_client.invoke_endpoint(
            EndpointName="Haredi-Serverless-Endpoint",
            ContentType="application/json",
            Body=json.dumps(body)
        )
        
        result = json.loads(response['Body'].read().decode('utf-8'))
        score = result['prediction']
        
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        table.put_item(
            Item={
                'PredictionId': prediction_id,
                'Timestamp': timestamp,
                'Inputs': json.dumps(body),
                'Score': str(score)
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({"prediction": score})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": str(e)})
        }