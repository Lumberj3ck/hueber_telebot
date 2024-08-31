delete from book;
delete from lecture;
delete from audio;

insert into book values 
(1, 'Schritte plus neu a1.1'),
(2, 'Schritte plus neu a1.2');


insert into lecture values 
(1, 1, 'book' , 1),
(2, 2, 'book' , 1),
(3, 3, 'book' , 1);


insert into audio values 
(1, '301081_AB_L01_01.mp3', 1),
(2, '301081_AB_L01_02.mp3', 1)
;