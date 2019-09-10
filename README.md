## Document Explorer Test App
* Web user interface for creating collections and documents.
* Sort/search/filter collections and documents.
* pytest selenium based framework.

## Test Configuration
* Web browser/ Web driver:
   - Mozilla Firefox: 69.0
   - Google Chrome: 76.0.3809.132
   - [geckodriver v0.24.0](https://github.com/mozilla/geckodriver/releases/tag/v0.24.0)
   - [chromedriver 76.0.3809.126](https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/)
 
* Packages:
    ```bash
    - Python 3.7.0+
    - pytest-4.3.1+
    - selenium-3.141.0+
    - pytest-html-1.22.0+
    ```   
* Update the drivers based on your test environment (OS, browser version etc)
  ```bash
  # Refer these locations
  {PROJECT_HOME}/DocumentExplorerTest/drivers/
  {PROJECT_HOME}/DocumentExplorerTest/conftest.py
  ```

* Logging Configuration.
  ```bash
  # Update this file.
  {PROJECT_HOME}/DocumentExplorerTest/logger.cfg
  ```
  
## Usage
Update ``` ${PROJECT_HOME}/utils/document_explorer.py```
```python
 self.app_url = "<ENTER_APP_URL>"
 self.test_user_name = "<ENTER_USER_NAME>"
 self.test_user_password = "<ENTER_PASSWORD>"
```
```bash
$ cd {PROJECT_HOME}
$ pytest tests --html=report.html
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.