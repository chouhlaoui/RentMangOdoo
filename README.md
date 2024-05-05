# Car Rental Management Module for Odoo

## Overview


This repository contains a custom module developed for Odoo, aimed at facilitating the management of car rental businesses. The module provides functionalities to manage reservations, clients, and cars within a centralized interface, enhancing operational efficiency and reducing manual tasks.

## Features

- Manage reservations:
  - Add, view, modify, and delete bookings.
- Manage clients:
  - Add, view, modify, and delete client information.
- Manage cars:
  - Add, view, modify, and delete car details.
  - Check the availability of cars.
- Graphical interfaces:
  - Intuitive interfaces for reservations, clients, and cars.
  - Easy navigation with a customizable NavBar.

## Installation

To install and use this module, follow these steps:

1. Ensure you have Odoo installed on your system.
      **Install PostgreSQL**:
   ```bash
   sudo apt-get install postgresql
   sudo su - postgres
   createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo17_user
   psql
   Alter USER odoo17_user WITH SUPERPOWER
   ```
   **Install PostgreSQL**:
    ```bash
   git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0 --single-branch odoo17
   cd odoo17
   pip3 install -r requirements.txt
   ```
      **Create odoo.conf and save your information in it**:
   
   ![image](https://github.com/chouhlaoui/RentMangOdoo/assets/61617827/3768ca3d-b32e-41b5-bc86-fbe0dcc2b0ce)

3. Run your Odoo
4. Install the module from the Odoo Apps menu.
5. Test it


## Usage

Once installed, access the Car Rental Management module from the Odoo interface. Use the provided interfaces to manage reservations, clients, and cars efficiently. 

## License

Feel free to contribute and make this module even better!
## Contact
For any inquiries or feedback regarding DermWise, please contact Chouroukhalaoui@gmail.com.

Thank you for using this Odoo module Beauty Advisor!

