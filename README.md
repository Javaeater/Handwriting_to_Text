
## ABOUT
This is a simple script to extract hand written text and attempt to turn it into a digital note marked up by quill.

### Installation
`Make sure AWS enviornment is setup and has permissons to use Textract.`

`Pip install anthropic`

`Replace api key with your api key`

`Pass in an a local or web url image for text to be read`

## Example Useage

`extractor = ExtractTextFromImage()`

`image_path_or_url = "https://example.com/path/to/your/image.jpg"  # or "local/path/to/your/image.jpg"`

`result_text = extractor.handwritingToText(image_path_or_url)`

`print(result_text)`

