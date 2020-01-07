# Analytical Procedures with Flask (Micro web framework written in Python)
 
This web app is built for my Final Thesis Project *Why Big Data Analytics should be an integral part of Accounting?* which I concluded under Prof. Jeanette Shown at Goshen College. It is built with jQuery and Bootstrap as Frontend and Flask(Python) as backend. This is built to show how quickly by using programming languages such as Python you can analyze the general ledger and run audit tests on it. Currently the app works on a particular General ledger extracted from a certain businuess but it can easily be extended to work on different General Ledgers or if someone is working/auditing certain company's General Ledger, they can customize it for only that company as well.

Following analytical procedures have been implemented:

| Analytical Procedures  | Description |
|----------------|-------------|
|Check Unbalanced Journal Entries| It checks for all the Journal Entries which are unbalanced or in other words debits is not equal to credits|
|Check Journal Entries On Weekend|It checks all the Journal entries for a specific weekend(selected by the user) as these can be suspicious because most of the entries are posted during the week days|
|Check Higher Dollar Journal Entries|It checks Journal entries which are higher than specific amount entered by user. It helps auditor to find the Journal Entries whose dollar amounts are suspicious.|
|Check Round Dollar Journal Entries|It checks Journal Entries whose dollar amount are multiples of 100s. Round number testing is relevant to AU-C Section 240; AU-C Section 315, Understanding the Entity and Its Environment and Assessing the Risks of Material Misstatement; and AU-C Section 520, Analytical Procedures.|
|Check a sample of Journal Entries|It obtains a sample number(entered by the user) of Journal entries|
|Check Journal Entries by Month|It check Journal Entries for the specific month|
|View Scatter Plot of Debits or Credits|Viewing scatter plot gives you a Visual way to look at the Range of Debits or Credits. By range I meant the range of dollars that what is the highest amount and what is the lowest.|


### Run the web app on your local machine

1 - Clone the repo to your local machine.

2 - Go to the repo in command line.

3- Do the following:

    $ export FLASK_APP=app.py (Mac OS) or set FLASK_APP=app.py (Windows)

    $ flask run

### Contributions are welcome

1 - Fork the repo.

2 - Clone it, create a branch and make changes.

3 - Submit pull request.


