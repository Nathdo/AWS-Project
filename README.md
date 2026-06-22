# ML Integration - Cloud Architecture Project

Final project for the AWS Cloud Systems Management course. This project implements a serverless, AI-driven web application designed to predict and recommend specialized employment training tracks for the Haredi population in Israel using a custom Machine Learning model.

## AWS Services Utilized
* **Amazon S3:** Hosts the static frontend web application (HTML/Tailwind/JS) and securely stores the ML model artifacts (`model.tar.gz`).
* **Amazon API Gateway:** Acts as the front door, providing a secure REST API with CORS configurations to bridge the frontend UI with the backend logic.
* **AWS Lambda:** Serverless compute (Python/Boto3) that acts as the controller, orchestrating requests between the API, the ML model, and the database.
* **Amazon DynamoDB:** A fully managed NoSQL database used to maintain a persistent audit trail of all candidate inputs, prediction scores, and timestamps.
* **Amazon SageMaker:** Hosts the custom PyTorch machine learning model on a dedicated endpoint (`ml.m5.large`) for real-time, low-latency inference.
* **AWS IAM:** Ensures strict security by enforcing the principle of least privilege through dedicated Execution Roles.
* **Amazon CloudWatch:** Provides comprehensive monitoring, logging, and error tracking for the Lambda executions and API requests.

## System Architecture
The application is built on a highly decoupled, Serverless architecture:
1. The user inputs demographic data via the web interface (hosted on **S3**).
2. The browser sends an HTTP POST payload to **API Gateway**.
3. API Gateway triggers the **Lambda** function.
4. Lambda invokes the **SageMaker** endpoint to process the data and generate a probability score.
5. Lambda logs the input variables, timestamp, a unique UUID, and the prediction result into **DynamoDB**.
6. Lambda formats the response with the appropriate CORS headers and returns it through the API to the user's screen.

## Installation & Deployment Instructions
As a fully cloud-native application, no local server setup is required. To run and test the system:
1. Ensure the **Amazon SageMaker Endpoint** is running and in the `InService` state within the AWS Console.
2. Navigate to the public **Amazon S3 website endpoint URL**.
3. Fill out the candidate's demographic features in the web form.
4. Click **"Analyze Candidate Profile"**. The system will perform the real-time cloud inference, display the business recommendation on-screen, and securely log the transaction in the database.
