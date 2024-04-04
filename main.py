"""
Global Investment Recommender System
This is the main file for our project, Global Investment Recommender System, a comprehensive
application designed to assist users in making informed investment decisions based on a blend of
economic performance and ethical considerations across various countries. The system guides users
through a selection process involving multiple investment criteria, including geographical region,
economic development status, sector of interest, and ethical priorities, to suggest suitable
countries for investment.

Using the application:
-   Download all the required packages mentioned in requirements.txt.
-   Run this file.
-   Fill out the form according to your preferences; If the form is completed inaccurately,
    our application will assist you in making the necessary corrections.
-   Once submitted with valid inputs, a popup dialog will display, stating
    "Form successfully submitted." Press OK, and the output screen will appear, showing a
    list of countries visualized using bar graphs and tables to recommend relevant countries.
-   Example Input and Output:
    Input:
        Region: 'Americas'
        Economic Development Status: 'Developed'
        Investment Terms: 'Long Run'
        Sector: 'Tertiary'
        Ethical Priority:
            Environment: 1
            Equity: 2
            Fair Labour Treatment: 3

    Output (Mentioning only the countries, not their scores,
    however the scores will be displayed on the output screen.)
        - Canada
        - United States

Copyright © 2023 Global Investment Recommender System (GIRS). All rights reserved.
"""
from application import run

if __name__ == '__main__':
    run()
