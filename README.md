# Database Schema README

## Overview

This document outlines the schema for tracking water quality data. It includes details about users, locations, and water quality measurements, designed to facilitate data collection and analysis without requiring authentication.

## Schema Design

### Tables

#### **1. User**

- **Purpose**: To store basic information about individuals who collect water quality data.
- **Columns**:
  - **`user_id`**: Unique identifier for each user (Primary Key).
  - **`name`**: Full name of the user.
  - **`email`**: Email address of the user (Unique).
  - **`profession`**: Profession or role of the user.

| Column Name | Data Type | Constraints                | Description                       |
|-------------|-----------|----------------------------|-----------------------------------|
| `user_id`   | INT       | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each user   |
| `name`      | VARCHAR   | NOT NULL                   | Full name of the user             |
| `email`     | VARCHAR   | NOT NULL, UNIQUE           | Email address of the user         |
| `profession`| VARCHAR   | NULL                       | Profession or role of the user    |

#### **2. Location**

- **Purpose**: To store details about the locations where water samples are collected.
- **Columns**:
  - **`location_id`**: Unique identifier for each location (Primary Key).
  - **`name`**: Name of the location.
  - **`latitude`**: Latitude coordinate of the location.
  - **`longitude`**: Longitude coordinate of the location.
  - **`address`**: Address of the location (Optional).

| Column Name | Data Type | Constraints                | Description                         |
|-------------|-----------|----------------------------|-------------------------------------|
| `location_id`| INT       | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each location |
| `name`      | VARCHAR   | NOT NULL                   | Name of the location                |
| `latitude`  | FLOAT     | NOT NULL                   | Latitude coordinate                 |
| `longitude` | FLOAT     | NOT NULL                   | Longitude coordinate                |
| `address`   | VARCHAR   | NULL                       | Address of the location (Optional)  |

#### **3. WaterQuality**

- **Purpose**: To record water quality measurements associated with a specific user and location.
- **Columns**:
  - **`id`**: Unique identifier for each water quality record (Primary Key).
  - **`location_id`**: Reference to the `Location` table (Foreign Key).
  - **`user_id`**: Reference to the `User` table (Foreign Key).
  - **`ph`**: pH level of the water.
  - **`Hardness`**: Hardness of the water (e.g., in mg/L as CaCO3).
  - **`Solids`**: Total dissolved solids (e.g., in mg/L).
  - **`Chloramines`**: Chloramines level in the water (e.g., in mg/L).
  - **`Sulfate`**: Sulfate concentration (e.g., in mg/L).
  - **`Conductivity`**: Conductivity of the water (e.g., in µS/cm).
  - **`Organic_carbon`**: Organic carbon concentration (e.g., in mg/L).
  - **`Trihalomethanes`**: Trihalomethanes concentration (e.g., in µg/L).
  - **`Turbidity`**: Turbidity of the water (e.g., in NTU).
  - **`Potability`**: Indicator of water potability (0 for non-potable, 1 for potable).

| Column Name         | Data Type | Constraints                | Description                                  |
|---------------------|-----------|----------------------------|----------------------------------------------|
| `id`                | INT       | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each record            |
| `location_id`       | INT       | NOT NULL, FOREIGN KEY      | Reference to the `Location` table            |
| `user_id`           | INT       | NOT NULL, FOREIGN KEY      | Reference to the `User` table                |
| `ph`                | FLOAT     | NOT NULL                   | pH level of the water                        |
| `Hardness`          | FLOAT     | NOT NULL                   | Hardness of the water (e.g., in mg/L as CaCO3) |
| `Solids`            | FLOAT     | NOT NULL                   | Total dissolved solids (e.g., in mg/L)       |
| `Chloramines`       | FLOAT     | NOT NULL                   | Chloramines level in the water (e.g., in mg/L)|
| `Sulfate`           | FLOAT     | NOT NULL                   | Sulfate concentration (e.g., in mg/L)        |
| `Conductivity`      | FLOAT     | NOT NULL                   | Conductivity of the water (e.g., in µS/cm)    |
| `Organic_carbon`    | FLOAT     | NOT NULL                   | Organic carbon concentration (e.g., in mg/L) |
| `Trihalomethanes`   | FLOAT     | NOT NULL                   | Trihalomethanes concentration (e.g., in µg/L)|
| `Turbidity`         | FLOAT     | NOT NULL                   | Turbidity of the water (e.g., in NTU)        |
| `Potability`        | BOOLEAN   | NOT NULL                   | Water potability (0 for non-potable, 1 for potable) |

### Relationships

- **One-to-Many Relationships**:
  - One `User` can be associated with many `WaterQuality` records.
  - One `Location` can be associated with many `WaterQuality` records.
  - One `Location` can be associated with many `Users` (multiple users can collect data from the same location).

- **Foreign Keys**:
  - `WaterQuality.location_id` references `Location.location_id`.
  - `WaterQuality.user_id` references `User.user_id`.

## Summary

This schema provides a structured approach to managing and analyzing water quality data. By linking water quality records to both users and locations, it supports effective tracking and analysis of data collected from various sources. The schema also accommodates the scenario where multiple users can gather data from the same location, ensuring comprehensive data collection and analysis capabilities.

