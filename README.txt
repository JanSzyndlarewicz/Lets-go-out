Project team:
Jan Szyndlarewicz (100546700)
Michał Włodarczyk (100546775)
Aleksander Woźniak (100546770)

General structure of the application's interface:
 	-Find - allows you to see suggested matches, as well as respond to received invitations.
	-Invitations - allows you to see invitations that you sent and their current state; invitations that you received and which you responed to in the past; agreed-on dates (that is, invitations sent either by or to you whose status is accepted).
	-You - allows you to browse the list of liked and blocked users, as well as see your profile details. Clicking on the pencil icon allows you to modify your profile data.
	-About us - flavor text.

Additional functionalities:

Interests
Profiles contain information about the user's interests, which can be selected from a predefined list at registation and then modified at any time. This information is taken into account by the matching algorithm, which makes it more likely to be matched with a person that shares your interests.
It is also worth saying that the interests choosing is a self implemented feature on the front end

See interests_choosing.html and interest_choosing.js for the widget handling interest selection.
See algorithm.py for the way interests are incorporated in the matching algorithm.

JS with fetch for better responsibility
Many user actions that have an effect in the database like inviting, responding to invitation, liking or blocking are handled through JavaScript fetch mechanism, so that the entire page does not have to be reloaded.
check you_page.js with "pull-buttons-set" and find_page_logic.js for mentioned feature

See find_page_logic.js and profile_logic.js for examples; the corresponding jinja templates are find_page.html and profile.html, while most of flask routes used are defined in interaction.py.

Matching buffer
A particular case is the JS code servicing the Find page, which keeps a list of potential matches and only requests for new matches from the database once the list's size decreases below a defined threshold. This way there's no need to send a request to the backend each time the user rejects a suggestion (or sends an invitation).

See find_page_logic.js for implementation.

Advanced access control
Newly registered account is unconfirmed, and most functionalities are blocked until the user confirms their email address by clicking on a link in an email sent to the provided address. We also created several customs access control decorators to handle specific edge cases (for example, most pages should only be available to confirmed users, but the page informing the user that they need to confirm their email address should only be available to unconfirmed users) For testing, this functionality can be disabled by setting the ADVANCED_ACCESS_CONTROL variable in config.py file to False.

Temporary storage of data on rejections
When the user rejects a suggestion, this information is stored in the database, and the same suggestion won't be made again before a specified amount of days passes. Each day, a routine task defined using the flask-apscheduler module is performed on the server that deletes all Rejected Associations older than the defined threshold.

The routine task is defined in jobs.py and activated in the top-level __init__.py.

Form handling via Flask-Wtf
Forms are created and serviced using the flask-wtf module, which make it easy to create the forms and handle their validation in a uniform manner. We have also created several custom data validators to check that the data provided by the user is valid in the context of the application's specific characteristics and its current state.

See .py files inside forms directory for examples, and complete_profile.html for one example of usage in a jinja template, and profile_manager.py for an example of usage in a flask route. 

Age preferences range slider
Implemented with Materialize library and js dynamic slider for choosing the upper and lower age limit in registration and profile manager.

Custom CSS
In addition to third-party libraries, extensive custom CSS style sheets have been created to customise the application's appearance.

See style.css.

Reusable template components.
check templates/components



Note on users:
The table of users was populated with 100 users with randomized properties, and a special user "admin" intended for testing. Some invitations, liking and blocking relationships have also been created.
You can log in to the "admin" acocunt with account name "admin" and password "admin".
Users compatible with admin that can be suggested by the matching algorithm are
  id | username | name      |
+----+----------+-----------+
|  2 | user1    | Jennifer  |
|  4 | user3    | Maria     |
|  6 | user5    | Ashley    |
| 16 | user15   | Jodi      |
| 36 | user35   | Courtney  |
| 38 | user37   | Martha    |
| 40 | user39   | Crystal   |
| 46 | user45   | Linda     |
| 48 | user47   | Michelle  |
| 52 | user51   | Elizabeth |
| 56 | user55   | Alyssa    |
| 60 | user59   | Patricia  |
| 62 | user61   | Molly     |
| 68 | user67   | Stephanie |
| 70 | user69   | Wanda     |
| 74 | user73   | Regina    |
| 76 | user75   | Julia     |
| 86 | user85   | Kim       |
| 90 | user89   | Sydney    |
| 92 | user91   | Jeanette  |
| 94 | user93   | Heidi     |
Note that because the matching algorithm is randomised those users may be suggested in any order.
You can also login to any of the randomly generated accounts using username "user[number]", for example "user51", and password "password".
Note that by default admin is the only user with a profile picture. You can test that pictures work by creating a new account and uploading a photo at register, or accessing the profile manager from You page and adding a picture there.

Decisions on uncertainties:
We decided that liking and blocking is independent - a user that is both liked and blocked will not be suggested by the matching algorithm and their invitations will be automatically ignored, but can still be seen in the list of liked users.
Blocking is not retractive, that is invitations that were received before the user was blocked will not be automaticalluy ignored. They can still be ignored or rejected manually. 