import os


DS_JWT = {
    "private_key": os.getenv("PRIVATE_KEY", None),
    "ds_client_id": "5da7db28-294d-45f1-95fc-c7c92a785fb4",
    "ds_impersonated_user_id": "cfc8a13b-3231-4217-95ba-f8ef09921dc5",  # The id of the user.
    #    "private_key_file": "./private.key", # Create a new file in your repo source folder named private.key then copy and paste your RSA private key there and save it.
    "private_key_file": "/Users/rus/Desktop/function/docusign_lib/app/private.key", # Create a new file in your repo source folder named private.key then copy and paste your RSA private key there and save it.
    "authorization_server": "account-d.docusign.com",
    "doc_docx": "World_Wide_Corp_Battle_Plan_Trafalgar.docx",
    "doc_pdf": "World_Wide_Corp_lorem.pdf"
}
