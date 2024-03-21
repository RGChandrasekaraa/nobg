# nobg

## Introduction

`nobg` is a background removal application that provides an easy-to-use interface for removing backgrounds from images. It is built with Python and Tkinter, leveraging the power of the `rembg` library for image processing.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Setup

To set up the application, follow these steps:

1. Clone or download the `nobg` application from its repository.
2. Navigate to the directory where you downloaded `nobg`.
3. Install the necessary dependencies by running:

pip install -r requirements.txt

This command will install `Pillow` and `rembg`, which are required for the application to function.

## Usage

To use the application, run the Python script:

python nobg.py

This will open the GUI. Follow these steps to remove the background from an image:

1. Click the 'Upload Image' button to select an image from your computer.
2. Wait for the application to process the image. A status label will indicate when the processing is complete.
3. Once processed, the original and the background-removed images will be displayed side by side.
4. Click the 'Save Processed Image' button to save the image without a background.
5. If you want to clear the images and reset the application, click the 'Clear' button.

## Contributing

Contributions to `nobg` are welcome. Please feel free to submit pull requests or issues to improve the functionality or address any bugs.
