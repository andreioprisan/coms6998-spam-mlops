# ML Spam Detector with SageMaker

File contents:
spam_classify_archive.zip - spam classifier files
spam-detector-stack.yml - CloudFormation recipe
parameters.json - Sagemaker endpoint details
numpy-layer.zip - Py3.8 packages with NumPy



### Step 1: Create spam-detection-storage s3 repo with source files (manual step in AWS Console)

This is used by CloudFormation to set up the stack for our Lambda and SageMaker. Upload numpy-layer.zip and spam_classify_archive.zip in spam-detection-storage.

### Step 2: Update parameters.json with Sagemaker endpoint (edit file)

### Step 3: Setup domain in SES (manual step)

Buy and set up a domain in Route 53 and set it up in SES.

### Step 4: Deploy stack with Cloudformation (CLI below)

```
 aws cloudformation deploy --template-file CloudFormationStack.yml --stack-name spam-detect --capabilities CAPABILITY_NAMED_IAM --parameter-overrides file://parameters.json  \
```

### Step 5: Active SES rule

Now that stack is live and domain is valid email receiving is enabled, enable the created email rule from CloudFormation spam-detection stack.

### Step 5: Enable S3 event in Lambda

Add trigger to lambda function  email_lambda_cloudformation and select S3 as trigger for bucket name spam-store-xyzz
 

 