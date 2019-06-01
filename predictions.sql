
--
-- Table structure for table `syncfinancialanalysis`
--

CREATE TABLE `syncfinancialanalysis` (
  `id` int(11) NOT NULL,
  `syncsupplier_id` int(11) NOT NULL,
  `year_number` int(11) NOT NULL,
  `frenns_id` varchar(255) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_type` enum('customer','supplier') NOT NULL,
  `acc_type` enum('ACCREC','ACCPAY') NOT NULL,
  `expected_days` int(11) DEFAULT NULL,
  `average_payment_days` int(11) DEFAULT NULL,
  `creditscore` int(11) DEFAULT NULL,
  `creditlimit` int(11) DEFAULT NULL,
  `purchasescore` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `syncrevenueprediction`
--

CREATE TABLE `syncrevenueprediction` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `frenns_id` varchar(255) NOT NULL,
  `acc_type` enum('ACCREC','ACCPAY') NOT NULL,
  `year_number` int(11) NOT NULL,
  `month_number` int(11) NOT NULL,
  `predicted_expense` decimal(15,2) DEFAULT NULL,
  `actual_expense` decimal(15,2) DEFAULT NULL,
  `is_justified` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `syncfinancialanalysis`
--
ALTER TABLE `syncfinancialanalysis`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `syncsupplier_id_2` (`syncsupplier_id`,`year_number`,`frenns_id`,`acc_type`),
  ADD KEY `syncsupplier_id` (`syncsupplier_id`);

--
-- Indexes for table `syncrevenueprediction`
--
ALTER TABLE `syncrevenueprediction`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `expense_prediction` (`frenns_id`,`acc_type`,`year_number`,`month_number`) USING BTREE,
  ADD KEY `frenns_id` (`frenns_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `syncfinancialanalysis`
--
ALTER TABLE `syncfinancialanalysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `syncrevenueprediction`
--
ALTER TABLE `syncrevenueprediction`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `syncfinancialanalysis`
--
ALTER TABLE `syncfinancialanalysis`
  ADD CONSTRAINT `payday_supplier` FOREIGN KEY (`syncsupplier_id`) REFERENCES `syncsupplier` (`syncsupplier_id`);
