# Food Truck Finder

This is a side project where I'm building out a site to host food trucks, their companies and assorted information. Below, I'll outline much of the architecture and thinking behind this project.  

### Rationale:

My fiance and I love to find good food trucks but it's not always easy. We're rather spontaneous, so we seldom know exactly where we're going to be until we get there. But there is no polished online resource to find food trucks - especially with a recognition that they have wheels and can be across town at any given point.  

This project hopes to provide a framework that acknowledges this and accommodates it. Further, many food trucks operate on a small budget - this solution should scale from the smallest food truck to a thriving enterprise of trucks in differing markets.  

### Architecture

This is partly detailed for my own benefit, but knowing that this may prove useful to demonstrate the full thought, I'm including the details below.  

Some tables may be shifted into a different database because they are less dynamic.  

Materialized views are intended for key, stable values lookups.  

##### Company

This may not actually be a corp or LLC, but every food truck has at least one managing entity that controls it and should be able to control its data.  

One company may have a relationship with another - one as an owner, another as an operator or franchisee. The model will reflect this reality, but will not require it. This would allow both groups to control items such as food truck locations and other marketing material.  

##### Menu

Within a company menu groups will be created and within a group, the menu items will be detailed. Images will be uploaded, names provided, as well as descriptions. Support will also exist for flair such as heart-healthy, gluten free, heart-attack, etc. All of this will display in a responsive webpage that scales to duplicate mobile app feel at small scales and traditional webpage formats at larger scales.  

##### Food Trucks

These will be set up by either an owning or operating company. The created menu items will be added to the truck and have their price set at this point. Because menu items could be used in multiple markets, this is an important aspect of making this scale quickly. Default prices will be available at the time of the menu creation, so this should be frictionless to the user. Available when they want it, but not forced beforehand.  

While some places in this world operate with multiple currencies, it's not my intention to support this as a feature. I could revisit this in the future, but I doubt the use of the feature would justify the costs of more 'expensive' queries.

Food trucks will have a number of features such as calendar events (with location), a full webpage, ability to track marketing events and target followers for messages based on their settings.  

##### Localization

Within all of the preceeding is localization plan so that, when a company chooses, they can display their offerings in the primary language of the browser in use. As an example, in Montreal, both French and English would be wise. In LA, a number of languages could be wise depending upon the market and the fare. This will accommodate that as long as they create the entries (e.g. Menu listing with English, Spanish and Korean descriptions).  

##### Users

This will follow along very traditional paths, but with some value add. Users can favorite a truck, write reviews, and have a somewhat specific subscription model - again, only if they want to customize it. An example use case here is receiving updates differently on workdays vs non-workdays.  

Intially I'd hope to do this with text messaging, but in a fanciful world where this became a business model, developing small apps for mobile could make sense.  

##### Future development

I have some specific thoughts that I think could really help with adoption and use, but I will refrain from listing them at the moment.  

This project is currently being worked for fun. In the (rare) chance I try to monetize this, those ideas could prove central to viability.  

### In Development

Currently I've created the basest of tables and I already need to make modifications. At the moment I've turned my focus to the full user experience in the hopes that I can create a much more comprehensive idea of what tables are needed, why, and how they'll relate to each other.  

As such, my attention is towards a soft focus on the front end. Not with an intention to get it 'right' yet, but with an intention to use the framing out as an opportunity to realize opportunities or needs and document those.  

I have not wired (Javascripted) any of the framing. I want the back end to be mature and then I'll build sample data using developed admin pages. From there the testing will radiate out towards all aspects of the user experience - food truck customers as well as their owning/operating companies.  