# Analytical Procedures with Flask (Micro web framework written in Python)

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
