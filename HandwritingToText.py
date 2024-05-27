import boto3
import base64
import requests
from anthropic import Anthropic

# Create a Textract client
textract_client = boto3.client('textract', region_name='us-west-2')
claude_client = Anthropic(api_key="YOUR-ANTHROPIC-API-KEY")

class ExtractTextFromImage():
    def get_image_bytes_from_url(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to retrieve image from URL: {image_url}")

    def get_image_bytes_from_local_path(self, image_path):
        with open(image_path, 'rb') as image_file:
            return image_file.read()

    def handwritingToText(self, image_path_or_url):
        if image_path_or_url.startswith(('http://', 'https://')):
            image_bytes = self.get_image_bytes_from_url(image_path_or_url)
        else:
            image_bytes = self.get_image_bytes_from_local_path(image_path_or_url)
      
        # Call the Textract API to detect text in the image
        response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

        # Extract the detected text
        text = ''
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + '\n'

        # Check for incomplete or broken text and correct it
        message = claude_client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Please analyze the following text extracted from an image and determine if any of the text is incomplete or broken. If it is incomplete or broken, please provide the corrected text. If it is complete and accurate, please respond with the original text. Only return the corrected or original text do not say anything else.\n\nExtracted Text:\n" + text,
                }
            ],
            model="claude-3-opus-20240229",
        )

        corrected_text = message['content']

        # Apply formatting for lists, headings, etc.
        formatted_message = claude_client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Please analyze the following text extracted from an image of a notebook and determine if there are any lists, headings, bullets, etc. and mark it up correctly so that it can be understood by react quill with these formats available.\n\nFormats:\n header, bold, italic, underline, strike, blockquote, list, bullet.\n If the text looks like it does not need any markups just return the original text. Respond with the marked-up text or original text only do not say anything else\n\nExtracted Text:\n" + corrected_text,
                }
            ],
            model="claude-3-opus-20240229",
        )

        formatted_text = formatted_message['content']
        return formatted_text




