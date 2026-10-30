# MedReport AI Cloud Demo Script (10–15 minutes)

Target length: about 12 minutes.

## 0:00–1:00 — Introduction

“Hi, I’m Hope Lekgeu, and this is MedReport AI, my Cloud Computing project.

The problem I focused on is incident documentation. Incident notes are often written quickly and can be incomplete or inconsistent. MedReport AI uses generative AI and AWS cloud services to transform unstructured incident notes into a clear, structured incident report.

This is an educational project and not a medical diagnostic system. For this demonstration I use only fictional incident data.”

## 1:00–2:30 — Architecture

Show your README architecture.

“The user interacts with a Streamlit interface. The application sends the incident notes to my MedReport AI agent.

The agent uses the Strands Agents framework and Amazon Bedrock with Amazon Nova Pro. A custom tool formats the final report into a consistent structure.

If the user chooses to save the report, the application stores it in Amazon S3. I also added application logging, AWS error handling, request validation and automated tests.”

Show:

```text
Streamlit UI
     ↓
MedReport AI
     ↓
Amazon Bedrock / Nova Pro
     ↓
Strands Agent Tools
     ↓
Structured Report
   ↙          ↘
Download     Amazon S3
```

## 2:30–4:00 — Code walkthrough

Open `medreport_agent.py`.

“This file contains the main cloud agent.

At the top I configure the AWS region, model ID and reports bucket using environment variables rather than hard-coding credentials.

The system prompt defines the agent’s role and safety rules. It tells the model not to diagnose, not to invent missing facts and to mark missing details as ‘Not specified’.”

Show `format_medical_report`.

“This custom tool creates the structured output.”

Show `save_report_to_s3`.

“This tool stores reports in S3. Each report gets a timestamp and a unique ID so objects do not overwrite one another. I also attach metadata and handle AWS errors such as AccessDenied.”

Show logging.

“I intentionally do not log the user’s incident notes. I only log operational events such as invocation start, successful completion and S3 errors.”

## 4:00–7:00 — Live UI demonstration

Start Streamlit:

```powershell
python -m streamlit run streamlit_app.py
```

Use this fictional test input:

```text
A staff member slipped on a wet floor near the reception area and injured their left wrist. They reported moderate pain and visible swelling. They remained conscious and were able to speak normally. A supervisor assisted them and recommended medical evaluation.
```

Say:

“I’ll submit fictional incident notes through the interface.”

Click Generate Incident Report.

“The application sends this text to the Bedrock-backed agent. Nova Pro extracts the important information and the formatting tool produces the structured report.”

Read only a few fields from the generated report.

“You can see the incident summary, affected person, injury, symptoms, severity, recommended action and notes.”

Show the download button.

“The user can download the report as a text file.”

## 7:00–8:30 — Amazon S3

If S3 is configured, save the report.

“I can also persist the generated report in Amazon S3 instead of keeping it only in the browser.”

Show the returned S3 success message, and if possible show the object in the AWS console.

“The object key includes a timestamp and unique report ID. S3 provides persistent cloud storage independent of the local application.”

If S3 is not configured during recording, explain the implementation and show the code instead of risking the demo.

## 8:30–9:30 — Validation and failure handling

Briefly demonstrate an empty prompt.

“The application validates requests before calling the model. An empty prompt is rejected.”

Explain:

“I also validate payload types and handle AWS SDK errors instead of allowing the application to crash.”

## 9:30–10:30 — Automated tests

Run:

```powershell
python -m unittest discover -s tests -v
```

Say:

“I added automated tests for report formatting, the health check, empty prompts, invalid payloads, missing S3 configuration, successful mocked S3 uploads and AWS AccessDenied handling.”

Show:

```text
Ran 7 tests
OK
```

“The S3 tests use mocks, so the unit test suite does not write real files into AWS.”

## 10:30–11:30 — Cloud engineering decisions

“Some important design choices in this project are configuration through environment variables, persistent object storage with S3, lazy model initialisation, structured logging, input validation, AWS exception handling and separation between the UI and agent logic.

The project also contains Docker and Bedrock AgentCore configuration for the cloud runtime.”

## 11:30–12:30 — Learning and future improvements

“Through this project I gained practical experience with Amazon Bedrock, Nova Pro, AgentCore, S3, Boto3, IAM-related access issues, Python virtual environments, logging, automated testing and building a small cloud-connected user interface.

The next improvements would be stronger CloudWatch observability, DynamoDB for searchable incident metadata, authentication, API Gateway and a more production-ready deployment of the frontend.”

## 12:30–13:00 — Closing

“To summarise, MedReport AI demonstrates an end-to-end cloud application: a user provides unstructured information, a cloud-hosted AI model processes it, application logic structures the result, and AWS services provide runtime and persistent storage.

Thank you.”
