        a_year_ago = datetime.datetime.now() - datetime.timedelta(days=3665)
        sql_query = " SELECT * " \
                    " FROM company_data" \
                    " WHERE `Accounts.LastMadeUpDate` >= {} and company_data.CompanyNumber = '{}' "\
                    " LIMIT {}".format(a_year_ago.strftime('%d/%m/%Y'), company_number, config.DATA_FETCH_LIMIT)
        logger.debug("QUERY: " + sql_query)

        cursor.execute(sql_query)
        company_row = cursor.fetchone()

        response = list()
        live_status = get_company_live_status(company_number)
        logger.debug("Live Status: " + live_status)
        company_row['CompanyStatus'] = live_status

        if len(company_row) == 0:
            return null

        report_rows = list()
        try:
            cursor.execute(
                "SELECT * FROM company_ann_reports "
                "WHERE company_ann_reports.CompanyNumber = %s", (company_number,))
            report_rows = cursor.fetchall()
        except Exception as e:
            logger.debug(e)

        try:
            cursor.execute(
                "SELECT * FROM financial_analysis "
                "WHERE financial_analysis.CompanyNumber = %s", (company_number,))
            analysis_row = cursor.fetchone()
        except Exception as e:
            logger.debug(e)
        try:
            yresponse =  requests.get("https://api.companieshouse.gov.uk/company"+"/"+company_number+"/officers",  auth=('ybR9_pjwYjYZsCdKN4lV6qXkPvxejCkq712lenhG', ''))
            yresponse.raise_for_status()
            yjson_response = yresponse.json()
            director=yjson_response['items'][0]
        except Exception as e:
            logger.debug(e)

        company = {'reports': report_rows, 'analysys': analysis_row, 'directors': director}
        
        company.update(company_row)

        response.append(company)
        return jsonify(response)