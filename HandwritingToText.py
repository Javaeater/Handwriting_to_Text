import boto3
import base64
from anthropic import Anthropic
# Create a Textract client
textract_client = boto3.client('textract', region_name='us-west-2')
claude_client = Anthropic(
    api_key="YOUR-ANTHROPIC-API-KEY",
)

class ExtractTextFromImage():
    def handwritingToText(self, image):
      
        # Call the Textract API to detect text in the image
        response = textract_client.detect_document_text(Document={'Bytes': image})

        # Extract the detected text
        text = ''
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + '\n'

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

        # Make sure spelling and grammer are correct
        formatted_message = claude_client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Please analyze the following text extracted from an image of a notebook and determine if there are any lists, headings, bullets etc and mark it up correctly so that it can be understood by react quill with these formats avaialbe. \n\nFormats:\n header,bold, italic, underline, strike, blockquote, list, bullet.\n If the text looks like it does not need any markups just return the original text. Respond with the marked up text or original text only do not say anything else\n\nExtracted Text:\n" + message.content[0].text,
                }
            ],
            model="claude-3-opus-20240229",
        )
        # Return the extracted text 
        return (formatted_message.content[0].text})




