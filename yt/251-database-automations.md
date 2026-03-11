# Database automations

**URL:** [https://www.youtube.com/watch?v=R8IOW72zfMY](https://www.youtube.com/watch?v=R8IOW72zfMY)
**Date:** 2023-08-30

![Database automations](../images/251-database-automations.jpg)

## Transcript

**[Voiceover]**

"if you constantly find yourself updating project statuses tagging team members to review tasks or sending out reminders to slack you can free up your time and put project management on autopilot with database automations in this video we'll show you how to create customized database automations that can change your project or task status reassign task owners update entries in"

"a related database send slack notifications and much more before we start just note that this feature is exclusive to certain plan types you can learn more at notion.com pricing you can use the lightning bolt icon at the top right of any database to see if you have it database automations are sequences of actions that happen anytime a specific"

"change to a database page occurs an automation consists of two parts the first one we call a trigger it's what sets off the entire automation process and the second one is an action it's what happens automatically after the trigger occurs in other words an automation consists of saying when any of these triggers occur do this action or series"

"of actions a trigger can take many shapes or forms and maybe when a page gets added to the database or when a property on a page gets edited when a trigger fires you could decide on the following actions either send a notification to slack make new edits to a page property add a page to another database edit pages"

"in another database or any combination of the above here's how to create a database Automation in a few simple steps we'll start with our tasks database while you can create automations in any notion database they're uniquely powerful in helping you manage your projects and tasks to create an automation you can either go to the options menu and select"

"automations or simply click on the lightning bolt icon all your automations will show up here but since we don't have any yet let's go ahead and click new automation to create one you can name your automation we'll call this one QA flow and then start selecting triggers and actions you'll see a drop down menu next to four pages"

"in this lets you choose whether you want your automation to apply to all pages in this database or only pages that appear in one of your saved filtered views note that if you or someone else adjust the filters in a saved view that will affect the pages your automation applies to in this case we want our automation to"

"apply to any page in the tasks database in this example whenever a Page's status changes to ready for QA we want to automatically assign the page to Santiago our QA engineer to do this we'll click add trigger in the drop down let's select status and only pick the ready for QA option when you're ready hit done great now"

"whenever this trigger occurs in a page we'll want to sign it to our QA engineer let's click add action then hit the assignee property now we can look up Santiago's name in the search bar and click on it when it shows up like so again click done lovely the last step is to click on the blue create button"

"to save the automation now when a Page's status is set to ready for QA the assignee property will automatically feature Santiago's name super note that you can expect the same result when someone adds a new page to the database and marks it as ready for QA now if you are a project manager here's an automation for you here"

"we're going to create a kickoff workflow whenever a project status is changed to up next we want to automatically create a project kickoff meeting at our meeting notes database as well as send a notification to Slack let's click on new Automation and call this one project kickoff this time the trigger event will be the status property being changed"

"to up next now in the actions menu we'll select add page 2 and find our company's meeting notes database let's call the new page that is being created project kickoff we can set the meeting type to project kickoff next let's click on the plus sign to add another action let's also send a slack notification to the product Channel"

"over slack workspace to notify others of the new project being tackled again hit create to save the automation great let's give our new automation a try when the Page's status is changed to up next a new project kickoff meeting is created in our meeting notes database and the product team will get notified of this change in our product"

"channel in Slack now keep in mind that when an automation contains the slack action such an action can only be edited by the person who created the notification in the first place on the other hand any automations regarding the Page's status can be created edited deleted disabled and enabled by anyone with full access to the database in question"

"which brings us to our last point to keep an automation active leave its blue toggle on but you can also decide to pause it in which case you'll just have to untoggle you can do this as many times as you please as you can see notion's database automations take just a minute or two to set up I can"

"save you a ton of time as well as make sure no important updates fall through the cracks instead of worrying about maintaining your projects and tasks databases and constantly notifying your team members about changes you can get on with work that matters most [Music]"

