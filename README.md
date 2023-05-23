# Python project in a mock terminal for Code Institute

## General information

This is a project for a course in Python, Project Portfolio 3, for Code Institute by Gustaf Starhög.
The purpose of this project is to promote myself and show my skills in Python.

This project is a budget application that runs in a mock terminal in Heroku where you get to do the following things:
1. Create an account and a pincode.
2. Enter different expenses and their costs.
3. See your budget with calculations showing how much you have left to spend in total & per day of the remaining days of the month.
4. You can at anytime delete any data, or your entire account if you chose.

Link to the application: [BudgetApp](https://star-pro3.herokuapp.com/)

Image of the application: ![Welcome Message](/documentation/testing/welcome-message.png)

Disclaimer: I could not get the pyfiglet print to look the way I wanted it in the deployed terminal. I tried different fonts, sizes, widths and printing the words one by one on different lines without success. This is how it looks in the terminal on Gitpod:

![Budget app in Gitpod](/documentation/testing/welcome-vscode.png)


## Table of Contents
---
 - ## [General Information](#general-information)

 - ## [Table of Contents](#table-of-contents-1)

 - ## [UX](#UX-1)

 - ## [Project Goals](#project-goals-1)

 - ## [User Stories](#user-stories-1)

 - ## [Flowchart](#Flowchart)

 - ## [General features](#general-features-1)
    
- ## [Testing](#testing-1)
    - ## [Code Validation](#code-validation-1)
    - ## [Testing User Stories](#testing-user-stories-1)
    - ## [Future improvements](#possible-future-implementations)
- ## [Bugs](#bugs-and-fixes)

- ## [Final Result](#final-result-1)

- ## [Deployment](#deployment-1)

- ## [Github Pages](#github-pages-1)

- ## [Credits](#credits-1)
---
## UX
The UX is very limited due to the program running inside the mock terminal. However, some colors and icons were used to highlight certain information throughout the program to make it a little more pleasing to see and engage with.
The welcome message in the start of the program was used with pyfiglet, and although I did not manage to make it look the same on Heroku as in the gitpod terminal, I decided to leave it in the program.

--- 
## Project Goals

---
# User Stories

---
## Flowchart

---
## General features

--- 
## Testing

### Code Validation

### Testing User Stories

### Future improvements

---
## Bugs

---
## Final Result

## Deployment
Creating the Heroku app

Steps (It's very important that these steps are followed in the correct order):
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

---
## Github Pages

---
## Credits

---