# eCommerce Project Setup

This guide provides instructions for setting up and running the eCommerce project on your local development environment.

## Setup Instructions

### 1. Open the Repository

Navigate to the repository directory in your terminal:

cd path/to/ecommerce

### 2. Activate the Virtual Environment
Activate the virtual environment by running the following commands:

For Windows:

cd my_env\Scripts

activate

For macOS/Linux:

source my_env/bin/activate

### 3. Install Required Packages
Change the directory to the project root where requirements.txt is located, and install the necessary packages:

cd ../../

pip install -r requirements.txt

### 4. Migrate the Models
Apply the database migrations to set up your database schema:

python manage.py migrate

### 5. Start the Development Server
Run the development server to start the project:

python manage.py runserver
