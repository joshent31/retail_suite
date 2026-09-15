# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

"""Single daily scheduler entry dispatching to each sector's job."""


def daily():
	from retail_suite.accessories_management.daily import run as accessories_daily
	from retail_suite.apparel_management.daily import run as apparel_daily
	from retail_suite.fmcg_management.expiry import run as fmcg_daily
	from retail_suite.footwear_management.daily import run as footwear_daily
	from retail_suite.home_makeover_management.daily import run as makeover_daily
	from retail_suite.lifestyle_fashion_management.loyalty_expiry import (
		run as lifestyle_daily,
	)

	for fn in (
		apparel_daily,
		footwear_daily,
		accessories_daily,
		makeover_daily,
		lifestyle_daily,
		fmcg_daily,
	):
		fn()
