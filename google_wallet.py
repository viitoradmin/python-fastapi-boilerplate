import uuid
import os
import json
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt
from dotenv import load_dotenv

load_dotenv()
        
        
class DemoGeneric:
    """
    Thic class for authenticate with google wallet credentials, and create
    passes class and objects with jwt token.
    """
    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        self.base_url = 'https://walletobjects.googleapis.com/walletobjects/v1'
        self.batch_url = 'https://walletobjects.googleapis.com/batch'
        self.class_url = f'{self.base_url}/genericClass'
        self.object_url = f'{self.base_url}/genericObject'

        # Set up authenticated client
        self.auth()
        
    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.http_client = AuthorizedSession(self.credentials)
        
    def create_object(self, issuer_id: str, class_suffix: str,
                  object_suffix: str) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 200:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            print("**-*-*--*", response.text)
            return f'{issuer_id}.{object_suffix}'
        
        elif response.status_code != 404:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        
        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        # Creating a new object
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{class_suffix}',
            'state': 'ACTIVE',
            'textModulesData': [{
                'header': 'Text module header',
                'body': 'Text module body',
                'id': 'TEXT_MODULE_ID'
            }],
            'linksModuleData': {
                'uris': [{
                    'uri': 'http://maps.google.com/',
                    'description': 'Link module URI description',
                    'id': 'LINK_MODULE_URI_ID'
                }, {
                    'uri': 'tel:6505555555',
                    'description': 'Link module tel description',
                    'id': 'LINK_MODULE_TEL_ID'
                }]
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'https://evrc-everycred-public.s3.ap-south-1.amazonaws.com/media/1/images/cbeee1ae-9f5c-4b88-89df-3ddfac417d9d.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description'
                        }
                    }
                },
                'id': 'IMAGE_MODULE_ID'
            }],
            
            ## QR code json
            'barcode': {
                'type': 'QR_CODE',
                'value': 'https://staging-verifier.everycred.com/83243cac-b8b8-47ab-a0f4-1dbb0c8be2d2'
            },
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'ViitorCloud Technologies Pvt. Ltd.'
                }
            },
            'header': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Award Certificate'
                }
            },
            # Logo json
            'hexBackgroundColor': '#4285f4',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://evrc-everycred-public.s3.ap-south-1.amazonaws.com/media/1/images/cbeee1ae-9f5c-4b88-89df-3ddfac417d9d.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card logo'
                    }
                }
            }
        }
        # Create the object
        response = self.http_client.post(url=self.object_url, json=new_object)
    
        print('Object insert response')
        print(response.text)
        print("----------- Object ID", response.json().get('id'))
        
        new_class = {'id': f'{class_suffix}'}
        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['http://localhost:8080'],
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'genericClasses': [new_class],
                'genericObjects': [new_object]
            }
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        obj = f'https://pay.google.com/gp/v/save/{token}'

        data = {"Google wallet object": obj}
        print(data)
        return data

    
    
google_obj = DemoGeneric()
google_obj.create_object("3388000000022264908", "3388000000022264908.4f765bb1-25c9-48f9-8992-15ad6da8ef0c", "DemoObject5")