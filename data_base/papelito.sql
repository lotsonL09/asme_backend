USE asme;

select id_user,DNI,first_name,last_name,t.team_name,a.area_name 
from users u,teams t,areas a 
WHERE DNI=87621311 AND u.id_team = t.id_team AND u.id_area = a.id_area;

SELECT t.id_ticket, t.number_ticket, b.first_name,b.last_name, b.DNI, b.email, b.cell_phone, t.booking_time 
FROM tickets t, buyers b 
WHERE t.id_user = 27 AND b.id_ticket = t.id_ticket AND t.booked = 0;

SELECT t.id_ticket, t.number_ticket 
FROM tickets t 
WHERE t.id_user = 27 AND t.booked = 0;


SELECT * FROM buyers;

SELECT * FROM tickets WHERE id_user = 27 AND booked = 0;

INSERT buyers(first_name,last_name,DNI,email,cell_phone) VALUES("William","Valencia","71414470","william@gmail.com","987654321");
INSERT buyers(first_name,last_name,DNI,email,cell_phone,id_ticket) VALUES("William","Valencia","71414470","william@gmail.com","987654321",782);

UPDATE tickets
set booked = 1
WHERE id_ticket = 782;

UPDATE buyers
SET id_ticket = 781
WHERE id_buyer=1;

UPDATE tickets
SET booked = 1
WHERE id_ticket=781;

SELECT number_ticket FROM tickets WHERE id_user = 1 AND booked = 1 LIMIT 1;

SELECT COUNT(booked) AS total_remain FROM tickets WHERE id_user = 1 AND booked = 0;

SELECT COUNT(booked) AS total_booked FROM tickets WHERE id_user = 1 AND booked = 1;

