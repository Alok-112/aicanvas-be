from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    try:
        # Extract and decode the base64 image
        image_data = data.image.split(",")[1]  # Assumes data:image/png;base64,<data>
        image_data = base64.b64decode(image_data)
        image_bytes = BytesIO(image_data)
        
        # Open the image using PIL
        image = Image.open(image_bytes)

        # Call the analyze_image function
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)

        # Prepare response data
        response_data = []
        for response in responses:
            response_data.append(response)

        logger.info('Responses in route: %s', response_data)

        return {"message": "Image processed", "data": response_data, "status": "success"}

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image data or processing error")
