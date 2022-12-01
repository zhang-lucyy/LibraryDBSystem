# Future Plans

### In the future, if we were to add the ability to have popularity tiers to your system, what would need to change? For example, we want more popular books to have earlier due dates (perhaps only checkout for one week). For those books, the late fees would be higher

The master inventory table would need changing to accommodate for popularity tiers for each book.
The inventory table would have another column that keeps track of the popularity for each book.

As for API methods I would provide, I would add a method that checks the popularity tier of the book.

I would modify the add_due_date API to have more popular books have earlier due dates compared to less popular ones.
I would also modify the apply_late_fees API to add a higher fee for more popular books when they're returned late.


### In the future, if we were to add the ability to have overdue warnings to your system, what would need to change? For example, books that are overdue by more than one week have an automatic notification sent out to the user

I'm not sure if I fully understand this question but if it's just having overdue warnings, no tables would need changing or adding.

I would need to provide an API method that sends a notification to the user to remind them of their overdue book.
I would also need a method that checks if books are overdue by more than one week.

No existing API method changes.

As for extra workflow logic, I think I would need a way to keep track of the current date so the system knows if a book
is overdue. This could be done by getting the current date.