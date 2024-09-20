
# PS SCAN

This tool serves as an initial version scanner specifically designed for PrestaShop, a popular e-commerce platform. The primary purpose of the scanner is to analyze PrestaShop instances for various aspects, such as module information, version details, and potential security vulnerabilities. By leveraging techniques like web scraping and parsing, the scanner extracts relevant data from PrestaShop installations, providing valuable insights for developers, administrators, or security professionals.

The scanner currently focuses on identifying PrestaShop modules, extracting their version information, and checking for associated Common Vulnerabilities and Exposures (CVEs) by querying external databases. This can be particularly useful for users seeking to maintain an up-to-date inventory of PrestaShop modules, understand their versions, and stay informed about any known security issues.

It's essential to note that this is an initial version, and future iterations may incorporate additional features, enhanced scanning capabilities, and improved accuracy. The tool aims to contribute to the ongoing efforts of PrestaShop administrators and developers in maintaining a secure and well-managed e-commerce environment.

# !!! You using this tool on your own responsibility !!!




# Change log 

### Version [1.0.3] - 2024-08-17
#### Added
- scripts will check default modules Prestashop
- Add default user-agent

#### Fixed
- add information when program start without variables
- separate method to parse XML config file


# Coming soon 

- check .git directory in modules
- check Prestashop API
