# TDXLib (TeamDynamix Python SDK)

TDXLib is a suite of Python libraries originally designed to take input from Google Sheets and create tickets in [TeamDynamix](https://teamdynamix.com) based on the contents of the sheets. The scope of the project has broadened past its humble beginnings, and continues to do so whenever there's a feature we need that it doesn't currently support.

## Quick Links
* [ReadTheDocs.io Documentation](https://tdxlib.readthedocs.io) - TDXLib Class & Method descriptions
* [TeamDynamix API Documentation](https://api.teamdynamix.com/TDWebAPI) - Descriptions of all TDX API Endpoints

## Dependencies

* Python 3.6+
* requests
* python-dateutil
* gspread (for Google Sheets integration -- not an official dependency)
* oauth2client (for Google Sheets integration -- not an official dependency)

## Getting Started

1. [Download](https://www.python.org/) and install Python 3.6 or later. If you're new to Python, check out this [setup tutorial](https://realpython.com/installing-python/ "Python 3 Installation & Setup Guide"). For an introduction to basic Python syntax and use, check out the guides on [python.org](https://www.python.org/about/gettingstarted/) 

   *NOTE: although Python comes pre-installed on MacOS and many GNU/Linux systems, it's often version 2.7. For GNU/Linux, install python3 packages if available. For MacOS, check out [homebrew](brew.sh).*

2. Clone or download TDXLib from [GitHub](https://github.com/cedarville-university/tdxlib).

3. Install the required dependencies to your environment using `pip`, which is bundled with Python 3.4+. If you run into issues on Windows, be sure that the location of your Python installation is specified in your system's `PATH` variable.

    The necessary packages are specified in `requirements.txt` and can be installed with `pip` 
    
    If your OS comes with Python 2.7, use `pip3` or whatever the name of the Python 3.6+ pip binary is on your system. A [virtual environment](https://docs.python.org/3/library/venv.html) can be helpful here:

       pip install -r requirements.txt

    Alternatively, install all the packages manually:

       pip install requests python-dateutil
    
    To get the libraries necessary to work with Google Sheets (as in the [sample script](examples/example_ticket_generation.py)), you can also install them with `pip`:
        
       pip install gspread oauth2client

4. Import TDXLib into your console or script: 
        
       import tdxlib
    
5. To interact with the TDX API, you'll need to create an api integration object, through which all of the TDXLib commands are run. TDXLib currently supports two types of integrations:

   * **TDX Ticket Integration (Tickets, Ticket Tasks, etc.)**
   
         my_tdx_integration = tdxlib.tdx_ticket_integration.TDXTicketIntegration()

   * **TDX Asset Integration (Assets, CIs, etc.)**
         
         my_tdx_asset_integration = tdxlib.tdx_asset_integration.TDXAssetIntegration()

6. In order to store settings, TDXLib uses a INI-style configuration file. 
   If there is no file set up in your working directory, TDXLib will walk you through the generation of one the first time you instantiate an integration object:
  
   <pre>
        $ python
        Python 3.7.3 (...) [...] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        >>> <b>import tdxlib</b>
        >>> <b>tdx = tdxlib.tdx_ticket_integration.TDXTicketIntegration()</b>
        No configuration file found. Please enter the following information:
        
        Please enter your TeamDynamix organization name.
        This is the teamdynamix.com subdomain that you use to access TeamDynamix.
        Organization Name (<orgname>.teamdynamix.com): <b>myuniversity</b>
        
        Use Sandbox? [Y/N]: <b>yes</b>
        
        TDX API Username (tdxuser@orgname.com): <b>myuser@myuniversity.edu</b>
        
        TDXLib can store the password for the API user in the configuration file.
        This is convenient, but not very secure.
        Store password for myuser@myuniversity.edu? [Y/N]: <b>no</b>
        
        Tickets App ID (optional): <b>123</b>
        
        Assets App ID (optional): <b>456</b>
        
        TDXLib uses (mostly) intelligent caching to speed up API calls on repetitive operations.
        In very dynamic environments, TDXLib's caching can cause issues.
        Disable Caching? [Y/N]: <b>no</b>
        
        Initial settings saved to: tdxlib.ini
   </pre>

    The generated file will look something like this:

        [TDX API Settings]
        'orgname': 'myuniversity',
        'sandbox': True,
        'username': 'myuser@university.edu',
        'password': 'Prompt',
        'ticketAppId': '123',
        'assetAppId': '456',
        'caching': True
     
    The `orgname` field is whatever subdomain your organization uses to access TeamDynamix. For example, `https://myuniversity.teamdynamix.com`.

    The `sandbox` field specifies whether TDXLib should interact with a sandbox version of the TDX Environment, which is written over by production monthly. It is recommended to use the sandbox environment when first getting familiar with the API environment.

    The `username` and `password` fields are the login credentials for an account to be used with the TeamDynamix API. Many API endpoints (such as creating objects in TDX) require elevated permissions beyond the average user. You may need to create a user specifically for use with TDXLib and grant permissions based on what you need to do.
    
    If the `password` field is set to `'Prompt'`, then whenever a new integration object is made, it will request a password, and dispose of the password after getting an API token: 
    
       Enter the TDX Password for user myuser@myuniversity.edu (this password will not be stored):   

    The `ticketAppId` and `assetAppId` fields are the numbers that appear after `Apps` in your TeamDynamix URL, and are specific to your organization. For example: 
    
    Tickets: `https://myuniversity.teamdynamix.com/TDNext/Apps/{ticketAppId}/Tickets/...`  
    Assets: `https://myuniversity.teamdynamix.com/TDNext/Apps/{assetAppId}/Assets/...`

    The `caching` field specifies whether or not TDXLib should cache TeamDynamix objects such as valid ticket types, statuses and priorities. Setting this option to `True` reduces the volume of API calls and allows TDXLib to perform some batch operations much faster.

    You can optionally specify an alternative configuration file that TDXLib should search for in your working directory. By default, it will look for `tdxlib.ini`.

        >>> tdx = tdx_ticket_integration.TDXTicketIntegration("specialconfig.ini")

    Depending on your `tdxlib.ini` settings, you may be prompted for a password to authenticate into the TeamDynamix API. Once everything is working, go ahead and test out a method:

        >>> accounts = tdx.get_all_accounts()

7. Congratulations! You now have the power of the TeamDynamix API at your fingertips. For information on the methods included with TDXLib, check out our documentation on [ReadtheDocs.io](http://tdxlib.readthedocs.io).
    

##  TDXLib Implementation status and Future Plans

* ### TDXIntegration:

    This base class that contains the methods necessary to authenticate to Teamdynamix. This class also contains methods to interact with TeamDyanamix objects that are universal across various Apps (Locations, People, Accounts, etc.)

    Currently Implemented:
    * Authentication (only simple auth, no loginadmin or SSO)
    * Locations & Rooms (read-only)
    * People & Groups (read-only) (no group members)
    * Accounts (read-only)
    * Custom attributes for Tickets & Assets (read-only)
    * Import & Export of TDX-Style DateTime objects into python datetime objects

    Future Plans:
    * Read-write support for Locations, Rooms, People, Groups, Accounts, and Custom Attributes
    * Support for custom attributes in Projects, CIs
    * Support for manipulating attachments
    * Support for inspecting/manipulating group members
    * Support for inspecting/manipulating roles & user lists
    * Support for mass-importing users from uploaded excel files

    Unlikely to be supported:
    * Time entries
    * Time types

* ### TDXTicketIntegration:

    The class (inherited from TDXIntegration) that allows interactions with Ticket objects.

    Currently Implemented:
    * Ticket Priorities
    * Ticket Statuses (including creation of custom statuses) (WIP)
    * Ticket Types
    * Ticket Urgencies
    * Ticket Sources
    * Ticket Impacts
    * Ticket Classifications (not available directly through API)
    * Ticket Forms (not available directly through API)
    * Tickets:
        * Creation (including templated batch-creation from Google Sheets)
        * Editing (including batch-editing of multiple )
        * Manipulating
        * Searching (by any attribute)

    Future Plans:
    * Support for Ticket Tasks
    * More documentation on how to get started with TDXTicketIntegration library

    Unlikely to be supported:
    * Blackout Windows
    * Ticket Searches/Reports

* ### TDXAssetIntegration:

    The class (inherited from TDXIntegration) that allows interactions with Asset objects.

    Currently Implemented:
    * (Not much)
