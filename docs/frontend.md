# Front End Details
The front end is built with React and these are the components:

> Note: There are multiple references to Lede AI, a commercial automated writing vendor. This application combines with capabilities developed by Lede AI to deliver a finished product to a newsroom's content management system.

-	**LoginPage:** Code for login page.
-	**HomePage:** This component is mounted once you login to the system. It holds the controls for all the SideBar component elements.
-	**SideBar:** It contains Home, Upload, Publish New Reports, Published Reports, Ignored Reports, Category Maintenance menu items.

> Note: The Settings menu item in the SideBar leads to an empty page. The UI component was not built out for the MVP. Maintenance tasks that would be in Settings are available through Postman scripts.

-	**Category:** Code for category maintenance where you can add remove categories into the system and assign priorities for the categories.
-	**ErrorPage:** *This was built for future capabilities.* It would be part of a self-service matching feature.
-	**Banner:** Shows banner messages.
-	**PublishNewReports:** Shows the list of all the reports which are ready to be published to Lede AI. We can also ignore them by clicking on the Ignore button.
-	**PublishedReports:** Shows the list of all the reports which have already been published to Lede AI.
-	**IgnoredReports:** Shows the list of ignored reports. We can also select any number of them and restore them.
-	**ImageUploader:** Enables us to upload the blotter for parsing by selecting the respective agency.
-	**NavBar:** A simple navigation bar.
