Based on this:
How I Built a Social Network in 4 Years as a Solo Developer
A behind-the-scenes look into my journey
Mario Stopfer


Immersive Communities — A Social Media Platform for Content Creators
This is a story, a full exposé, of my solo-dev project, Immersive Communities — a social media platform for content creators, which I took up in early 2018 and completed in 2022. I hope it will serve as a guide to anyone who is starting a large project or is in the middle of building one and needs the motivation to keep going.

The Idea
Way back in early 2018, faint voices started emerging. People began to voice their opinion on the state of the web and social media in general. Some people were dissatisfied with Facebook and its policies on user privacy; others were complaining about YouTube and its monetization practices, while others turned their opinion against the platforms where they were voicing their opinion, like Medium.com.

But what would the alternative to all of these look like?

The Solo-Dev Project — A History in the Making
The idea to build a social media platform came from the desire to give content creators the ability to create content as individuals, engage with their community, and contribute to the content creation process. They can also monetize their efforts — all in one place.

The platform should be free to use, and anyone should be able to join. The creators, who invest time into their work, which educates and entertains people worldwide, should also be able to make a living from what they love doing.

Would any of this solve all the problems we face online today? No, but it’s an alternative, and that’s what counts. It’s a seed that can, over time, turn into something beautiful.

As a technologist, I also wondered if a single person could do all of this. Would it be possible for a single person to step up to the challenge and deliver a robust, enterprise-level platform that people would love using, and if yes, what would it take to deliver such a system?

To be completely honest, I didn’t have an answer to those questions, but I decided to take up the challenge.

In those early days of 2018, I had around six years of work experience as a software developer, mostly backend .NET and some WPF on the frontend. I have also been living in Tokyo, where I moved less than three years ago, and working overtime was the norm. The idea of taking up additional work was unreasonable.

If it wanted to be available to as many people as possible, the platform would need to be a website. With almost no web development experience, none of this seemed achievable.

The fact that it seemed impossible, was exactly why I decided to start sooner rather than later. Would all of this be a giant waste of time? Only time would tell, but the sooner I started, the sooner I would find out the answer.

Then, on February 1st of 2018, I started planning.

2018 — The Plan
The first thing I decided to do was to tell myself — to think this would not be easy would be an understatement of the century. I had never done anything like this before, so I literally had no idea what I was getting myself into.

This meant no hobbies or anything resembling a life until this thing was completed. Working overtime at my full-time job and then coming home and working on this project would become the new norm. Would I take a vacation and travel at some point? Yes, but I would have to spend these vacations mostly working as well.

If I’ve learned anything from my previous experience, it’s that being organized makes or breaks your project and keeps you on track. The more you prepare and design upfront, the less trial-and-error work you need to do later.

Thinking and planning are easier than building and less time-consuming, so the more I do in the planning phase, the less I would have to discover during the actual development phase, which requires more time.

I didn’t have resources, so I had to make up for that with planning and design. I also knew that the web was the place to go when I got stuck, but I decided not to ask new questions on Stack Overflow for this project.

The reasoning behind this decision was quite simple. Seeing there will be a lot to learn here, if I go and ask someone to solve all my problems, I wouldn’t gain any experience. The further the project progresses, the harder it will become, and I will not have gained any experience to tackle it on my own.

Therefore, I decided only to search the web for already existing answers but not to ask new questions to solve my problems. Once the project was done, I could engage with Stack Overflow again, but it would be off-limits for this particular development goal.

I would utilize the OOAD approach to designing the system I wanted to build. The system would tell me how each part works and how it interacts with other parts of the system. Furthermore, I would extract business rules which I would later implement in code.


Early notes for product reviews
I then started taking notes and realized there were two main points I had to focus on:

Project design
Tech stack
Since I knew there were only 24 hours in a day, and most of those I’ll be spending either at work or traveling, I had to optimize my time carefully.

Project Design
For the project design part, I decided to look at which products already worked well and use those as inspiration to maximize my time.

Clearly, the system needs to be fast and accessible to everyone, and since I don’t have time to write code for multiple platforms, the web was the answer.

I then turned to design. Apple, being well known for its well-accepted design practices, was an immediate source of inspiration. Next, I turned to Pinterest and decided that this was the simplest possible design that worked well. The idea behind my decision was the old saying.

“Content is king.” — Bill Gates, 1996.

This gave me the idea of removing as many unnecessary design details as possible and focusing on presenting the content. If you think about it, people will come to your website once because it has a nice design, but they won’t return unless you have good content.

This had the effect of reducing the time required to design the frontend.

The system itself had to be simple. Every user should be able to create and own their own community. Other users should be able to join as members and write articles to contribute content to this community. This feature would be inspired by Wikipedia, where many users can edit the same article.

If many people are engaging together on a certain topic, this tells us that what we have at hand is a community and, as such, should be separate from the rest.

As far as features go, users would need to be able to write regular articles and connect them as Wikipedia does, and also reviews, which would require a different type of article. Thus, regular articles would be called “Interests” and would be factual and informational in nature, with anyone being able to edit them. On the other hand, “Reviews” would be based on each interest, and only the review’s author could edit it.

In short, people could collaboratively write about a movie, let’s say “The Matrix,” and edit that article whenever they want. They could add any factual information to the article they wanted.

Then, each user could write their own review of that movie. Naturally, the original article would then show a list of all the reviews for this movie.

It was clear to me that I also had to add two more important features. The first would be a search option for articles in each community. The other feature was recommendations, which the users would be served based on what they liked once they scrolled to the end of the article.

Each user should also be able to post short updates or “Activities” to their profile, which would act as a Wall on Facebook. This was the basic outline that I made before I started thinking of the technologies which I could use to actually deliver the project.

The Tech Stack
The second thing I focused on was the tech stack. Since I had already decided I would build a web-based project, I decided to write down all the popular and modern technologies that were most commonly used at that time. I would then choose those technically as close to what I already used in my career to spend as little time as possible learning new technologies.

Furthermore, the idea that led my thinking the most during this phase was to make design decisions that would require me to write as little code as possible, thus saving time.


Immersive Communities Tech Stack
After extensive research, I settled on the following main Tech Stack:

NodeJS
PWA
Serverless
Aurelia JS
AWS Cognito
AWS AppSync
AWS DynamoDB
AWS Kinesis
AWS Cloudfront + S3
Terraform
Furthermore, by choosing SaaS services, I would further save time because I would not need to implement these features by myself. The services I decided on were as follows:

Cloudinary
Embedly
Algolia
Recombee
Locize
Twilio
Stripe
These were the main technologies I had to learn as quickly as possible to even begin working on the project. Everything else would have to be learned along the way.

At this point, I started learning new technologies. For the main and most important ones, I started reading the following books:

