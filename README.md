The project contains a cloud function which send an NDA document to the email. Function uses the docusign_lib library based on DocuSign API example.
To deploy:
```
terraform init
terraform plan
terraform apply
```
To test:
```
curl -m 70 -X POST <FUNCTION-URL> -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"signer_email": "user@gmail.com", "signer_name": "User", "cc_email": "user@gmail.com", "cc_name": "User"}'
```
