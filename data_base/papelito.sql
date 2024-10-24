USE asme;

select id_user,DNI,first_name,last_name,t.team_name,a.area_name 
from users u,teams t,areas a 
WHERE DNI=87621311 AND u.id_team = t.id_team AND u.id_area = a.id_area;


SELECT COUNT(booked) AS total_remain FROM tickets WHERE id_user = 1 AND booked = 0;