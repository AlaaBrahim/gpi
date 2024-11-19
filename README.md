# Django App Readme

## Setup and Run Instructions

1. **Clone the Repository**  
   Clone the project repository to your local machine.

2. **Create a Virtual Environment**  
   Run the following command to create a virtual environment:  
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**  
   - On Windows:  
     ```bash
     .\venv\Scripts\activate
     ```
   - On Linux:  
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**  
   Install all required packages by running:  
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**  
   Start the Django development server with:  
   ```bash
   python .\manage.py runserver 0.0.0.0:8000
   ```

6. **Access the Application**  
   Open your web browser and navigate to:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000) if you are running the server on your local machine.
   If you are trying to access the server from a different machine on the same network, replace 127.0.0.1 with the IP address of the machine.
