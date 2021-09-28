# hh-analyzer
Analysis of vacancies from HeadHunter   

This software application is implemented in Python 3.8 in the PyCharm Professional 2020.3.3 development environment.   

This application collects information on vacancies from the HeadHunter API in the form of .json files, a total of 17.5 GB of data was received. Next, we import this data into the ClickHouse BD columnar analytical database on a remote machine running Ubuntu AWS from Amazon.   

The work has been done to analyze vacancies by various filters, for example, the most paid vacancies by city, the most demanded ones have grown, the average salary in recent months by city, etc.   

The data obtained after analysis is presented in the form of graphs using the Plotly library for data visualization and hosted on the Flask web server on the Heroku cloud.

