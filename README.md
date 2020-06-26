# Albion Market Tools
Various tools for making silver!

# Developer TODOs
* Turns out fetching every iteration of item could take as long as an hour... probably need to rethink the strategy behind expiring cache values. Initial data seed is probably best, followed by a cache item update if last update was > 1 hour ago.
* Adjust black market calculator to use cache data instead of API.
* Adjust enchanting calculator to use cache data instead of API.

# Future Features
* Farming calculator (?)
* Optimized Time of Day Calculator (?) {This would involve tracking historical prices. Too much data to cache me thinks, so this would probably be on request.}