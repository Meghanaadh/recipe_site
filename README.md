FlavorVerse Recipe Website

This is the project page for FlavorVerse, an online space for finding and sharing recipes. It's designed for everyone, from experienced cooks to those just starting their culinary journey.

The application's backend is built using Python and the Flask framework, with Tailwind CSS handling the visual styling to maintain a clean and simple look.

Application Features

The homepage offers a selection of featured recipes to provide initial inspiration.

A dedicated page allows users to browse the entire collection of submitted recipes.

Each recipe has a detailed view showing its ingredients, a picture, and step-by-step cooking instructions.

Users can contribute their own recipes through a straightforward submission form.

The website is designed to be responsive, ensuring it works well on mobile devices, tablets, and desktops.

Technology Stack

The core technologies used to build this project are:

Backend: Python, Flask

Database: SQLite

Frontend: HTML, Tailwind CSS

Icons: Feather Icons

Local Setup and Installation Guide

To run this project on your own computer, you will need to have Python 3 installed.

Installation Steps:

First, download a copy of the project's code. You can do this by cloning the repository.
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

It is recommended to create a virtual environment. This isolates the project's dependencies from other Python projects on your system.
For Windows:
python -m venv venv
venv\Scripts\activate

For macOS or Linux:
python3 -m venv venv
source venv/bin/activate

Next, install the required packages listed in the requirements.txt file.
pip install -r requirements.txt

You can now run the application. This will start the local development server.
python app.py

To view the website, open a web browser and go to the address https://www.google.com/search?q=http://127.0.0.1:5000.

The application is set up to automatically generate a database file (recipes.db) with a few sample recipes the first time it is run.

Thank you for your interest in the FlavorVerse project. We hope you find it useful.