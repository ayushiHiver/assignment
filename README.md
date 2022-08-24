# assignment
onboarding assignment

# msg_create.py
This file contains script to send message from "ayushi.s@grexit.com" to "userashrivastava@gmail.com" (userA account) with subject "Training Exercise". Label is 
created as "Training Exercise" if not already present. "gmail.storage" is created inside the current folder when the sender is authenticated. 

# pubsub.py
Topic is created on userA account.
This file contains script to watch for the changes in the mailbox of userA using watch() and stop(). All the unique msgids are captured in a set. Then the 
message corresponding to these is inserted into userB,C,D accounts.

# question2_sendmsg.py
Reply msg is sent from B to A.

# question2_pubsub.py
C and D will also receive the reply in the same thread.

If Email E3 is sent to users A and B, duplicates are not created in C and D. Since we are writing individual scripts without server, so we have the control
over whom to authenticate for subscription.
