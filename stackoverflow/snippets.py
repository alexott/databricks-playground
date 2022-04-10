# Requires com.databricks:spark-xml_2.12:0.14.0

# TODO: normalize column names - remove `_`, switch to snake case

posts_schema = "`_AcceptedAnswerId` BIGINT, `_AnswerCount` int,`_Body` STRING,`_ClosedDate` TIMESTAMP,`_CommentCount` int,`_CommunityOwnedDate` TIMESTAMP,`_ContentLicense` STRING,`_CreationDate` TIMESTAMP,`_FavoriteCount` int,`_Id` BIGINT,`_LastActivityDate` TIMESTAMP,`_LastEditDate` TIMESTAMP,`_LastEditorDisplayName` STRING,`_LastEditorUserId` BIGINT,`_OwnerDisplayName` STRING,`_OwnerUserId` BIGINT,`_ParentId` BIGINT,`_PostTypeId` BIGINT,`_Score` int,`_Tags` STRING,`_Title` STRING,`_ViewCount` BIGINT"
df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "posts").schema(posts_schema).load("/Users/ott/tmp/stackoverflow-vi/Posts.xml")

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "badges").load("/Users/ott/tmp/stackoverflow-vi/Badges.xml")
badges_schema = "`_Class` BIGINT,`_Date` TIMESTAMP,`_Id` BIGINT,`_Name` STRING,`_TagBased` BOOLEAN,`_UserId` BIGINT"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "comments").load("/Users/ott/tmp/stackoverflow-vi/Comments.xml")
comments_schema = "`_ContentLicense` STRING,`_CreationDate` TIMESTAMP,`_Id` BIGINT,`_PostId` BIGINT,`_Score` BIGINT,`_Text` STRING,`_UserDisplayName` STRING,`_UserId` BIGINT"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "posthistory").load("/Users/ott/tmp/stackoverflow-vi/PostHistory.xml")
post_histroy_schema = "`_Comment` STRING,`_ContentLicense` STRING,`_CreationDate` TIMESTAMP,`_Id` BIGINT,`_PostHistoryTypeId` BIGINT,`_PostId` BIGINT,`_RevisionGUID` STRING,`_Text` STRING,`_UserDisplayName` STRING,`_UserId` BIGINT"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "postlinks").load("/Users/ott/tmp/stackoverflow-vi/PostLinks.xml")
post_links_schema = "`_CreationDate` TIMESTAMP,`_Id` BIGINT,`_LinkTypeId` BIGINT,`_PostId` BIGINT,`_RelatedPostId` BIGINT"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "tags").load("/Users/ott/tmp/stackoverflow-vi/Tags.xml")
tags_schema = "`_Count` BIGINT,`_ExcerptPostId` BIGINT,`_Id` BIGINT,`_TagName` STRING,`_WikiPostId` BIGINT"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "users").load("/Users/ott/tmp/stackoverflow-vi/Users.xml")
users_schema = "`_AboutMe` STRING,`_AccountId` BIGINT,`_CreationDate` TIMESTAMP,`_DisplayName` STRING,`_DownVotes` BIGINT,`_Id` BIGINT,`_LastAccessDate` TIMESTAMP,`_Location` STRING,`_ProfileImageUrl` STRING,`_Reputation` BIGINT,`_UpVotes` BIGINT,`_Views` BIGINT,`_WebsiteUrl` STRING"

df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "votes").load("/Users/ott/tmp/stackoverflow-vi/Votes.xml")
votes_schema = "`_BountyAmount` int,`_CreationDate` TIMESTAMP,`_Id` BIGINT,`_PostId` BIGINT,`_UserId` BIGINT,`_VoteTypeId` BIGINT"

#df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "posts").load("/Users/ott/tmp/stackoverflow-vi/")

#df = spark.read.format("xml").option("rowTag", "row").option("rootTag", "posts").load("/Users/ott/tmp/stackoverflow-vi/")

