# Train Booking CLI Application

## Overview

The Train Booking CLI Application is a command-line interface (CLI) tool that simplifies the process of booking train tickets, managing schedules, and providing an efficient way for customers to interact with the train booking system.

## How It Works

### 1. Booking Tickets

- Users can book train tickets using the application.
- Two ticket types are available: "Early Bird" and "Normal."
- Early Bird tickets are sold at a discounted rate from 6 AM to 8 AM.

### 2. Listing Available Trains

- Users can view a list of all available trains, including their names and departure times.

### 3. Listing Train Schedules

- Users can access train schedules to see departure routes and times.

### 4. Updating Booking Details

- Customers can update their booking details, including changing the ticket type (Early Bird to Normal or vice versa).

### 5. Searching for Tickets

- Users can search for available tickets for a specific train.
- The application displays the number of available Early Bird and Normal tickets for the selected train.

## Usage

1. Clone this repository to your local machine.

2. Navigate to the project directory.

3. Run the following command to create the SQLite database:
   ```bash
   sqlite3 train_booking.db < schema.sql
