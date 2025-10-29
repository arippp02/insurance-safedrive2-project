-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 09, 2025 at 08:07 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `safedrive2`
--

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

CREATE TABLE `application` (
  `Application_ID` int(11) NOT NULL,
  `Officer_ID` int(11) DEFAULT NULL,
  `ReviewDate` date DEFAULT NULL,
  `Purpose` varchar(255) DEFAULT NULL,
  `ApprovalStatus` varchar(50) DEFAULT NULL,
  `ApplicationDate` date DEFAULT NULL,
  `PolicyType_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`Application_ID`, `Officer_ID`, `ReviewDate`, `Purpose`, `ApprovalStatus`, `ApplicationDate`, `PolicyType_ID`) VALUES
(1, 182, '2025-01-01', 'New application', 'Approved', '2025-01-01', 1),
(2, 243, '2025-02-13', 'Entah test', 'Pending', '2025-02-01', 2);

-- --------------------------------------------------------

--
-- Table structure for table `claim`
--

CREATE TABLE `claim` (
  `Claim_ID` int(11) NOT NULL,
  `Policy_ID` int(11) DEFAULT NULL,
  `DateOfClaim` date DEFAULT NULL,
  `ClaimAmount` decimal(10,2) DEFAULT NULL,
  `ClaimStatus` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `commercial_vehicle`
--

CREATE TABLE `commercial_vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `BusinessName` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `commercial_vehicle`
--

INSERT INTO `commercial_vehicle` (`Vehicle_ID`, `BusinessName`) VALUES
(2, 'Roti Angrip');

-- --------------------------------------------------------

--
-- Table structure for table `comprehensive_policy`
--

CREATE TABLE `comprehensive_policy` (
  `Policy_ID` int(11) NOT NULL,
  `AccidentCoverage` decimal(10,2) DEFAULT NULL,
  `TheftCoverage` decimal(10,2) DEFAULT NULL,
  `GlassCoverage` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comprehensive_policy`
--

INSERT INTO `comprehensive_policy` (`Policy_ID`, `AccidentCoverage`, `TheftCoverage`, `GlassCoverage`) VALUES
(0, 100.00, 200.00, 100.00),
(5, 10.00, 10.00, 10.00),
(6, 50.00, 50.00, 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `insurance_officer`
--

CREATE TABLE `insurance_officer` (
  `Officer_ID` int(11) NOT NULL,
  `FullName` varchar(100) DEFAULT NULL,
  `Position` varchar(50) DEFAULT NULL,
  `ContactDetails` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `insurance_officer`
--

INSERT INTO `insurance_officer` (`Officer_ID`, `FullName`, `Position`, `ContactDetails`) VALUES
(182, 'Muhammad Angrip', 'Senior Officer', '081-2228'),
(243, 'Kim Nam Joon', 'Officer', '081-2274');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `Payment_ID` int(11) NOT NULL,
  `Policy_ID` int(11) DEFAULT NULL,
  `PaymentDate` date DEFAULT NULL,
  `AmountPaid` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `personal_vehicle`
--

CREATE TABLE `personal_vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `OwnerName` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personal_vehicle`
--

INSERT INTO `personal_vehicle` (`Vehicle_ID`, `OwnerName`) VALUES
(0, 'Muhammad Logowo'),
(3, 'Longgowo'),
(4, 'Aszreen');

-- --------------------------------------------------------

--
-- Table structure for table `policy`
--

CREATE TABLE `policy` (
  `Policy_ID` int(11) NOT NULL,
  `PolicyType` varchar(50) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `PremiumAmount` decimal(10,2) DEFAULT NULL,
  `CoverageAmount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy`
--

INSERT INTO `policy` (`Policy_ID`, `PolicyType`, `StartDate`, `EndDate`, `PremiumAmount`, `CoverageAmount`) VALUES
(2, '1', '2025-01-02', '2028-01-01', 15000.00, 5000.00),
(4, '2', '2025-03-09', '2027-06-25', 10000.00, 2000.00),
(5, '1', '2024-01-01', '2025-01-01', 1000.00, 10.00),
(6, '1', '2024-01-01', '2025-01-01', 10000.00, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `policyholder`
--

CREATE TABLE `policyholder` (
  `Policyholder_ID` int(11) NOT NULL,
  `Policyholder_Name` varchar(100) DEFAULT NULL,
  `Application_ID` int(11) DEFAULT NULL,
  `ContactDetails` varchar(255) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `DrivingLicenseNumber` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policyholder`
--

INSERT INTO `policyholder` (`Policyholder_ID`, `Policyholder_Name`, `Application_ID`, `ContactDetails`, `DateOfBirth`, `DrivingLicenseNumber`) VALUES
(1, 'Muhammad Logowo', 0, '0163076163', '2002-03-16', 'QBD6276'),
(2, 'Angrip', 0, '0163076163', '2002-03-16', 'QBD6276');

-- --------------------------------------------------------

--
-- Table structure for table `policyholder_backup`
--

CREATE TABLE `policyholder_backup` (
  `Policyholder_ID` int(11) NOT NULL,
  `Policyholder_Name` varchar(100) DEFAULT NULL,
  `Application_ID` int(11) DEFAULT NULL,
  `ContactDetails` varchar(255) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `DrivingLicenseNumber` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policyholder_backup`
--

INSERT INTO `policyholder_backup` (`Policyholder_ID`, `Policyholder_Name`, `Application_ID`, `ContactDetails`, `DateOfBirth`, `DrivingLicenseNumber`) VALUES
(0, 'Muhammad Logowo', 0, '0163076163', '2002-03-16', 'QBD6276');

-- --------------------------------------------------------

--
-- Table structure for table `policytype`
--

CREATE TABLE `policytype` (
  `PolicyType_ID` int(11) NOT NULL,
  `PolicyType_Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policytype`
--

INSERT INTO `policytype` (`PolicyType_ID`, `PolicyType_Name`) VALUES
(1, 'Comprehensive'),
(2, 'ThirdParty');

-- --------------------------------------------------------

--
-- Table structure for table `policy_vehicle`
--

CREATE TABLE `policy_vehicle` (
  `Policy_ID` int(11) NOT NULL,
  `Vehicle_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy_vehicle`
--

INSERT INTO `policy_vehicle` (`Policy_ID`, `Vehicle_ID`) VALUES
(2, 0),
(2, 2),
(2, 4);

-- --------------------------------------------------------

--
-- Table structure for table `thirdparty_policy`
--

CREATE TABLE `thirdparty_policy` (
  `Policy_ID` int(11) NOT NULL,
  `LiabilityCoverage` decimal(10,2) DEFAULT NULL,
  `InjuryCoverage` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `Policyholder_ID` int(11) DEFAULT NULL,
  `VehicleType` varchar(50) DEFAULT NULL,
  `MakeModel` varchar(100) DEFAULT NULL,
  `YearOfManufacture` year(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`Vehicle_ID`, `Policyholder_ID`, `VehicleType`, `MakeModel`, `YearOfManufacture`) VALUES
(2, 0, 'Commercial', 'Toyota Harrier', '2016'),
(3, 0, 'Personal', 'Mitsubishi RX7', '2001'),
(4, 1, 'Personal', 'Toyota Wish', '2012');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `application`
--
ALTER TABLE `application`
  ADD PRIMARY KEY (`Application_ID`),
  ADD KEY `FK_Application_Officer` (`Officer_ID`),
  ADD KEY `FK_PolicyType` (`PolicyType_ID`);

--
-- Indexes for table `claim`
--
ALTER TABLE `claim`
  ADD PRIMARY KEY (`Claim_ID`),
  ADD KEY `Policy_ID` (`Policy_ID`);

--
-- Indexes for table `commercial_vehicle`
--
ALTER TABLE `commercial_vehicle`
  ADD PRIMARY KEY (`Vehicle_ID`);

--
-- Indexes for table `comprehensive_policy`
--
ALTER TABLE `comprehensive_policy`
  ADD PRIMARY KEY (`Policy_ID`);

--
-- Indexes for table `insurance_officer`
--
ALTER TABLE `insurance_officer`
  ADD PRIMARY KEY (`Officer_ID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`Payment_ID`),
  ADD KEY `Policy_ID` (`Policy_ID`);

--
-- Indexes for table `personal_vehicle`
--
ALTER TABLE `personal_vehicle`
  ADD PRIMARY KEY (`Vehicle_ID`);

--
-- Indexes for table `policy`
--
ALTER TABLE `policy`
  ADD PRIMARY KEY (`Policy_ID`);

--
-- Indexes for table `policyholder`
--
ALTER TABLE `policyholder`
  ADD PRIMARY KEY (`Policyholder_ID`),
  ADD KEY `fk_application_id` (`Application_ID`);

--
-- Indexes for table `policytype`
--
ALTER TABLE `policytype`
  ADD PRIMARY KEY (`PolicyType_ID`),
  ADD UNIQUE KEY `PolicyType_Name` (`PolicyType_Name`);

--
-- Indexes for table `policy_vehicle`
--
ALTER TABLE `policy_vehicle`
  ADD PRIMARY KEY (`Policy_ID`,`Vehicle_ID`),
  ADD KEY `fk_policy_vehicle_cascade` (`Vehicle_ID`);

--
-- Indexes for table `thirdparty_policy`
--
ALTER TABLE `thirdparty_policy`
  ADD PRIMARY KEY (`Policy_ID`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`Vehicle_ID`),
  ADD KEY `vehicle_ibfk_1` (`Policyholder_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `application`
--
ALTER TABLE `application`
  MODIFY `Application_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `policy`
--
ALTER TABLE `policy`
  MODIFY `Policy_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `policyholder`
--
ALTER TABLE `policyholder`
  MODIFY `Policyholder_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `policytype`
--
ALTER TABLE `policytype`
  MODIFY `PolicyType_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `Vehicle_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `application`
--
ALTER TABLE `application`
  ADD CONSTRAINT `FK_Application_Officer` FOREIGN KEY (`Officer_ID`) REFERENCES `insurance_officer` (`Officer_ID`),
  ADD CONSTRAINT `FK_PolicyType` FOREIGN KEY (`PolicyType_ID`) REFERENCES `policytype` (`PolicyType_ID`);

--
-- Constraints for table `claim`
--
ALTER TABLE `claim`
  ADD CONSTRAINT `claim_ibfk_1` FOREIGN KEY (`Policy_ID`) REFERENCES `policy` (`Policy_ID`);

--
-- Constraints for table `commercial_vehicle`
--
ALTER TABLE `commercial_vehicle`
  ADD CONSTRAINT `fk_commercial_vehicle_cascade` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `comprehensive_policy`
--
ALTER TABLE `comprehensive_policy`
  ADD CONSTRAINT `comprehensive_policy_ibfk_1` FOREIGN KEY (`Policy_ID`) REFERENCES `policy` (`Policy_ID`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`Policy_ID`) REFERENCES `policy` (`Policy_ID`);

--
-- Constraints for table `personal_vehicle`
--
ALTER TABLE `personal_vehicle`
  ADD CONSTRAINT `fk_personal_vehicle_cascade` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `policyholder`
--
ALTER TABLE `policyholder`
  ADD CONSTRAINT `FK_Policyholder_Application` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`),
  ADD CONSTRAINT `fk_application_id` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`);

--
-- Constraints for table `policy_vehicle`
--
ALTER TABLE `policy_vehicle`
  ADD CONSTRAINT `fk_policy_vehicle_cascade` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `policy_vehicle_ibfk_1` FOREIGN KEY (`Policy_ID`) REFERENCES `policy` (`Policy_ID`);

--
-- Constraints for table `thirdparty_policy`
--
ALTER TABLE `thirdparty_policy`
  ADD CONSTRAINT `thirdparty_policy_ibfk_1` FOREIGN KEY (`Policy_ID`) REFERENCES `policy` (`Policy_ID`);

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`Policyholder_ID`) REFERENCES `policyholder` (`Policyholder_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
