######################################
-------------FIFA SOCCER GAME APPLICATION------------------

1. This application displays the games played during the FIFA games 2022. User needs to login with a username. Once logged in, user needs to input the date in the format MM-DD-YYYY and it shows all the games played on that day. 
2. For API call, example:
      a. http://127.0.0.1:2224/getdata/alldata
      b. http://127.0.0.1:2224/getdata/11-22-2022
3. The results being displayed are from 11-20-2022 to 11-28-2022 only at the moment.
4. Example API call result below:
            [
      {
      "score": "6-2",
      "team1": "England",
      "team2": "Iran",
      "winner": "England"
      },
      {
      "score": "0-1",
      "team1": "Senegal",
      "team2": "Netherlands",
      "winner": "Netherlands"
      },
      {
      "score": "1-1",
      "team1": "USA",
      "team2": "Wales",
      "winner": "Draw"
      }
      ]

######################################
