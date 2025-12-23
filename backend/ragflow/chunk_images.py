# Added by Judy >>>>>>>>>>>>>>>>>>>>

import asyncio
import logging
from io import BytesIO
from pathlib import Path
from typing import AsyncIterator

from PIL import Image

from .constants import IMAGE_DIR, IMAGE_TYPES
from .files import get_file_type

# RAGFlow logger
ragflow_logger = logging.getLogger("ragflow")


def resize_image_longest_side(
    img: Image.Image,
    img_max_length: int | None = None,
) -> Image.Image:
    """
    Resize the image so that the longest side is equal to `img_max_length`.
    Make sure to keep aspect ratio.

    Args:
        img (Image.Image): The original image.
        img_max_length (int, optional): The maximum image side length. Default is `None`. Least is `32`.

    Returns:
        resized_img (Image.Image): The resized image.

    Raises:
        ValueError: If `img_max_length` is less than 32.
    """

    # Validate `img_max_length` is valid
    if img_max_length and img_max_length < 32:
        err_msg = f"The input value `img_max_length` ({img_max_length}) must be at least 32."
        ragflow_logger.error(err_msg)
        raise ValueError(err_msg)

    # Return the original image directly if satisfied with some conditions
    width, height = img.size
    longest = max(width, height)
    if img_max_length is None or longest <= img_max_length:
        ragflow_logger.info(f"There is no need to resize the image; return origin directly.")
        return img

    # Resize the image
    ragflow_logger.info(f"Start to resize the image's longest side from {longest} to {img_max_length}.")

    scale = img_max_length / float(longest)
    ragflow_logger.info(f"The scale is {scale}.")

    new_width = max( 1, int(round(width * scale)) )
    new_height = max( 1, int(round(height * scale)) )
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # LANCZOS gives high-quality downsampling

    ragflow_logger.info(f"Resize the image successfully from ({width}, {height}) to ({new_width}, {new_height}).")
    return resized_img


async def get_image_iterator(
    img: Image.Image,
    img_type: str = "jpeg",
    reading_size: int = 4096,
) -> AsyncIterator[bytes]:
    """
    Generate an image iterator for delivering this image.

    - The image type `webp` will be converted to `jpeg`.
    - The image type `png` will be kept as origin to preserve transparency potential.
    - Otherwise, default to `jpeg` because of smaller photos.
    - If the image type is `jpeg`, ensure `RGB` because it doesn't support alpha.

    Args:
        img (Image.Image): The image.
        img_type (str): The image type. Default is `jpeg`. Only supports `jpeg`, `jpg`, `webp` and `png` now.
        reading_size (int): The size of each reading. Default is `4096` bytes. Least is `1`.

    Yields:
        iterator (AsyncIterator[bytes]): The image iterator.

    Raises:
        ValueError: If the image type is not supported.
        ValueError: If `reading_size` is less than or equal to 0.
    """

    # Validate `img_type` is valid
    if f".{img_type.lower()}" not in IMAGE_TYPES:
        err_msg = f"The image type ({img_type}) is not supported. Only supports {IMAGE_TYPES} now."
        ragflow_logger.error(err_msg)
        raise ValueError(err_msg)

    # Validate `reading_size` is valid
    if reading_size <= 0:
        err_msg = f"The input value `reading_size` ({reading_size}) must be at least 1."
        ragflow_logger.error(err_msg)
        raise ValueError(err_msg)

    # Encode PIL Image to BytesIO without saving to disk
    buf = BytesIO()
    if ( img_type.lower() ) in ("jpeg", "jpg", "webp"):
        if img.mode != "RGB":
            img = img.convert("RGB")
        format = "JPEG"
        img.save(buf, format=format, quality=90, optimize=True)
    elif ( img_type.lower() ) == "png":
        format = "PNG"
        img.save(buf, format=format, optimize=True)
    else:
        format = "JPEG"
        img.save(buf, format=format)
    ragflow_logger.info(f"Encode the image as type '{format}' to BytesIO successfully.")

    # Generate the image iterator
    ragflow_logger.info(f"Start to generate the image iterator.")
    buf.seek(0)
    while True:
        block = buf.read(reading_size)
        if not block:
            break
        yield block
        # Generate an awaitable suspension point to release control back to the event loop 
        # doing other things, avoiding sticking to the server
        await asyncio.sleep(0)
    ragflow_logger.info(f"The image generator is to the end.")


async def get_image_iterator_by_path(
    img_path: str | Path,
    img_max_length: int | None = None,
    reading_size: int = 4096,
) -> AsyncIterator[bytes]:
    """
    Generate an image iterator by image path for delivering this image.

    Args:
        img_path (str | Path): The image path.
        img_max_length (int, optional): The maximum image side length. Default is `None`. Least is `32`.
        reading_size (int): The size of each reading. Default is `4096` bytes. Least is `1`.

    Yields:
        iterator (AsyncIterator[bytes]): The image iterator.

    Raises:
        ValueError: If `img_max_length` is less than 32.
        ValueError: If the image type is not supported.
        ValueError: If `reading_size` is less than or equal to 0.
        FileNotFoundError: If the image path is not found.
    """

    img_abspath = IMAGE_DIR / Path(img_path)

    # Validate the image path exists
    if not img_abspath.is_file():
        err_msg = f"The image path ({img_path}) is not found."
        ragflow_logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    # Read the image
    img = Image.open(img_abspath)  # Use the image path to open directly
    img.load()  # Load the image to memory forcefully to avoid 'ValueError: seek of closed file'
    ragflow_logger.info(f"Read the image from path '{img_path}' successfully.")

    # Scale the image
    img = await asyncio.to_thread(resize_image_longest_side, img, img_max_length)

    # After resizing, we don't need to close Pillow Image manually until garbage is collected
    # Otherwise, closing early will raise 'ValueError: seek of closed file' in an async situation
    # img.close()

    # Generate the image iterator
    image_type = t[1:] if ( t := get_file_type(img_abspath) ) else ""  # Remove the first character '.'
    iterator = get_image_iterator(img, image_type, reading_size)

    return iterator

# <<<<<<<<<<<<<<<<<<<< Added by Judy
