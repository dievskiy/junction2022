import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients

from ...consts import demo_docs_path, pattern
from ...jwt_helpers import create_api_client


class Eg002SigningViaEmailController:

    @classmethod
    def worker(cls, args, doc_docx_path, doc_pdf_path):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args, doc_docx_path, doc_pdf_path)
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args, doc_docx_path, doc_pdf_path):
        """
        Creates envelope
        Document 1: An HTML document.
        DocuSign will convert all of the documents to the PDF format.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        # document 1 (html) has sign here anchor tag **signature_1**
        #
        # The envelope has two recipients.
        # recipient 1 - signer
        # recipient 2 - cc
        # The envelope will be sent first to the signer.
        # After it is signed, a copy is sent to the cc person.

        # create the envelope definition
        env = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )
        doc1_b64 = base64.b64encode(bytes(cls.create_document(args), "utf-8")).decode("ascii")

        document1 = Document(  # create the DocuSign document object
            document_base64=doc1_b64,
            name="NDA",  # can be different from actual file name
            file_extension="html",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )

        env.documents = [document1]

        # Create the signer recipient model
        signer1 = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1"
        )
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # create a cc recipient to receive a copy of the documents
        cc1 = CarbonCopy(
            email=args["cc_email"],
            name=args["cc_name"],
            recipient_id="2",
            routing_order="2"
        )

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        sign_here1 = SignHere(
            anchor_string="**signature_1**",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1], carbon_copies=[cc1])
        env.recipients = recipients

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env

    @classmethod
    def create_document(cls, args):
        """ Creates document 1 -- an html document"""

        return f"""
        <!DOCTYPE html>
        <html>
            <head>
              <meta charset="UTF-8">
            </head>
            <body style="font-family:sans-serif;margin-left:2em;">
            <h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
                color: darkblue;margin-bottom: 0;">Junction 2022</h1>
            <h2 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
              margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
              color: darkblue;">NON-DISCLOSURE AGREEMENT</h2>
            <h4>Ordered by {args["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer_email"]}</p>
            <p style="margin-top:1em;">
                I. Confidential Information. This Agreement shall govern the conditions of disclosure by Releasor to Recipient of certain Confidential Information. "Confidential Information", as used herein, means all engineering and business information (including prototypes, drawings, data, trade secrets and intellectual property) which:
            </p>
            <p style="margin-top:0.7em;">
                i. if tangible, is identified in writing as confidential at the time of its disclosure to the recipient; or
            </p>
            <p style="margin-top:0.7em;">
                ii. if intangible, is identified at the time of disclosure to the recipient as confidential and is later promptly confirmed in writing within one (1) month from the date of disclosure as being confidential.
            </p>
            <p style="margin-top:0.7em;">
                The term Confidential Information shall exclude information which:
            </p>
            <p style="margin-top:0.7em;">
                i. is known or possessed by the Recipient at the time of its disclosure to the recipient;
            </p>
            <p style="margin-top:0.7em;">
                ii. is publicly known at the time of disclosure to the recipient;
            </p>
            <p style="margin-top:0.7em;">
                iii. is subsequently received by the Recipient from a third party without restriction on disclosure;
            </p>
            <p style="margin-top:0.7em;">
                iv. subsequently becomes publicly known without violation of this Agreement;
            </p>    
            <p style="margin-top:0.7em;">
                v. is independently developed by the recipient without access to the Confidential Information; or
            </p>
            <p style="margin-top:0.7em;">
                vi. is disclosed by recipient pursuant to a requirement of a law, regulation, or legal process with regard to the Confidential Information.
            </p>
            <p style="margin-top:0.7em;">
               II. Governing Laws. The laws of <b>Finland</b> shall govern this Agreement and its validity.
               <b>Releasor’s Signature</b> <b><i>Signature</i></b> Date <b>05.11.2022</b>.
               Print Name: <b>Inventor</b>
            </p
            <p style="margin-top:1em;">
               Recipient’s Signature: <span style="color:white;">**signature_1**/</span> Date: <b>05.11.2022</b>
               Print Name: <b>Signer</b>
            </p>
            </body>
        </html>
      """

