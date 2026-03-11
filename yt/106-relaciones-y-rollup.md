# Relaciones y rollup

**URL:** [https://www.youtube.com/watch?v=AyKDTSs5hs8](https://www.youtube.com/watch?v=AyKDTSs5hs8)
**Date:** 2021-12-23

![Relaciones y rollup](../images/106-relaciones-y-rollup.jpg)

## Transcript

**[Voiceover]**

"do you use more than one database in notion if so there may come a time when you will want to connect items across your databases this is something you can achieve with relations and rollups this video will show you how you can connect pages in a database to pages from another database that's what we call relations you will"

"also learn how to pull specific properties from a related database into another database we refer to this feature as rollup here's a workspace designed for a fictional engineering team we have two databases projects and tasks in this case tasks are the actions that make up projects so it would make sense to want to connect every task to its"

"corresponding project we'll use relations to achieve this let's have a look at this task database there are several properties in this table the first step is to add a relation property click on the plus sign at the right of your table name your new property here we'll just call it projects you'll find Rel in the advanc section at"

"the bottom click on it here you will be asked which database you want to link your table to click here then either find that database in the search bar or scroll through the drop- down select the database and hit create relation a new relation property will appear in your table now what we want to do is specify the"

"projects that the tasks are related to for example rewrite query caching logic corresponds to the performance improvements project to connect both Pages click inside the new project cell and select performance improvements here you go you can now view your project page here and access it by clicking on its name there's no need to go to the other database"

"to find it every time you link two databases to each other the changes show up in both databases you'll see that a new relations column was automatically added to the Project's database where you can also find the task page we just linked again click here to be directed to your task page rename your new column if you wish"

"finally let's very quickly link or remaining tasks to their projects all done now every project is linked to its corresponding tasks and every task is linked to its corresponding project this was relations in a nutshell now let me show you what you can achieve with rollup as I said previously this feature pulls data from one database into another"

"database in our tasks database we specifi the estimated Dev Time Each task can take what if we wanted to know how long an entire project could take go to the Project's database and now we'll need to add a rollup property to our table click on the plus sign at the right of the table and name your property go"

"to the Advan section and this time select rollup a new rollup property appears click on it then select configure rroll up this is the part where you specify the database you would like to pull your data from as well as the specific property you want to show click here and select the tasks database then click here and select"

"the property from the tasks database that you're interested in and in the calculate section select sum this will automatically calculate the total amount of De time required for this project and here you have it a time estimate for the entire project neatly showing up as a column in your Project's database this was a preview of all the useful"

"connections you can create with relations and rollups as your workpace grows you will have more opportunities to link databases that way and consequently make better sense of your data at hand"

