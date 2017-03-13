# kiwi-python-weekend-entry
Kiwi.com Python weekend entry submission  
Program searches all posssible paths from airport. Restrictions are:  
1) Exactly 10 flights  
2) No visiting same country twice  
3) Last flight is not later than one year after first flight  
4) Last flight returns to source airport of first flight  

Program uses modified DFS algorithm for searching suitable paths.  

kiwi.py - Flight path searching program  
airport_country.csv - Database of airport countries  
input_data.csv - Database of flights  