Amazon Web Services in Action
Serverless Architecture on AWS
Aurelia in Action
What is WebPack
Cognito Dev Guide
CloudFront Dev Guide
DynamoDb Dev Guide
Serverless GraphQL with AppSync
Terraform Up and Running
Progressive Web Apps
I decided I would work on my full-time job during the day, but evenings were a fair game. When I would come home, I could study until I went to sleep. As far as sleep goes, I would cut it down to six hours to gain more time to study.

I initially predicted I would only need a year to build this project. Then, after almost a year of learning new technologies, it was December of 2018, and I had just finished the main reading material while having written exactly zero lines of code.

The Development Starts
In December of 2018, I finally started developing. I set up Visual Studio Code and started building out my development environment.

It was clear to me from day one that I would not be able to maintain all the servers necessary for such a large project. Not just from a technical perspective but also the budget side. Thus, I had to find a solution.

Luckily, I found the solution in the form of DevOps and the Serverless approach to back-end infrastructure. Even before these approaches became widespread as they are today, it was immediately clear to me that if we can describe something succinctly with code, we can also automate it, saving time and resources.


CI/CD Pipeline for the Backend Infrastructure
With DevOps, I would unify and automate both the front-end and back-end development, while with Serverless, I would remove the need for server maintenance and lower the cost of operation as well.

This philosophy clearly went along with my thinking, and the first thing I decided to set up was a CI/CD pipeline with Terraform.

The design consisted of three branches: Development, UAT, and Production. I would work each day, and when the work was done, I would commit the changes to the Development branch in AWS CodeCommit, which would trigger AWS CodeBuild to build my project.


CI/CD Pipeline for the Immersive Communities Front End
I would keep a Terraform executable in the repository for macOS, local testing, and Linux to build on CodeBuild. Once the build process started, the Terraform executable would be invoked inside CodeBuild, and it would pick up the Terraform code files, thus building out my infrastructure on AWS.

All of these parts would then have to be connected and automated, which I did using AWS’s CodePipeline, which would move the code from CodeCommit to CodeBuild every time I made a commit. This would help me keep my code and my infrastructure in sync. Whenever I was ready to move forward, I would merge the Development branch to UAT or the UAT to Production to sync my other environments.

2019 — COVID-19 Hits
Once I finished the CI/CD pipeline for the backend, I would turn to setting up the actual website locally to start developing the frontend.

The initial step of setting up the frontend was to create an Aurelia-based project. The decision behind using Aurelia and not React, which was and still is the most popular choice for a JavaScript framework, was because of the MVVM pattern.

The MVVM pattern is prominently used in WPF desktop apps which I had experience with. Thus, learning React would have taken more time than simply building on what I already knew.

On the other hand, the decision to use Aurelia and not Angular or Vue was based on the philosophy behind Aurelia, which is to have the framework get out of your way. In other words, there is no Aurelia in Aurelia. What you are using while developing with Aurelia is HTML, JavaScript, and CSS, with some added features like data binding to attributes. I was already familiar with these.

Therefore, the decision was final. Next, coming from the C# world, which is statically typed, I decided to go with TypeScript over JavaScript.

Next came WebPack. There was a clear need to split the application into chunks, facilitating lazy loading. Since I already knew that there were going to be many features in the app, it was imperative to build it as a SPA that would be able to load parts on demand. Otherwise, the user experience would be unacceptable.

To make it easier to handle the WebPack configuration, I added Neutrino.JS to the mix and used its fluent interface to set up WebPack.

It was well known that mobile web browsing was on the rise even back in 2019. To be ready for the modern web, the development approach was defined as follows:

Mobile-first
Offline-first
This was facilitated by two main technologies: Tailwind CSS and PWA. When it comes to styling, to simplify the system more, I added Tailwind CSS. This turned out to be one of the best decisions I made since it is mobile-first by default. Also, it is utility-based. Thus, it has high reusability, which was exactly what I was looking for.

Furthermore, since I was trying to offer a native-like experience but had no time to build native apps, I decided to go for the next best thing — an app that could be directly installed from the browser and worked offline.

This is what Progressive Web Apps (PWA) aim to give to the user, but a manual setup would be too error-prone and time-consuming. Thus, I decided to use Google WorkBox, which has the Service Worker installation, offline, and caching features built-in.

Once the core was set up, it was time to take it for a ride online. It was clear that the website should be accessible to anyone at all times, outages do not belong in a modern system, so I decided to set up the system in the following way.

Firstly, the HTML and JS files will be served from an AWS S3 bucket. AWS CloudFront CDN Network will front it to make it available with low latency globally.

A slight setback, in this case, was when I also decided to use the Serverless Framework because setting up AWS Lambda functions were easier than with Terraform. Thus, I introduced a new technology that I had to take care of.

Once the setup was done, I bought the domains in AWS Route 53, which I used for testing, and the production domain. https://immersive.community.

The idea behind the name comes from a similarly named community-based network — Mighty Networks. I decided on the word “Immersive” since, at that time, it started highly trending on Google. Since “immersive.networks” and “immersive.communities” were already taken, I settled on “immersive.community.”

Now that I had the frontend launched, it was time to start working on the database. Even though I was used to SQL-based, relational databases in the past, they were clearly too slow for this particular project, so I decided to go with a NoSQL database. I chose AWS DynamoDB because of its Serverless offering.

To access the database, I chose AWS AppSync, a managed GraphQL implementation that is also serverless.

A Multi-Tenant System
At this point, it was time to start solving one of the biggest problems I faced, namely:

How to allow users to join multiple communities but keep the private or restricted data, in each community, separate from each other?

The easiest way to solve this problem would be to create multiple databases, but this has clear limitations because, at some point, we would run out of databases we could create. It turns out that each AWS account has limitations on how many resources you can create, so this was not a viable solution.

Finally, I would solve this problem by assigning a type column to each entry in the DynamoDB database. Each user would have its type set to “user,” while each community would be set as “web.”

I would then indicate that a user has joined a community by adding a new row where the key of this row is designated as “user#web_user#web.” Since the user and the community name would be unique, this key would also be unique, so the user couldn’t join the community multiple times.

If I want to perform an action that can only be performed if a user has joined a community, I would use Pipeline Functions provided by AppSync, which allows you to query for multiple rows in DynamoDB. I would then query and check if the user is a member of a community and only if they are, allow the user to perform the action.

This solved the multitenancy problem, but one of the largest problems to solve was just around the corner.

Highly Available Architecture
An enterprise-level system is built with fault tolerance and high availability in mind. This would allow users to continue using the system, even if there are failures in some of its components. If we want to implement such a system, we should do it with redundancy in mind.

