Project team:
Jan Szyndlarewicz
Michał Włodarczyk
Aleksander Woźniak

General structure of the application's interface:
 	-Find - allows you to see suggested matches, as well as respond to received invitations.
	-Invitations - allows you to see invitations that you sent and their current state; invitations that you received and which you responed to in the past; agreed-on dates (that is, invitations sent either by or to you whose status is accepted).
	-You - allows you to browse the list of liked and blocked users, as well as see your profile details. Clicking on the pencil icon allows you to modify your profile data.
	-About us - flavor text.

Additional functionalities:

Interests
Profiles contain information about the user's interests, which can be selected from a predefined list at registation and then modified at any time. This information is taken into account by the matching algorithm, which makes it more likely to be matched with a person that shares your interests.

See interests_choosing.html and interest_choosing.js for the widget handling interest selection.
See algorithm.py for the way interests are incorporated in the matching algorithm.

JS with fetch for better responsibility
Many user actions that have an effect in the database like inviting, responding to invitation, liking or blocking are handled through JavaScript fetch mechanism, so that the entire page does not have to be reloaded.

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

Custom CSS
In addition to third-party libraries, extensive custom CSS style sheets have been created to customise the application's appearance.

See style.css.

Example user and possible matches

Our understaing of how things are supposed to work (por ejemplo can you invite blocked users, should liked users that are no longer compatible show up in likes).