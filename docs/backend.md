# Backend Details
The backend tech stack is Python with Flask RestAPIs and MySQL database with ORM tool as SQLAlchemy. There are various RestAPIs to fulfill the user interface requirements. 

> Note: There are multiple references to Lede AI, a commercial automated writing vendor. This application combines with capabilities developed by Lede AI to deliver a finished product to a newsroom's content management system.

## Flask Server Components - Python Classes

-	**dbmappers:** Map to database tables.
-	**services:** Core functionality (CRUD operations) of various services that the server needs to serve the UI requests.
-	**parsers:** Parsing capabilities for various public safety agencies. The existing parsers handle Minnesota public safety agencies in the Brainerd Dispatch's coverage area.

## REST API Endpoints
-	**/is_authenticated:** Checks if the user has an existing session.
-	**/login:** Authenticates the user and returns session_id for further user requests.
-	**/logout:** Ends the user session based on the session_id
-	**/process_blotters:** Processes the police blotter sent by the UI and parse the blotter based on the agency provided by the user.
-	**/update_parser_mappings:** *This was built for future capabilities.* It is would power a self-service matching feature in the event a police blotter's format is brand new or has changed. This could happen when registering a new agency, or perhaps when an agency changes its publication format. This endpoint is used to update the parsers fields to respective database columns. However, the feature would need to be combined with parsers that are flexible enough to return detected fields in uploaded documents.
-	**/getunpublishedreports:** Returns the list of all the unpublished reports which are ready to be sent to Lede AI
-	**/getpublishedreports:** Returns the list of all the reports which have already been published to Lede AI.
-	**/getignoredreports:** Returns the list of all the reports which are ignored by user.
-	**/publishreports:** Publish the reports selected by the user to Lede AI.
-	**/ignorecases:** Mark the list of cases selected by user as ignored.
-	**/restorecases:** Restore the ignored cases selected by the user.
-	**/agencies:** Allows CRUD operations on agency table.
-	**/publications:** Allows CRUD operations on publication table.
-	**/categories:** Allows CRUD operations on categories table.
-	**/category_priority_list:** Allows CRUD operation on priority table with respect to the category belonging to a publication.

## Entity Relationship Diagram
<img src="Brainerd ERD for Case Study.png" alt="Entity Relationship Diagram">