My research leads me to the optimal solution in this case, which is an Active-Active Highly Available architecture. It turns out that most services on AWS are already highly available, but AppSync itself is not. Thus, I decided to create my own implementation.

The web didn’t solve this problem, so I had to build my own. I started thinking globally. Meaning my visitors would be coming from different regions, and if I were to place my AppSync in the US, then the visitors in Asia would have a higher latency.

I solved the latency and high availability problem in the following way. I’ve decided to create ten different AppSync APIs in all available regions at that time. Currently, the APIs are located in the US, Asia, and Europe.


Highly Available Active-Active Architecture
Furthermore, each API needs to be connected to the corresponding DynamoDB database in the same region. Thus, I further created additional ten DynamoDB tables.

Luckily, DynamoDB offers a Global Table feature that copies the data between the connected DynamoDB tables and keeps them in sync. Now, regardless of where a user writes to the database, a user in a different region would be able to read that same information after the data gets synced.

The question that now arose was the following:

How would users be routed to the closest API? Not only that, but if it were the case that one API were to fail, how would we immediately route the call to the next available API?

The solution came about in the form of CloudFront and Lambda@Edge functions. It is an amazing feature of CloudFront which can trigger Lambda@Edge functions in the region where the caller is located. It should be clear that if we know where the user is located, we can pick the API, inside the Lambda@Edge function, based on where the call is coming from.

Furthermore, we can also get the region of the executing Lambda@Edge function, thus, allowing us to pick the AppSync API in that same region. The first step to implement this solution was to proxy AppSync calls through CloudFront. Therefore, the calls would now be directly made to CloudFront instead of AppSync.

I then extracted the HTTP call from the CloudFront parameters inside the Lambda@Edge function. Once I had the region and the AppSync query extracted from the CloudFront parameters, I would make a new HTTP call to the corresponding AppSync API. When the data returned, I would pass it back to CloudFront through the Lambda@Edge function. The user would then get the data that was requested.

But we did not solve the Active-Active requirement just yet. The goal was now to detect when an API is unavailable and switch to a different one. I solved this problem by checking the result of the AppSync call. If it was not an HTTP 200 response, the call clearly failed.


Performing another HTTP request if the original one fails
I would then choose another region from a list of all available regions and then make a call to the next AppSync API in that region. If the call succeeds, we return the result; if it fails, we try the next region until we succeed. If the last region also fails, then we return the failed result.

This is simply the Round Robin implementation of Active-Active Highly Available architecture. With this system now in place, we have actually implemented the following three features:

Global Low Latency
Region-based Load Balancing
Active-Active High Availability
We clearly have low latency, on average, for each global user since each user will get routed to the closest region he is invoking the call to the API from. We also have region-based load balancing because users will be routed to multiple APIs in their region. Lastly, we have an Active-Active High Availability, since the system will stay functional even if some of its APIs or databases fail because users will be routed to the next available API.

It would actually not be enough to handle high availability for the APIs simply. I wanted to have it for all the resources, including the HTML and JavaScript files served from CloudFront.

I used the same approach this time but created 16 AWS S3 buckets. Each bucket would serve the same files but be located in different regions.

In this case, when the user visits our website, the browser makes multiple HTTP calls to either HTML, JS, JSON, or image files. The Lambda@Edge would, in this case, have to extract the URL currently being called. Once I have the URL, I would have to determine the file type of this file and make a new HTTP call to the corresponding S3 bucket in the region.

Needless to say, if the call succeeds, we would return the file, while if it fails, we would use the same routing system as previously, thus also providing an Active-Active Highly Available system.

With this system now in place, we have reached another milestone and placed another piece of the cornerstone for our enterprise-level infrastructure. This was by far the hardest system to develop, and it took three months to complete.

As it turns out, we had more problems to solve, and this system would prove useful again.

Dynamic PWA Manifest
PWA is an amazing web technology and will be used by more websites as time goes on, but back in 2019, things were only getting started. Since I decided to serve each community on a separate subdomain, I also wanted to give users the ability to install their branded PWA with an appropriate title and app icon as well.


We can easily install the main app with its icon and title
As it turns out, the PWA Manifest file, which defines all these features, does not work based on subdomains. It can only define one set of values based on the domain it’s served from.

The fact that I could already proxy HTTP calls using CloudFront and Lambda@Edge also came in handy here. The goal was now to proxy each call to the manifest.json file. Then, depending on which subdomain the call is coming from, to get the corresponding community data, which would be the app icon, title, etc. We would then dynamically populate the manifest.json with these values.


But now we can also install a subdomain with its icon and title
The file would then be served to the browser, and the community would then be installed as a new PWA app on the user’s device.

Moving to the Frontend
Once I had these crucial steps figured out, it was time to start working on the frontend. In line with the previous subdomain-based requirement, we also had to figure out how to load a different community and its data based on the subdomain. This would also require loading different website layouts, which would be used in each community.

For example, the homepage would need to list all the available communities, while other subdomains would need to list the articles on each of those communities.

It goes without saying that to solve this problem, we cannot simply build multiple different websites from scratch. This would not scale, so we would need to reuse as many controls and features as possible. These features would be shared between these two community types and then loaded only if required. To maximize the reusability of the code, I defined all controls as four different types:

Components
Controls
Pages
Communities
The smallest custom HTML elements like <button> and <input> were defined as Components. Then we could reuse these Components in Controls which are sets of these smaller elements. For example, the profile info Control would display the user’s profile image, username, followers, etc.

We would then again be able to reuse these elements in higher-level elements, which in our case, are — Pages. Each page would represent a route, for example, the Trending page, where we could see all the activities, or the Interest page, where the actual article text would be displayed. I would then compose each Page from these smaller Controls.

Lastly, the highest level elements would be defined in Communities based on their type. Each Community element would then define all the lower-level Pages it requires. The Aurelia Router came in handy because you can load the routes dynamically. The implementation was handled in the following way.

Regardless of the subdomain, when the website starts loading, we register the two main branches implemented as Aurelia components. These represent two different community types. I then defined two different web types or layouts:

Main
Article
The “main” type represents the website layout which will be loaded when the user lands on the main https://immersive.community page. Here, we will display all the communities with all the corresponding controls.


Preparing Page elements that will be registered for each route
On the other hand, once the user navigates to a subdomain, we would then need to load a different layout. In other words, instead of communities, we would load articles and corresponding features and routes, for example, the ability to publish and edit articles. This would enable or disable certain routes based on the community type we were located on.

Our Aurelia and WebPack setup splits the JavaScript into appropriate chunks so that routes and features that are not needed do not get loaded at all, thus improving speed and saving on bandwidth.


Asynchronously loading JavaScript using WebPack
Once we determine which subdomain we are located on, we would load the community and the user data for this specific community, thus having successfully implemented the solution.

