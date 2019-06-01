SELECT  sum(`outstanding_amount`) as outstanding_amount, 
        CONCAT(YEAR(`creation_date`), CONCAT('-',MONTH(`creation_date`))) as year_and_month 
    FROM `syncinvoice` 
    where frenns_id = 'RAHULSPS' 
    group by `frenns_id`,CONCAT(YEAR(`creation_date`), MONTH(`creation_date`)) 
    order by creation_date ASC;

/*==   ==*/

SELECT  syncinvoice_id, 
        date(issue_date) as issue_date, 
        date(due_date) as due_date, 
        date(pay_date) as pay_date, 
        COALESCE(DATEDIFF(date(pay_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days, 
        DATEDIFF(date(due_date),date(pay_date)) as before_due_days, 
        paid
    FROM `syncinvoice` 
    where frenns_id = 'FRN100000350' and 
		due_date < NOW() and
		DATEDIFF(date(NOW()), date(issue_date)) <= 365
    order by issue_date desc;
