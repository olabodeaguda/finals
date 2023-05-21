SELECT ln.id loanID,
 u.gender Gender,
  (case 
	when reg.k_relation_fam = 'Spouse' then 'Y' else 'N' end) Married,
 (case 
	when reg.k_relation_fam = 'Spouse' then 'Y'
	when reg.k_relation_fam = 'Child' then 'Y' else 'N' END) Dependents,
 (case when reg.employment = 'Employed' then 'Graduate' else 'Under Graduate' End) Education,
 (case when reg.employment = 'Employed' then 'N' else 'Y' End) Self_Employed,
 (case 
    when reg.salary = '50k – 100k' then '100000'
    when reg.salary = 'Less than 50k' then '50000'
    when reg.salary = '101k – 200k' then '200000'
    when reg.salary = 'Above 300k' then '301000'
    when reg.salary = '201k – 300k' then '300000'
	else '20000' END) ApplicantIncome,
  (case 
    when reg.salary = '50k – 100k' then 0.75 * 100000
    when reg.salary = 'Less than 50k' then 0.75 * 50000
    when reg.salary = '101k – 200k' then 0.75 * 200000
    when reg.salary = 'Above 300k' then 0.75 * 301000
    when reg.salary = '201k – 300k' then 0.75 * 300000
	else 0.75 * 20000 END) CoapplicantIncome,
 ln.amount LoanAmount,
 ten.days Loan_Amount_Term, 
 ( year(now()) - year(Date(reg.dob))) DateOfBirth,
 case when reg.mono_account_id is not null then 'Y' else 'N' END Credit_History,
(case 
	when reg.state = 'Lagos' then 'Urban' 
	when reg.state = 'FCT - Abuja' then 'Urban' 
	when reg.state = 'Cross River' then 'Urban' 
	when reg.state = 'Rivers' then 'Urban' 
    else 'Rural' end) Property_Area,
 (case reg.status when 'APPROVED' then 'Y' else 'N' END) Loan_Status
 FROM loan247.quick_loan_apps ln
 inner join loan_registrations reg on reg.id = ln.reg_id
 inner join users u on u.id = reg.user_id
 inner join tenure_ints ten on ten.id = ln.tenure_int_id