The Masonry Layout
I reasoned that we should try to keep the design as simple as possible. So, since the users are coming to the website for the content, we will focus on displaying the content as opposed to secondary features. The articles should be displayed in lists, but they should not look stale. Thus I’ve decided that each article would consist of the following:

A cover photo
Article title
Article category
Date when the article was posted or edited
Author’s profile
The main way I made sure the list of articles wouldn’t look stale was to make sure the user could choose the aspect ratio of each cover photo for their article. The inspiration came from how Pinterest displays its pins so that each article would have a different aspect ratio. This required me to implement the masonry layout, which can’t be chosen out-of-the-box in either CSS Grid or FlexBox.


The Masonry layout for articles
Luckily, there are several useful open source implementations that I tried out and used for the layout. I had to add several improvements, like loading paginated data and scaling with the screen size.

And then…

In November of 2019, the first signs of COVID-19 started to appear. The world was soon thrown into turmoil, and nobody had a clue what was going on, but it would change the world and how we interacted with each other in ways nobody could imagine.


COVID-19 breaks out in late 2019
Soon after, we would start working from home. This would greatly impact my development process since I could no longer travel to work. Ironically, the world came crashing down while I got the break I needed!

Interests and Reviews
Back in the development world, the idea behind writing articles on Immersive Communities was based on collaboration. To this end, I went with Wikipedia as a basis for the collaborative effort. Also, community websites like Amino Apps and Fandom.com and blogging website HubPages.com played their role as well.

Writing blog posts as a single person can be a good start, but we can go beyond that by having people write articles together. Once we add hyperlinks to the text and connect these articles written by different people, we basically create a community where people come together to engage in topics they are interested in.

I’ve decided to define two types of articles, namely,

Interests
Reviews
Interests would be short articles, approx. 5,000 character-long, and they would factually describe any particular interest a person might have. Then, each person could write a review with a rating of this particular interest. The main interest page would then reference all the reviews written for this particular interest. The main difference would be that anyone can edit Interests, but only the person who authored a Review could edit it, thus adding a personal touch to each article.

Here, our earlier decision to go with CloudFront to proxy AppSync calls came back to bite us. It turns out that CloudFront only supports query string lengths up to 8,192 bytes. Thus, we cannot save data that is longer than that.

Regarding each article, each interest could be liked and commented on. Thus, the users could come together and discuss how each article will be written and edited. Furthermore, each Interest could be added to the user’s profile page for quick access.

Once all these features were in place, the end of the year came. The situation looked good, and I was certain the project would be completed next year. This assumption did not turn out to be accurate, to say the least.

2020 — Full Speed Ahead
The year, more or less, started off well. The economy still held up somewhat but started to go down after a while. The markets started responding to the pandemic, and the prices started rising. Early 2020 was when I put in a lot of work but didn’t have a truly working product. There was still a lot left to be done, but I was confident in the outcome, so I continued to push forward.

At my day job, the work hours extended as well, and we had to reach our deadlines faster than usual. I had to reorganize my schedule, and the only way to save some more time would be to sleep for only four hours each night.


Waiting for a train in Tokyo Metro
The idea was to come home by 6 or 7 p.m. and then go straight to work on the project. I could then work until 3 or 4 a.m. and then go to sleep. I would then have to wake up around 7 a.m. and quickly get to my day job. This would, of course, not be enough sleep each night, but I figured I would make up for that time by sleeping for 12 hours during the weekends. I’d also scheduled all vacation days and public holidays for work as well.

The new system was set up, and I proceeded as planned.

The Markdown Editor
It goes without saying that an article-writing website should have an easy-to-use text editor. During early 2020, Markdown emerged as a very popular way to write text. I decided that Immersive Communities would have to support it out of the box.

This would not only require me to write the Markdown but then display it as HTML as well. The Markdown-It library would be used to transform Markdown into HTML. But there were additional requirements, so the complete list of different media we should display is as follows:

Text
Image
Video
Embeds
Furthermore, images and videos should be displayed as a slider where users could swipe images like on Instagram. This would require a mix of Markdown and other HTML elements. The editor would be split into several parts with two types of inputs, the text field, and the media field. Each field in the editor can be moved up or down, which was quite easy to implement using Sortable.js.

When it comes to input fields, the Markdown field was simple enough to create with a <textarea> element. The editor also loads the Inconsolata Google Font, which gives the text typed the typewriter look.


Markdown editor with media input elements
Furthermore, to actually style the text, a bar was implemented, which would add Markdown to the text. The same was done using keyboard shortcuts using Mousetrap.js. Now we can easily add bold text in the form of ** Markdown tags using Control+B, etc. While typing, it's only natural to have the <textarea> element expand as the number of text increases, so I used the Autosize.js library to implement this feature.

The media field would be able to display either images, video, or iframes containing embedded websites. The type of media field would switch based on the media itself. I used Swiper.js to implement the swiping between images. The video component was implemented using the Video.js library.

The issues started arising when it came time to actually upload the media. Regarding images, it was easy to use the browser’s File API to load photos and videos from your device. What I then had to do, was to first transform images, which might have been in HEIC format, into JPEG. Then I would compress them before uploading them to the backend. Luckily, Heic-Convert and Browser-Image-Compression libraries served this purpose well.

Another issue occurred when I had to choose the correct image aspect ratio and crop it before uploading. This was implemented using Cropper.JS but, unfortunately, didn’t work out of the box on the Safari browser. I spent quite a lot of time setting the appropriate CSS for the image to not overflow from the container. In the end, the user can easily load an image from their device, zoom in and out, and crop it before uploading.

Once everything was completed, the media would be uploaded to Cloudinary, a service for managing media files.

It was then time to put all of this together and display it to the user in the form of articles. I was fortunate enough that Aurelia has a <compose> element that can load HTML dynamically. Therefore, depending on the input type, I would load either media elements or Markdown elements, which would be transformed into HTML.

This HTML would have to be styled with CSS, especially the HTML tables, which I would transform depending on the screen size. On larger screens, tables would be shown in their regular horizontal layout, while on smaller screens, they would be shown in a vertical layout.

This would require an event-driven approach that would tell us when and how the screen size changes. The best library to use in this case was RxJs, which handled the “resize” events, and I could format the table accordingly.

Improving the Data Input
I then came back to the articles. I had to change the way articles were being saved to the database since it was the case that multiple people could be modifying the article at the same time.

I would then save the new article as an initial article type, but the actual data of each article would be saved as a version. I would then be able to track which user and when each article was changed. This prevented me from saving a new version if the user didn’t load the latest version first. Also, if a certain update was inappropriate, it could be disabled, and a previous version would then be visible again. Drafts for each article would be saved in the same way.

