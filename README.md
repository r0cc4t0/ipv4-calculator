# IPv4 Subnets Calculator

### Application to calculate IPv4 subnets.

<br>To run this project locally, follow these steps:<br>

* **1st:** Create a virtual environment.<br>
Example: <code>python3 -m venv ipv4_venv</code><br><br>

* **2nd:** Run the virtual environment.<br>
Example: <code>source ipv4_venv/bin/activate</code><br><br>

* **3rd:** Update the pip.<br>
Example: <code>pip install -U pip</code><br><br>

* **4th:** Install the project dependencies.<br>
Example: <code>pip install -r requirements.txt</code><br><br>

* **5th:** Run the project.<br>
Example: <code>python manage.py runserver</code>

<br>To run this project with Docker, follow these steps:<br>

* **1st:** Create a build.<br>
Example: <code>docker build --no-cache -t ipv4_calculator .</code><br><br>

* **2nd:** Run the container.<br>
Example: <code>docker run -d --restart=always --name ipv4_calculator -p 8000:8000 ipv4_calculator</code>