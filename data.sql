INSERT INTO books VALUES (1, 'The Early Bird', 'John Smith', 1900);
INSERT INTO books VALUES (2, 'Modern Times', 'Jane Doe', 2020);
INSERT INTO books VALUES (3, 'Future Glimpse', 'Future Author', 2050);
INSERT INTO books VALUES (4, 'Repeated Title', 'Author One', 2000);
INSERT INTO books VALUES (5, 'Repeated Title', 'Author Two', 2010);
INSERT INTO books VALUES (6, 'Case Test', 'Author Case', 2000);
INSERT INTO books VALUES (7, 'case test', 'author case', 2005);
INSERT INTO books VALUES (8, 'Special Characters &%', 'Strange Author', 2000);

INSERT INTO members VALUES ('1.com', 'Password', 'John Doe', 1985, 'Engineering');
INSERT INTO members VALUES ('2.com', 'password123', 'Jane Smith', 1990, 'Science');
INSERT INTO members VALUES ('3.com', '12345', 'Unique User', 2000, 'Arts');
INSERT INTO members VALUES ('4.com', 'caseTest123', 'Case Test', 1995, 'Business');
INSERT INTO members VALUES ('5.com', 'CaseTest321', 'Case Test', 1995, 'Business');

INSERT INTO borrowings VALUES (1, '1.com', 1, '2024-01-01', '2024-01-31');
INSERT INTO borrowings VALUES (2, '1.com', 2, '2024-02-01', NULL);
INSERT INTO borrowings VALUES (3, '2.com', 3, '2024-01-01', NULL);
INSERT INTO borrowings VALUES (4, '3.com', 4, '2024-02-04', '2024-03-10');
INSERT INTO borrowings VALUES (5, '4.com', 5, '2024-03-01', NULL);
INSERT INTO borrowings VALUES (6, '5.com', 6, '2024-03-05', NULL);

INSERT INTO penalties VALUES (1, 1, 10, 5);
INSERT INTO penalties VALUES (3, 4, 15, NULL);

INSERT INTO reviews VALUES (1, 1, '1.com', 5, 'Great book!', '2024-01-22');
INSERT INTO reviews VALUES (2, 2, '2.com', 4, '', '2024-02-02');
INSERT INTO reviews VALUES (3, 4, '3.com', 3, 'Decent read.', '2024-01-11');
INSERT INTO reviews VALUES (4, 5, '4.com', 2, 'Could be better.', '2024-03-02');
INSERT INTO reviews VALUES (5, 6, '5.com', 1, 'Did not enjoy.', '2024-03-06');


-- Adding more members
INSERT INTO members VALUES ('6.com', 'securePass123', 'New Member', 1998, 'Literature');
INSERT INTO members VALUES ('7.com', '1', 'Experienced Member', 1980, 'History');

-- Adding more borrowings (some will be overdue to test the overdue functionality)
-- Assume today's date is 2024-03-15 for calculating overdue
INSERT INTO borrowings VALUES (7, '6.com', 7, '2024-02-20', NULL); -- Overdue
INSERT INTO borrowings VALUES (8, '6.com', 8, '2024-03-01', NULL); -- Not overdue
INSERT INTO borrowings VALUES (9, '7.com', 2, '2024-01-10', '2024-02-05'); -- Returned on time
INSERT INTO borrowings VALUES (10, '7.com', 3, '2024-03-01', NULL); -- Not overdue
INSERT INTO borrowings VALUES (11, '7.com', 1, '2024-02-22', NULL); -- Overdue

-- Adding penalties for overdue borrowings (assuming a penalty has been assigned to each overdue borrowing)
INSERT INTO penalties VALUES (4, 7, 20, 0); -- Not paid
INSERT INTO penalties VALUES (5, 11, 15, NULL); -- Not paid

-- You can also add more reviews if needed for a more comprehensive testing
INSERT INTO reviews VALUES (6, 7, '6.com', 4, 'Interesting insights.', '2024-03-05');
INSERT INTO reviews VALUES (7, 8, '7.com', 5, 'A must-read!', '2024-03-10');


-- Adding more borrowings for member '7.com', including overdue borrowings
-- Assuming today's date is 2024-03-15 for calculating overdue

-- Borrowed on time but not yet returned, not overdue
INSERT INTO borrowings VALUES (12, '7.com', 4, '2024-02-20', NULL);

-- Overdue borrowing
INSERT INTO borrowings VALUES (13, '7.com', 5, '2024-01-10', NULL);

-- Another overdue borrowing
INSERT INTO borrowings VALUES (14, '7.com', 6, '2024-01-15', NULL);

-- Recently borrowed, not overdue
INSERT INTO borrowings VALUES (15, '7.com', 7, '2024-03-01', NULL);

-- Penalties for overdue borrowings (13 and 14) by '7.com'
-- Borrowing 13 is 34 days overdue (penalty $14)
-- Borrowing 14 is 29 days overdue (penalty $9)

-- We'll assume these are penalties 6 and 7 in your penalties table
INSERT INTO penalties VALUES (8, 13, 14, NULL);  -- Not paid yet
INSERT INTO penalties VALUES (9, 14, 9, NULL);   -- Not paid yet


-- Review by '7.com' for the book from borrowing 13
-- Assuming this is review 8 in your reviews table
INSERT INTO reviews VALUES (8, 5, '7.com', 4, 'Insightful read with compelling arguments.', '2024-03-15');