As far as actual data input goes, I decided to implement it as a pop-up. The pop-ups would not simply appear on the screen but would slide up from the bottom. Furthermore, it would be possible to swipe inside the pop-up. For this purpose, I reused the Swiper.Js library, while all the other animations were done using the Animate.CSS library.


Pop-up element presents several features
The pop-up was not simple to implement because it required scaling with the screen size. Thus, on larger screens, it would take 50% of the screen width, while on smaller screens, it would take 100% of the width.

Furthermore, in certain cases, like with the list of followers, I implemented the scroll to be contained within the pop-up. This means that the list which we were scrolling did not stop at the top but would disappear when scrolling. I added further styling, dimmed the background, and disabled scrolling or clicking outside the pop-up. On the other hand, the Preview pop-up for the article editing system moves with the screen.

This was inspired by Apple’s Shortcuts app and how its pop-ups appear, which also goes for the pill buttons and titles above the elements.

The Navigation Bar
One of the most important UI features I implemented was further inspired by the iPhone: its navigation bar. I’ve noticed that almost all mobile apps have a fairly basic navigation bar, with simple and small icons which don’t really fit into the overall design of the application.

I’ve decided to replicate the iOS bar and use it throughout the website. It should not always be visible but disappear when we scroll down and appear when we scroll up. When the user is scrolling down, we assume they are interested in the content and will not navigate away from the current page. Thus, we can hide the bar. On the other hand, if the user is scrolling up, they might be looking for a way to leave the page, so we might as well show the bar again.

Four buttons on the bar allow the user to navigate to the four main parts of the website. The Home button navigates to the homepage of each community. The Trending button navigates to the Trending page, where the user can see all the recent activities other users have posted. The next button is the Engage button which navigates to the list of all the features and settings the community offers. Lastly, the Profile button leads us to our profile page.

It was also necessary to consider larger screens, so the bar moves to the right side of the screen when displayed on a large screen. It becomes sticky and does not move anywhere at that point.

Real-Time Batch Processing
Once the most important work on the frontend was done, it was time to visit the backend again. This part of the system would prove to be one of the most complex to implement but, ultimately, very important and would also make it quite easy to proceed with other features.

In Object Oriented Programming, there exists a concept of Separation of Concerns, where we keep our functions simple and make them do only one thing, which they are meant to do.

Furthermore, the idea of Aspect Oriented Programming is specifically about the separation of concerns, where we need to separate business logic from other cross-cutting concerns. For example, saving a user to a database should naturally be accompanied by logging while the saving of the user is being processed. But the code for these two features should be kept separate.

I’ve decided to apply this reasoning across the board and extract as many features from the UI, which are not important to the user and move them to the backend. In our case, we are mostly concerned with saving data to the database, which relates to communities, articles, comments, likes, and so on.

If we want to track how many likes an article gets, we could have a process that counts all the likes for each article and updates them periodically. Since we are here dealing with a large amount of data stored in the database and potentially a large amount of data constantly flowing into the database, we will need to employ real-time data processing to handle this situation.


Real-time aggregation of new or deleted items for each community using AWS Kinesis
I have chosen AWS Kinesis for this task. Kinesis can ingest large amounts of real-time data, and we can write SQL queries to query and batch this data in near real-time as well. By default, Kinesis will batch data for either 60 seconds, or the batch reaches 5 MB, whichever comes first.

Thus in our case, we will query the incoming data, meaning, creation of new communities, addition or deletion of articles, users, activities, etc., and update the database every minute with fresh data. The question now arises is how do we get the data into Kinesis in the first place?

Our database of choice, DynamoDB, can define invoked triggers in the form of Lambda functions whenever the data is either added, removed or modified. We would then catch this data and send it to Kinesis for processing.

It just so happens that one of our earlier decisions would make this process slightly harder to implement because we are not dealing with one database but ten databases. Therefore, once the data is added, the Lambda functions will be invoked ten times instead of once. Yet, we need to handle each case because the data could come from any database since they are located in different regions.

I solved this problem by filtering out copied data as opposed to the original data that the user added to the database. The “aws:rep:updateregion” column gives us this information. We can determine if we are dealing with the data in the region where it was inserted or if it represents copied data.

Once this problem was out of the way, we would filter either the addition of new data or its removal. Furthermore, we would filter the data based on its type, meaning we are dealing with data representing a community, article, comment, etc. We then collect this data, mark it as either “INSERT” or “DELETE,” and pass it on to Kinesis. These ideas from the Domain-Driven Design approach are called Domain Events and allow us to determine which action happened and update our database accordingly.


Real-time batch data processing with AWS Kinesis
We then turn our attention to Kinesis. Here we had to define three main parts of the system

AWS Kinesis Data Streams
AWS Kinesis Firehose
AWS Kinesis Data Analytics
The Kinesis Streams allow us to ingest data in real-time in large amounts. The Kinesis Analytics system allows us to query this data in batches and aggregate it based on a rolling time window. Once the data is aggregated, we would push each result further into Kinesis Firehose, which can handle large amounts of data and store it in a destination service, which in our case is an S3 bucket in the JSON format.

Once the data reaches the S3 bucket, we trigger another Lambda function and handle this data to update the DynamoDB database. For example, if five people liked an Interest in the last minute, we would find this data in our JSON file. We would then update the like count for this Interest and either increment or decrement the like count. In this case, we would increment it for five likes.

Using this system, the statistics of every community would stay up to date within a minute.

Furthermore, we would not need to write and execute complex queries when we need to display aggregate data since the exact result is stored in the fast DynamoDB database in each record, thus increasing the query speed for each record. This improvement is based on the idea of data locality

Cloudinary
It was now time to start implementing third-party services that would handle the features I needed. I found buying a subscription was easier than building my own. The first service I implemented was Cloudinary, a media management service. I’ve set up all the presets on Cloudinary to transform images for the following responsive screen breakpoints eagerly.

576 px
768 px
992 px
1200 px
These would also be breakpoints set in Tailwind CSS, where our website would conform to different screen sizes for mobile phones, small tablets, large tablets, and computer monitors. Then depending on the current screen size, we would appropriately invoke eagerly created images from Cloudinary using the scrcset attribute on the <image> element.

This would help us save bandwidth and shorten the time to load images on mobile devices.

As far as the video feature goes, after it had been implemented, I decided to drop it because the pricing for the videos at Cloudinary was too expensive. So, even though the code is there, the feature is currently not used but might become available later. This will require me to build a custom system on AWS in the future.

Embed.ly
I decided to use Embed.ly to embed content from popular websites such as Twitter, YouTube, etc. Unfortunately, this did not work without issues. Hence, I had to use several techniques to manually remove Facebook and Twitter scripts from the website because they would interfere with the embedded content after it gets loaded multiple times.

