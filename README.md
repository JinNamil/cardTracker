# cardTracker

This program helps you process and calculate the total amount of your credit card transactions, excluding canceled transactions and adding any custom deductions.

## Prerequisites

Before running this program, ensure you have the following:

- Python 3 installed on your machine.
- The necessary Python libraries:
  ```bash
  pip install pandas xlrd

## How to Use
1. Download Transaction Data:

    Ensure your transaction data is saved in the Downloads folder of your system. The program currently expects two files:

    - 신용카드이용내역_승인_국내통합.xls: For Shinhan credit card transactions.
    - report.xls: For Woori card transactions.
2. Running the Program:
    Run the Python script in a terminal or command prompt using the following command:

```bash
  python card_tracker_main.py
```

3. Custom Deductions:

    After processing the files, the program will ask if you want to manually subtract any additional amounts from the total. If yes, you can input the amount; otherwise, input 0 to proceed.


4. Card Types Supported:

    The program supports multiple card types, including Shinhan (Credit and Check), KB, Woori, Hana, NH, and Samsung cards. The transaction data for Shinhan and Woori cards is currently processed, but you can modify the script to support other cards by updating the respective file names and URLs.

5. Transaction Processing:

  - The program reads transaction data from Excel files, cleans and processes the data, and excludes any transactions that are considered canceled.
  - It processes two main types of transactions:

    + Credit card transactions (Shinhan): The amount is rounded to the nearest thousand if it is above 5000 (for cashback purposes).
    + Woori card transactions: Excludes certain categories (e.g., café, transportation) based on keywords.
6. Output:

    The total sum of valid transactions, along with any custom deductions, is displayed and saved to output.txt.

7. Error Handling:

    If the required files do not exist in the expected location, the program will open the corresponding card's website in your default web browser for manual download.

8. Modifying the Program:

  - You can add additional card types by updating the CARD_NAMES and CARD_URLS dictionaries.
  - If you want to modify how transactions are processed, you can change the process_transactions function as needed.
