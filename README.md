# Email Service Demo

python v3.6.9

## Python external packages

Flask to handle the low level web protocol stuff, didn't pick Django because I wanted to use something light.

[flask](https://flask.palletsprojects.com/en/1.1.x/)

Requests for http client calls.

[requests](https://2.python-requests.org/en/master/)


## To Run:

- install dep packages

`~/<project-root>$ pip3 install -r requirements.txt`

- run the app locally

`~/<project-root>$ source .env`

`~/<project-root>$ flask run`

The app also needs api keys from Mailgun and Sendgrid, which should be provided to you.

You can append the keys to the .env file so the `source .env` step sets these variables for you.

These need to be set as `SENDGRID_API_KEY` and `MAILGUN_API_KEY` in the env var.

## Description:

A http service that utilize either Sendgrid or Mailgun to send emails.

Sendgrid is the default service. To use Mailgun, you need to set environmental variable `EXTERNAL_EMAIL_API` to `mailgun`. The app checks the env var on start. So you would have to restart the app to switch APIs.

I picked Sendgrid as the default because Mailgun requires you to have a list of verified test email accounts if you don't have a verified domain. If you'd like to see the app in action with Mailgun, I need to add the email you'd like to use in that list first.

## TODOs:

- more tests, both unit and integration

- better handling for failed external api send mail operation. Right now the errors returned from external API are all presented as 500s. These should at least be logged somewhere.

- better HTML cleaner

- maybe better email format checking, though I am not sure how valuable anything beyond basic format checking would be.

## API call example:

**Send Email**
----
Sends email
* **URL**

/email

* **Method:**

`POST`

* **Content Type:**

`application/json`

* **Data Params**

**Required**

`to=[string]`

`to_name=[string]`

`from=[string]`

`from_name=[string]`

`subject=[string]`

`body=[string]`

* ** Success Response:**

	* **Code:** 200
	
* ** Error Response:**

	* **Code:** 400 BAD REQUEST
	
	OR
	
	* **Code:** 500 INTERNAL SERVER ERROR