Algolia
Regarding search, I chose Algolia and implemented the search for communities, activities, articles, and users. The frontend implementation was simple enough.

I created a search bar which, when clicked, would hide the rest of the application and, while we’re typing, would display the result for the specific subdomain we are currently browsing. Once we press “Enter,” the masonry on the home page displays the articles which fit the query. I also had to implement the pagination, which would load the results incrementally to mimic the look and feel of Pinterest.

The problem came in when I realized there was no way to search the activities unless you stored the whole text in Algolia, which I wanted to avoid. I, therefore, decided to store only relevant tags for each activity, but the question was how to extract relevant tags from each activity.

The answer came in the form of AWS Translate and AWS Comprehend. Since the number of items that would be added to the database would be large and we would like to add this data to Algolia, we might overload the API if we were to add each record separately. We would instead like to handle them in real-time and in batches. Therefore, we would again employ Kinesis as a solution.


In this case, each addition of a new item to the database would trigger a Lambda function which would send that data to Kinesis Data Streams, which would, in turn, send the data to Kinesis Firehose (no need for Analytics this time) and further store them in an S3 bucket.

Once the data is safely stored, we would trigger a Lambda function to send it to Algolia, but before that, we would need to process this data. In particular, we would need to process activities, from which we would strip out Markdown text using the markdown-remover library. We would then be left with plaintext. Once we have the actual text, we can proceed with extracting the relevant tags which will be used for the search.

This can be easily done using the AWS Comprehend service, but the problem is that it supports only some languages. Thus, if a user is writing in a language that is not supported, we would not be able to extract the tags. In this case, we use AWS Translate and translate the text to English. Then we proceed to extract the tags, and then we translate them back to the original language.

Now, we store the tags in Algolia as intended.

Recombee
One of the most important features Pinterest has is its recommendation engine. Once the user clicks on a Pin, they are immediately shown the full-size image of the Pin, while under the image, we can see the recommendations the user might like based on the current Pin.

This is a very good way to increase user retention and keep them browsing the website. To implement this feature, which in my case would have to show similar articles to users, I chose Recombee — a recommendation engine SaaS.

The implementation was easier this time as opposed to Algolia since I reused the same principles. Seeing as how we will need to recommend communities, articles, and activities for each new item that a user creates, I would use Kinesis to batch these items and send them to Recombee.

The recommendation process is based on Views, meaning every time a user sees an article, we would send this View for this specific user and the article to Recombee.

We can also assign other actions to the items in Recombee based on how the user interacts with them. For example, writing a new Interest would be mapped to a Cart Addition for that Interest. If a user likes an Interest, this would add to the Rating. If a user joins a community, this would be mapped to the Bookmark for this community.

Based on this data, Recombee would create recommendations for users.

On the frontend, I would get the article the user is currently reading and the recommendation data for this specific article and the user. This would be displayed at the bottom of each article as a paginated masonry list. This would give the user a list of potential articles they might be interested in reading.

Locize
Seeing how the website would aim for a global audience from the start, I also had to implement localization. For the initial release, I decided to go with ten languages and settled for a SaaS service — Locize — which is implemented based on the i18next localization framework.

We will need to localize words based on the amount, meaning either singular or plural, and would have to localize time. We display the time when each article was created or last updated.


${‘recommend’ & t} can be used to localize elements
I’ve chosen English as the default language and translated all the words using Google Translate into other languages like German, Japanese, etc. It is, again, very convenient that Aurelia supports localization as well. Once all the translations were done, I imported the translated JSON files into the application and had them split based on the community type so that we don’t load unnecessary text that won’t be used.

Aurelia then allows us to use templates and binding that automatically translate the text. But I also used Value Converters, which would format the time to show how long it has been since an article was written instead of showing an actual date. Furthermore, I had to format the numbers as well; thus, instead of showing the number 1000, I would display 1K. All these features were handled by libraries such as Numbro and TimeAgo.

Twilio
A community website requires communication, but not just in public. It requires private communication as well. This meant that a real-time private chat should also be something that I need to offer. This feature was implemented using Twilio Programmable Chat service.

Every user can have a private chat with any other user in each community. The backend implementation was easy enough to implement using Twilio libraries. Regarding the frontend, I decided to style the chat based on Instagram because it had a clean and simple design.

Prerendering the SPA
I’ve also chosen a service called Prerender to prerender the website to make it available to search engine crawlers. After realizing the pricing might be a concern, I decided to build the prerendering system on my own. To this end, I found a library called Puppeteer, which is a Headless Chrome API.

This library could be used to load websites programmatically and return a generated HTML with executed JavaScript, which the search crawlers at that time didn’t do. The implementation would load Puppeteer in a Lambda function, which would load a website, render it and return the HTML.

I would use Lambda@Edge to detect when my user was a crawler and then pass it on to the pre-rendering Lambda. This was simple enough to do by detecting the “user-agent” attribute in the CloudFront parameters. It turned out that Lambda couldn’t load the Puppeteer library because it was too large.

This was not a show-stopper since I then found the chrome-aws-lambda library. It did all of this work out of the box and would be much smaller since it uses only the Puppeteer core, which was needed for my purposes. Once the system was completed, the search engines were already powerful enough and started executing JavaScript as well. Thus, even though I completed this feature, I turned it off, allowing search engines to crawl my website on their own.

Stripe
One of the core features of Immersive Communities is its Revenue Sharing scheme, where the users share 50% of member subscriptions and ad revenue. As stated previously, we need to enable our creators to not just create their content but also monetize it. The question was now how to implement this system. The default choice was Stripe, so I proceeded as follows.

I’ve decided to design the Revenue Sharing system based on each community. This way, a user can create several communities and earn based on each community. The revenue for each community would come from two sources.

Member Subscriptions
Self-Service Ads
Member subscriptions were the easiest to implement. I would create three price points for member subscriptions — $5, $10, and $15 monthly. The members of each community can then support the owner of the community every month and, in return, would not be shown any ads.


A member can support each community with monthly subscriptions
The ad system was based on the same monthly subscriptions but would range between $100 and $1000. The company which wants to advertise in a particular community can choose the monthly payment amount and set the ad banner.

Assuming several advertisers in a single community, the ads would be chosen randomly with every page load or route change. The way the advertiser can increase the frequency of showing their ads, compared to other advertisers, is by increasing the monthly payment amount.


A company can advertise its brand in each community with monthly payments
We would also need to show the advertiser how their ads perform, so I again employed a Kinesis setup to measure both views and clicks. This system would then update the statistics as usual, and I then used the Brite Charts library to display the statistics.

The most important part was the actual revenue-sharing feature. This was implemented by the Stripe Connect feature. The user needs to add their bank account and connect to Stripe Express, and the system would then have all the info needed to send payments.


