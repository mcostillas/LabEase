-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 12, 2025 at 07:23 PM
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
-- Database: `labease`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserID` int(11) NOT NULL,
  `FullName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `ContactNumber` varchar(11) DEFAULT NULL,
  `UserType` enum('Student','Instructor','Admin','Guest','LabInCharge','LabDirector') NOT NULL,
  `IsActive` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`UserID`, `FullName`, `Email`, `ContactNumber`, `UserType`, `IsActive`) VALUES
(1, 'John Smith', 'john.smith@example.com', '09123456789', 'Student', 1),
(2, 'Maria Garcia', 'maria.garcia@example.com', '09234567890', 'Student', 1),
(3, 'Dr. James Wilson', 'james.wilson@example.com', '09345678901', 'Instructor', 1),
(4, 'Prof. Sarah Chen', 'sarah.chen@example.com', '09456789012', 'Instructor', 1),
(5, 'Admin User', 'admin@example.com', '09567890123', 'Admin', 1),
(6, 'John Doe', 'john.doe@example.com', '09123456789', 'Student', 1),
(7, 'Alice Smith', 'alice.smith@example.com', '09234567890', 'Guest', 1),
(8, 'Lab In-Charge', 'labincharge@example.com', '09345678901', 'LabInCharge', 1),
(9, 'Lab Director', 'labdirector@example.com', '09456789012', 'LabDirector', 1);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--

CREATE TABLE `credentials` (
  `CredentialID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `LastLogin` datetime DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT 1,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `credentials`
--

INSERT INTO `credentials` (`CredentialID`, `UserID`, `Password`, `IsActive`) VALUES
(1, 3, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNZyHHu7iYEie', 1),
(2, 4, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNZyHHu7iYEie', 1),
(3, 5, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNZyHHu7iYEie', 1);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`CredentialID`),
  ADD KEY `UserID` (`UserID`);

--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `CredentialID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for table `credentials`
--
ALTER TABLE `credentials`
  ADD CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `laboratory`
--

CREATE TABLE `laboratory` (
  `LabID` int(11) NOT NULL,
  `LabName` varchar(255) NOT NULL,
  `Capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `laboratory`
--

INSERT INTO `laboratory` (`LabID`, `LabName`, `Capacity`) VALUES
(1, 'Computer Laboratory A', 30),
(2, 'Computer Laboratory B', 25),
(3, 'Software Development Lab', 20),
(4, 'Computer Lab A', 30),
(5, 'Computer Lab B', 25);

--
-- Indexes for table `laboratory`
--
ALTER TABLE `laboratory`
  ADD PRIMARY KEY (`LabID`);

--
-- AUTO_INCREMENT for table `laboratory`
--
ALTER TABLE `laboratory`
  MODIFY `LabID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `StudentID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `StudentNumber` varchar(20) NOT NULL,
  `Course` varchar(100) NOT NULL,
  `YearLevel` int(11) NOT NULL,
  `Department` varchar(100) NOT NULL,
  `StudentStatus` enum('Regular','Irregular') DEFAULT 'Regular'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`StudentID`, `UserID`, `StudentNumber`, `Course`, `YearLevel`, `Department`, `StudentStatus`) VALUES
(1, 1, '2025-0001', 'BS Computer Science', 3, 'Computer Science', 'Regular'),
(2, 2, '2025-0002', 'BS Information Technology', 2, 'Information Technology', 'Regular'),
(3, 6, '2025-0003', 'BS Computer Science', 3, 'Computer Science', 'Regular');

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`StudentID`),
  ADD KEY `UserID` (`UserID`);

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `StudentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `InstructorID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `Department` varchar(100) NOT NULL,
  `EmployeeID` varchar(20) NOT NULL,
  `Position` varchar(100) NOT NULL,
  `Specialization` varchar(255) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`InstructorID`, `UserID`, `Department`, `EmployeeID`, `Position`, `Specialization`, `IsActive`) VALUES
(1, 3, 'Computer Science', 'INS-2025-001', 'Associate Professor', 'Software Engineering', 1),
(2, 4, 'Information Technology', 'INS-2025-002', 'Assistant Professor', 'Database Systems', 1);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`InstructorID`),
  ADD KEY `UserID` (`UserID`);

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `InstructorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for table `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `class_schedule`
--

CREATE TABLE `class_schedule` (
  `ClassScheduleID` int(11) NOT NULL,
  `LabID` int(11) DEFAULT NULL,
  `InstructorID` int(11) DEFAULT NULL,
  `DayOfWeek` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL,
  `Semester` varchar(20) NOT NULL,
  `SchoolYear` varchar(20) NOT NULL,
  `Section` varchar(20) NOT NULL,
  `IsActive` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `class_schedule`
--

INSERT INTO `class_schedule` (`ClassScheduleID`, `LabID`, `InstructorID`, `DayOfWeek`, `StartTime`, `EndTime`, `Semester`, `SchoolYear`, `Section`, `IsActive`) VALUES
(1, 1, 1, 'Monday', '09:00:00', '11:00:00', 'First', '2024-2025', 'CS-3A', 1),
(2, 2, 1, 'Wednesday', '13:00:00', '15:00:00', 'First', '2024-2025', 'CS-3B', 1),
(3, 3, 2, 'Tuesday', '10:00:00', '12:00:00', 'First', '2024-2025', 'IT-2A', 1);

--
-- Indexes for table `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD PRIMARY KEY (`ClassScheduleID`),
  ADD KEY `LabID` (`LabID`),
  ADD KEY `InstructorID` (`InstructorID`);

--
-- AUTO_INCREMENT for table `class_schedule`
--
ALTER TABLE `class_schedule`
  MODIFY `ClassScheduleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for table `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD CONSTRAINT `class_schedule_ibfk_1` FOREIGN KEY (`LabID`) REFERENCES `laboratory` (`LabID`) ON DELETE CASCADE,
  ADD CONSTRAINT `class_schedule_ibfk_2` FOREIGN KEY (`InstructorID`) REFERENCES `instructor` (`InstructorID`) ON DELETE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `AttendanceID` int(11) NOT NULL,
  `StudentID` int(11) DEFAULT NULL,
  `ClassScheduleID` int(11) DEFAULT NULL,
  `Date` date NOT NULL,
  `TimeIn` time DEFAULT NULL,
  `TimeOut` time DEFAULT NULL,
  `Status` enum('Present','Late','Absent','Excused') DEFAULT NULL,
  `Remarks` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`AttendanceID`, `StudentID`, `ClassScheduleID`, `Date`, `TimeIn`, `TimeOut`, `Status`, `Remarks`) VALUES
(1, 1, 1, '2025-03-11', '09:05:00', '11:00:00', 'Present', NULL),
(2, 2, 3, '2025-03-12', '10:15:00', '12:00:00', 'Late', 'Traffic delay'),
(3, 1, 1, '2025-03-13', '09:00:00', '11:00:00', 'Present', NULL);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`AttendanceID`),
  ADD KEY `StudentID` (`StudentID`),
  ADD KEY `ClassScheduleID` (`ClassScheduleID`);

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `AttendanceID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `student` (`StudentID`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`ClassScheduleID`) REFERENCES `class_schedule` (`ClassScheduleID`) ON DELETE CASCADE;

-- Rest of your tables and data here --

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
