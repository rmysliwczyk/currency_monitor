# Currency Monitor
#### Video Demo: https://youtu.be/pn0MEODmwdo
#### Description: 
This is my final project submission for CS50P course. This program allows users to check the value of main world currencies compared to Polish Złoty (PLN), and also convert a chosen amount to PLN and back. The source of the currency data comes from an API provided by NBP (National Bank of Poland).   
The program can be operated either by using it's GUI or via CLI. To open the program in **GUI** mode pass the **-g** argument to the program upon execution. To open the program in **CLI** mode, simply run the program without any arguments. The program is written in Python and depends on **tkinter** for the GUI, uses **requests** library to communicate with the API and **tabulate** library to represent the data visually when using CLI. Command line arguments are handled by **argparse** library.  
The main purpose of this project was to learn how to create simple user interface in a desktop environment, whilst creating a somewhat useful tool to handle real-world data. The interface of the program is aware of the global scaling of the environment, and adjusts it's window size based on that. The entirety of code that handles the GUI is contained within a separate class, allowing for the main logic to be run independently. The information about value of each currency is contained within an object of a class designed to hold all of the necessary data about the individual currency (name, code, bid, ask), which is obtained by making a call to the API.  
The codes of the currencies must be provided in ISO4217 format, i.e. three letter codes that represent a given currency. The program checks for those three letter codes by comparing an input string to a regex pattern that looks for any three letter combinations and returns them as a list, that it used to get the information from the API response. This is not strictly necessary for the GUI side of things, but is essential for the CLI, where the user chooses which currency to check for by typing the appropriate codes in. The available currency codes that can be requested from the API are the following:

-USD - United States dollar  
-AUD - Australian dollar  
-CAD - Canadian dollar  
-EUR - Euro  
-HUF - Hungarian forint  
-CHF - Swiss franc  
-GBP - Pound sterling  
-JPY - Japanese yen  
-CZK - Czech koruna  
-DKK - Danish krone  
-NOK - Norwegian krone  
-SEK - Swedish krona  

![Program window](https://i.imgur.com/kHFJrq5.png)