Stripe-based Revenue Sharing System
I would then have a scheduled Lambda system that would get all the users daily, update transactions, and make sure that 50% of each transaction (either member subscription or ad payment) is transferred to the community’s owner, where the payment is made.

AWS Cognito
The last service that had to be implemented was Auth0, which would help with user authentication. After some research, I decided on a passwordless setup based on SMS messages. Seeing how we are now in a mobile-first world, it made only sense to forgo passwords and base the authentication on something everyone already has — their mobile phone.

It turned out that the Auth0 implementation of passwordless authentication was sub-optimal since it would redirect to their website every time and would be based on URL parameters, which I wanted to avoid. The pricing also wouldn’t scale for a social network, so I built my own implementation using AWS Cognito.

It was quite convenient that Cognito has triggers that can be connected to Lambda functions, which I used to trigger authentication. The Lambda functions would be used to collect user data during signup. At this point, the user only needs to provide their phone number and username to register.


Passwordless login process
During the login procedure, the Lambda function would collect the user’s phone number and send an SMS message containing a verification code to the user using AWS SNS. The user would then type in this code to get verified through Cognito and would be redirected to his profile page.

Of course, once the user gets authorized and the validation data is passed back to the frontend, we would have to encrypt it before storing it. The same authorization data gets encrypted before it gets stored on the backend.

Also, we store the user’s IP during each signup and login.

It would later turn out that users would have an issue with giving out their mobile phone numbers, so I decided to replace the SMS with email messages. There was a problem with duplicated messages when I wanted to use AWS SES, so I switched to Twilio’s SendGrid to send emails to users.

With this system completed, the year was out, and the project I started two years ago was nowhere near complete. There was no other choice but to continue working and trying to complete it as soon as possible. Little did I know that the biggest challenges were yet to come.

2021 — No End in Sight
Here is when everything had to fall into place, but working as a solo developer without any feedback for this long makes you question the direction the project is going.

The question that any developer who is currently in the same place right now might ask themselves is:

How can I keep myself motivated and able to keep going even though I see no end in sight?

The answer is quite simple.

You shouldn’t question your decisions, regardless of how you currently feel about the project. You can’t allow your current emotional state to determine how you will act. You might not feel like continuing right now, but you might feel like it later, and you sure as hell will feel bad if you do quit.

So if you do quit, you will not have the project anymore, and all the work will have been for nothing. The only thing to do is to keep going forward regardless of what happens. The only thing to remember is that every delivered feature, every single keyboard press, is getting you closer to the goal.


Just trying to get by…
During this project, I changed my job three times, each time being quite involved, but even though I had to go for job interviews, I would still go back home, sit behind my desk, and continue to work on my project.

What you have to ask yourself if you are lacking motivation is the following:

If you quit now, where will you go? The only way you can go, after quitting, is back to where you came from. But you already know what’s back there. You already know what its like, and you did not like it, which is why you set out on this journey in the first place.

So, you now know for a fact, that there is nowhere to go back to. The only way you can go, is forward. And the only way to go forward, is to just keep working.

This is all the motivation I had available during this project. As I said already, it was either that or going back to where I already was, so I decided to keep moving forward.

The Admin System
It was now time to start bringing things together and to start. I decided to implement the Admin System, which would be used to maintain each community. Each community owner could make decisions about removing content from their community. This would imply that we can disable ads, articles, activities, and ban users if their actions are not in line with the rules of conduct.

The owner of each community is also able to give admin rights to other users as well. But we also need to make it possible for the admins on the main community to be able to administrate all other communities. Furthermore, these admins could completely disable other users from all communities and even disable the community.

To make it easier for admins to do their job, I introduced the flagging system, where each item can be reported to the admins. The users can now report anything on the website that they deem to be inappropriate.

The validation of permissions for each user would be decided on the backend. I would create a Lambda function that would be invoked inside each AppSync call to validate each request.

Furthermore, the frontend would use routing-based authorization, which Aurelia provides. I would define rules that allow or disallow the current user from proceeding to a certain route.

For example, you would not be able to see your profile if you have been banned from a certain community. But this system could also prevent someone from navigating to a profile page if they are not logged in. Instead, they would be redirected to the login page.

The Analytics Dashboard
Another feature that would be useful for the users would be the Analytics Dashboard page. Each community owner can see charts showing exactly how much interaction is happening in their community. For this particular case, I would reuse the data aggregated by Kinesis and display it with charts using the Brite Charts library.


The owner of each community can access the community statistics page
Furthermore, I would also take the Stripe data and display the number of subscribers, advertisers, and total earnings this community has.

The only problem which had to be solved was the responsive design, meaning how to display charts on both small and large screens. Again, I used RxJs to detect the “resize” event and apply styling based on the screen breakpoints defined in Tailwind CSS.

The Security
An additional level of security was also on the roadmap, and I decided to implement a WAF in front of my CloudFront distributions. I used the AWS Marketplace and subscribed to the Imperva WAF system, which would proxy my traffic and make sure to allow only the traffic validated as safe.

The solution was quite easy to implement, but the bill was way too much to handle once the first month was out. I disconnected the system and decided to rely on what CloudFront had to offer by default.

The Last-Minute Redesign
At this point, I had to start looking at all that I had done and fixing the small issues that were still left. Many things still needed to be polished, but the largest thing that had to be changed was the DynamoDB database setup.

It turns out my initial setup, which wasn’t the one I’m using now, was not going to scale well. This is why I decided to completely redesign it and start using the “#” separator to indicate branching in the record’s identifier.

Previously I was making separate records and using AppSync Pipelines to locate each related record, which was unsustainable. This also affected the Kinesis and third-party services setup like Algolia and Recombee.

It took three months to redesign the system to work properly and completely. Once this was done, I could continue with the new features again.

The Hottest Summer on Record
Summers in Tokyo are hot and humid. It is quite a challenge to stay on point with anything you’re doing, especially in July and August. During that time, the Olympics were being held in Tokyo, and on August 7th, it was reported that the hottest temperature was recorded in the history of the Olympics.


Record-breaking heat levels recorder in Tokyo
Going to work by train would not make sense anymore because the weather would be too exhausting, leaving me drained and unable to work in the evening. I realized that I had to save some more time by taking a taxi to work instead. This gave me more time to sleep and would keep me from being too tired to work once I got back home.

Real-Time Notifications
PWA is a great technology that offers us a way to send notifications to users using Push Notifications. I decided that this would be a system that would also be needed and proceeded with the implementation.

The notification system would be implemented based on the user being followed. If you are following a user, you would need to be notified when they create a new activity or article.

