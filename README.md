TEAM LFS - BUSINESS PACKAGING PROGRAM

+++ What is this the Buisness Packaging Program? +++

This program is a terminal ran business packaging and shipment tracking system program.
This program allows users to create businesses, users under businesses,
register packages, calculate shipping ammounts, and view a report of shipped packages.

+++ WHAT THE PROGRAM CAN DO +++

Business Management

- Create a business profile
- Choose a business location from available cities
- Optionally enter a custom business location with latitude/longitude
- List all stored businesses
- Select an active business
- Log out / clear the active business
- Manage a selected business by:
  - adding sections
  - adding employee IDs
  - assigning package IDs to sections
  - moving packages between sections
  - viewing sections

User Management

- Create a user profile under the active business
- Store basic information such as:
  - first name
  - last name
  - billing info
  - email
  - phone number
- List users for the active business only
- Select an active user
- Clear the active user

Package Management

- View all packages for the active business
- View all packages for the active user
- Register a new package
- Calculate a shipping quote using distance and weight
- Save package data for later use
- View a financial report for the selected business and user

+++ HOW TO RUN THE MAIN PROGRAM +++

Open a terminal in root folder and run: python3 -m source.tracker_app

If that does not work try: PYTHONPATH=. python3 -m source.tracker_app

+++ USING THE PROGRAM +++

When the program starts, a new user should in order...

1: Go to Business Management and create a business

2: Select that business as the active business

3: Go to User Management and create a user under that business

4: Select that user as the active user.

5: Go to Package Management and register packages.

6: Use Financial Report or Logistics Tools if needed.
