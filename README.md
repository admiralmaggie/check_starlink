# Starlink Order Status Notification
This script logs into Starlink order portal, pulls your estimated delivery date and emails it to a designated email address. 

## Requirements 
This script needs the following components:

- Python version > 3.7
- Modules noted in requirements.txt file
- Chromedriver executable for your OS (download from here: https://chromedriver.chromium.org/downloads)
- Chrome/Chromium browser
- An account with mailgun API
- Only works with US website. I have no way of testing non-us sites.

## Installation
I recommend a virtual environment:
```bash
python -m venv venv
```
Activate the newly created enviroment:
```bash
source venv/bin/activate
```
Install required modules:
```bash
pip install -r requirements.txt
```
Make sure to download and copy Chromedriver into the project directory. Some operating systems might require you to add the project location to your PATH enviroment variable.

Modify the python script and add your email API detail (mailgun) - this must be done or you won't be able to send an email:
```python
class Robotics:
    delay = 10000
    email = None
    password = None
    location = None
    mail_key = '[your mailgun API key]'
    mail_sandbox = '[your mailgun sandbox URL]'
    mail_recipient = 'recipient <email@email.eml>'
    mail_from = 'sender <email@email.eml>'
    mail_subject = 'Starlink Order Status'
```

## Email
This scrip is using mailgun mainly because I had an account with them already. Feel free to use a different method/provider.

## Usage
To use this script, provide your starlink portal email, your password, and a freeform "location" text:
```bash
source venv/bin/activate
python check_starlink.py mail@mail.eml paSSw0rd! Home
```

## Notes
This script is completely dependent on how Starlink's portal is coded. Any change by Starlink could cause issues. Keep that in mind.

## Disclaimer
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## License
[MIT](https://choosealicense.com/licenses/mit/)