Currently, the only issue with the Push Notifications is that at the time of this writing, they are still not supported by the Safari browser on iOS devices. Instead of native Push Notifications, I’ve decided on the browser’s Notification API. On the backend, I would create a new instance of AWS API Gateway and set it up to work with real-time data.


The Real-time Notification System
On the frontend, I would make a connection using WebSocket API to the API Gateway. Once the user being followed publishes a new article, this data will be sent to Kinesis. Again, using batch processing, we get all the users who follow the author and then use the API Gateway to send the notifications to the frontend. On the frontend, the WebSocket connection gets triggered, which we use to invoke the browser’s Notification API and display the notification.

Furthermore, when it comes to comments that the users can write on each article, we need to keep track and show the user where they are currently engaged in discussions. I also implemented an unread indicator that would show which comment section has new comments the user has still not read.

This would be checked when the user loads the application without using the await keyword when invoking the AppSync call. This would ensure that the execution does not wait for the call to be completed; instead, the more important data gets loaded first.

Once the call would return, we would update the UI and show the notification to the user.

I would also use notifications in the form of pop-ups to signal to the user when an action was completed successfully or not. For example, I would create a pop-up message telling the user if the article update has failed.

Frontend Validation
Seeing how the backend validation was completed, we had to give the user an even better experience by implementing the validation on the frontend to give the user faster feedback.


Fluent validation with Aurelia
Thankfully, Aurelia has a validation plug-in and is appropriately implemented with a fluid interface. This made it quite easy to create business rules which would limit, for example, the number of characters the user could type into an <input> field for an article name.

I would use the Aurelia property binding system to collect and display the validation messages on the UI. I would need to incorporate this with the localization system and ensure the messages are displayed in the correct language.

Finalizing the Work
The rest of the year consisted of working on smaller details. It required me to create things like loading placeholders. I specifically decided that I did not want to display loading placeholders as separate screen elements.

Instead, I wanted to indicate to the user that an element is being loaded. That is why I used the outline of the element which was being loaded and gave them a transparent loading animation instead. This was inspired by the Netflix mobile app, which works similarly.

By this point, the end of the year came, and I was now working on the main home page. This page would only display all the communities which we currently have. Luckily, the component-based system I created made it easy to reuse most of the code I wrote, so the task was completed quickly.

The year finally ended, and I was satisfied with the work. Even though the project was not yet done, I knew success was within my reach.

2022 — The Last Mile
This year was to be the final year. I did not know whether I would implement everything I wanted to, but I knew I had to do it regardless of what happened. I did not want a repeat of the work during summer like I did last year because it was more probable that it would be even hotter than the last year.

My prediction came true, and it turned out that Tokyo had the hottest summer temperature in 2022, measured in the last 147 years!

The Landing Page Design
I started by designing the landing page. The question was the following:

How do I want my users to feel when they visit my landing page?

I didn’t want the users to feel like this would be too serious of a website, but rather a friendly and collaborative community.

I noticed that, lately, landing pages had illustrations instead of photographs of real people, so it would make sense to go down this path. That’s why I decided on a set of illustrations I bought on Adobe Stock.

The landing page had to be simple and would also have to describe everything the website is offering quickly. This had to be localized, so I used the localization feature to translate all the landing page titles and subtitles on display.


A simple and clear landing page
The only technical issue that had to be overcome was introducing color inside the text. Luckily, I could use the styling feature inside the translation definitions and then use Markdown to dynamically generate the HTML, which would be displayed on the landing page.

Required data, like “Privacy Policy” and “Terms of Use,” were purchased online and translated into multiple languages using Google Translate.

Expect the Unexpected
It was now time to tie up all the loose ends, so I spent the rest of the time making sure logging was present in all the Lambda functions on the backend. This would help me ensure that if issues were to happen, I would know what was happening.

By the time I was finishing up, the war in Ukraine had begun. This again increased the uncertainty of the global economy, but I continued to work and kept myself focused on the final goal.

Having not kept the PWA implementation up to date, I had to ensure that all the features were working, so further development was needed to improve JavaScript and image caching. The offline feature was finally turned on, and the application was now properly behaving as an offline app.

I also had to move the changes I made on the backend and spread the changes I made on AppSync to other regions. Since it would be too cumbersome to have done that during development, I made no changes to other regions since I started developing.

The same goes for the environments. It would have wasted too much time to build all three environments constantly, so I finally synced them and moved the code to UAT and Production.

Lastly, I had to implement the https://immersive.community domain, which would have to work without the “www” subdomain and redirect to the homepage correctly.


The End, … or is it?
At this point, we were in the early morning hours of the 25th of April 2022. My four-year-long project was finally over. I created the first post on the website and went to sleep. I knew I finally succeeded. Not only did I finish what I set out to do, but I also did it before the summer came.

Final Words
Ironically, the final words of my adventure are — this is not the end but just the beginning. Now that the system is live, the content that needs to be created and the promotion and advertising needed for brand awareness will be a completely new adventure.

But what have I actually learned from this exercise?

Well, quite a lot. First of all, I can confidently say I would never do it again. Not that I’m not pleased with the outcome, quite the opposite, I’m very satisfied, but this is the kind of thing you do once in a lifetime, and it wouldn’t make sense to try to outdo yourself to prove you can do it even better.

I wanted to know whether it was possible to build an enterprise-level system as a solo developer, and I have shown that it can be done with the tech stacks we have at our disposal. More than anything, this is a statement to every developer working on their side project or thinking of starting one.

Would I recommend this approach to other developers out there? Absolutely. Not because it’s an optimal way of doing things; it most certainly isn’t. Not asking for help when you’re stuck is certainly not the fastest way to solve a problem, but it will help you discover your limits. Once you’ve decided to do something like this and succeed, you will know that everything else you decided to do after that will be easier to achieve.

I believe my story will motivate you to finish whatever you started regardless of how you feel, and even if you don’t see the end of the road you are now walking down, remember that “back there” is not where you want to be.

If you found this story inspiring, subscribe to my YouTube channel because I will start doing an advanced “Full Stack Dev” programming course where I will detail all the tech I used to build Immersive Communities.

What I didn’t touch upon in this article are the philosophical underpinnings, justifications for how I approached each problem, and the techniques I used to analyze and design the solutions to each problem. This was an even more important component than simply knowing the technologies and how to use them. How you approach a problem — and the thought process that brings you to the solution — is something I will go in-depth in my YouTube videos.

This will be a great way for developers to learn programming from someone who created a real-world system and is ready to share his knowledge.

See you on YouTube too! Thanks for reading.


Tell me:
* How many member subscription tiers are there?
* How much is each tier?
* When did he first start planning?
* Who said 'Content is King" and when? According to the text provided
* Did he have familiarity with dynamically typed languages before starting the project?