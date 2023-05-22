# Image Viewer

This Python script uses `PyQt6` and `requests` libraries to create a simple image viewer application. The application fetches random images from a given set of image URLs and provides functionalities like adding images, grouping images, and connecting central points of two selected images.

## Features

1. Add random images fetched from a set of URLs.
2. Group images.
3. Connect the central points of two selected images.
4. Display image size information for the added image.

## Dependencies

1. PyQt6
2. Requests

You can install the required libraries using the following command:

```bash
pip install PyQt6 requests
```

## Usage

1. Run the script using Python:

```bash
python image_viewer.py
```

2. The application window appears with the following options/buttons:

    - Add Image
    - Group Images
    - Connect Image Centers

3. Click on "Add Image" to add random images to the scene. The script fetches random images from the set of image URLs and displays them on the screen.

4. Group Images:

    - Select multiple images by ctrl+clicking on them. (Note that just clicking on the image won't work)
    - Click "Group Images" button to group the selected images.
    - The grouped images can now be moved together as a single unit.
    - Existing Groups can also accomadate a new image ,thus creating a larger group.

5. Connect Central points:

    - Select two images to connect their centers.(ctrl+click)
    - Click on "Connect Image Centers" button.
    - A dotted line is drawn between the centers of the two images.
    - To clear the line, click on the button again.

## Customization

The script fetches random images from image URLs provided in a file named "Images.dat". The file contains a pickled list of image URLs. You can modify the URLs in the file to change the set of images that the script fetches.


- The script uses the `requests` library to fetch images from provided URLs and `QImage` and `QPixmap` classes from PyQt6 to display images within the application.
- Make sure that the downloaded image files have an appropriate file format that can be loaded by `QImage`.
- Images can be moved individually or within a selected group.
- When connecting central points, ensure that at least two items are selected.
