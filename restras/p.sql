CREATE TABLE hotel
(
	hotel_name 		varchar(32)	,
	city_name		varchar(32)	,
	type			varchar(32)	,
	s_limit			integer	,
	CONSTRAINT hotel_pk PRIMARY KEY(hotel_name)
);
	
CREATE TABLE booking_history
(
	hotel_name			varchar(32)	,
	booking_date		date	,
	no_of_seats			integer	
	);
	
