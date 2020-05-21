create database project1;
use project1;
/*Course(Course_No, Course_Name, Credit, TA_hr_req) */

/*Section(Sec_No, Course_No, Year, Semester, Max_enroll, Instructor_SSN) */
/*Staff(T_SSN, T_Name, T_ADD, Function, T_Salary, Rank, Course_Load, Work_hr) */
/*For every course, the student should be able to see the existing sections, the instructor and number of students currently 
registered and the maximum number of students that can be allowed in the section. */




/*Staff(T_SSN, T_Name, T_ADD, Function, T_Salary, rnk, Course_Load, Work_hr) */

create table staff(staff_ssn int primary key not null,staff_name varchar(15) not null, field varchar(15) not null 
check (field='staff' or field='faculty' or field='TA'),salary int not null, rnk int not null, course_load int not null,work_hr int not null );


create table building(building_id int not null primary key, building_name varchar(15) not null,location varchar(15) not null);



create table department(dept_id int not null primary key, dept_name varchar(15) not null,annual_budget int not null,dept_chair varchar(15) not null,building_id int not null, 
foreign key(building_id) references building(building_id));

create table course(course_no int not null primary key, course_name varchar(15) not null,year1 int not null, credit int not null,
ta_hr_req int not null,dept_id int not null, foreign key (dept_id) references department(dept_id));


create table section(sec_no int primary key not null, course_no int not null,year1 int not null,staff_ssn int not null,current_enrolled int,max_enroll int not null, 
foreign key (course_no) references course(course_no), foreign key(staff_ssn) references staff(staff_ssn));

/*Student(S_ID, S_SSN, S_Name, S_Add, S_High, S_Year, Dept_ID)  */

create table student(s_id int primary key not null,s_ssn int unique key not null,s_name varchar(15) not null,s_address varchar(15) not null,s_highschool varchar(15) not null,s_year int not null,dept_id int not null, 
foreign key(dept_id) references department(dept_id));
/*Registeration*/


create table registeration(s_id int not null,sec_no int not null , course_no int not null,foreign key (course_no) references course(course_no), 
foreign key (sec_no) references section(sec_no)
 );
 
 
 create table sectioninroom(building_id int not null,room_no int not null,course_no int not null,sec_no int not null, weekday1 varchar(25) not null,time1 time not null,
 foreign key (building_id) references building(building_id),
 foreign key (course_no) references course(course_no), foreign key (sec_no) references section(sec_no), check (weekday1 in ('Monday','Tuesday','Wednesday','Thrusday','Friday')));
 /*,constraint total_check 
check (1>=all (select count(registeration.s_id) from registeration group by registeration.course_no,registeration.sec_no ))*/
 
/*alter table registeration add constraint registeration_check 
check (1>=all (select count(registeration.s_id) from registeration group by registeration.course_no,registeration.sec_no ));*/


/*alter table registeration add constraint sec_no check(sec_no <> 
(select r.sec_no from registeration r,registeration r1 where r.s_id=r1.s_id and r.course_no=r1.course_no ));*/
/*triggers*/

/*delimiter $
create trigger registeration123 
after delete on registeration for each row
begin
if (old.s_id = s_id) and (old.course_no= course_no) and (old.sec_no = sec_no) 
then delete from registeration where old.s_id=s_id and old.course_no=course_no and old.sec_no=sec_no;
end if;
end $
delimiter ;*/

select c.dept_id,s.course_no,s.sec_no,count(registeration.s_id) as already_registered,staff_name,max_enroll 
from registeration,student,course c,section s,staff where staff.staff_ssn=s.staff_ssn 
and s.course_no=c.course_no and registeration.s_id=student.s_id and registeration.course_no=c.course_no group by s.course_no,s.sec_no;



/*Building(Building_ID, B_Name, Location) */



/*SectionInRoom(Building_ID, Room_No, Course_No, Sec_No, Weekday, Time) weekday1 in */


