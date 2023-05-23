# Python project in a mock terminal for Code Institute



## Creating the Heroku app

Steps:
1.	Create an account on https://id.heroku.com/login
2.	If you have inputs in your code, you must insert the new line code for each input at the end for the mock terminal to display your inputs correctly. The code is “\n”.
3.	You need to enter information to your credentials.txt file, as Heroku uses this file to seach for dependencies when building your application in the mock terminal. You need to enter the following command in the command terminal: “pip3 freeze > requirements.txt” Be sure to spell the command exactly like this, and make sure that the requirements.txt file is named the same way. 
4.	Make sure to commit and push theses changes before moving on.
5.	Go to Heroku’s daschboard.
6.	Click “Create a new app”
7.	Name your app (The app’s name must be unique) and choose a region
8.	Click Create app
9.	Go to the Settings tab when the app has been created.
10.	Go to the “Config Vars” (Click Reveal config vars)
11.	If you have protected any files in the gitignore file in your project we need to add config var settings for them to work(I have a file named creds.json file, I will add that one now). If you have a Google sheet API for example, follow these steps:
12.	In the field named “KEY” – enter “CREDS” (All capital letters) Then go into your creds.json file and copy the entire content. 
13.	Paste the copied content into the field named “value”
14.	Add a second KEY called “PORT” with the value “8000”.
15.	Next we need to scroll down to the buildpacks and click “Add buildpack”
16.	Click “python”, and click Save Changes. 
17.	Next we need to add another buildpack called “node.js”, click it, and then click Save Changes.
18.	Make sure that you do it in this order and the python buildpack is above the nodejs buildpack in the order. If they are in a different order, you can move python to the top after you have chosen both. 
19.	Click the “Deploy” section at the top next to the settings tab. 
20.	In the deployment method, select “GitHub”
21.	Confirm that you want to connect to GitHub, and enter your GitHub credentials(“If needed”).
22.	Now you can search for your repository that you want to deploy. 
23.	Enter your repositorys name and click “search”
24.	Then choose your repository and click connect
25.	Now you have 2 options, Automatic deploys, or Manually deploy.
26.	If you choose the automatic deploy, the code will automatically update each time you push to GitHub. Choose this option if your code is not yet finished. Otherwise you can choose Manual deploy, and click “deploy branch”
27.	When it’s done, you should see a message that says “Your app was successfully deployed” and you can click “view” to see your deployed app in the mock terminal. 
28.	You are all done and your project should now be uploaded to Heroku. 


