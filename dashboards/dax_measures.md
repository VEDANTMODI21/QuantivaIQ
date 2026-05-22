# QuantivaIQ — DAX Measures Reference

Use these highly-optimized DAX measures in your Power BI Dashboard to recreate the QuantivaIQ intelligence layer.

## Revenue & Sales Measures

1. **Total Revenue**
```dax
Total Revenue = SUM(orders[total_amount])
```

2. **Previous Month Revenue**
```dax
PM Revenue = CALCULATE([Total Revenue], PREVIOUSMONTH('Date'[Date]))
```

3. **MoM Revenue Growth %**
```dax
MoM Growth % = DIVIDE([Total Revenue] - [PM Revenue], [PM Revenue], 0)
```

4. **Average Order Value (AOV)**
```dax
AOV = DIVIDE([Total Revenue], DISTINCTCOUNT(orders[order_id]))
```

5. **Gross Profit**
```dax
Gross Profit = SUMX(order_items, order_items[quantity] * (order_items[unit_price] - RELATED(products[cost_price])))
```

6. **Profit Margin %**
```dax
Profit Margin % = DIVIDE([Gross Profit], [Total Revenue], 0)
```

7. **YTD Revenue**
```dax
YTD Revenue = TOTALYTD([Total Revenue], 'Date'[Date])
```

8. **Total Discount Given**
```dax
Total Discount = SUM(order_items[discount])
```

## Customer & Retention Measures

9. **Total Customers**
```dax
Total Customers = DISTINCTCOUNT(customers[customer_id])
```

10. **Active Customers (Last 30 Days)**
```dax
Active Customers 30D = CALCULATE(DISTINCTCOUNT(orders[customer_id]), orders[order_date] >= TODAY() - 30)
```

11. **New Customers**
```dax
New Customers = CALCULATE(DISTINCTCOUNT(customers[customer_id]), customers[registration_date] >= DATEADD(LASTDATE('Date'[Date]), -1, MONTH))
```

12. **Customer Retention Rate %**
```dax
Retention Rate % = DIVIDE([Active Customers 30D], [Total Customers], 0)
```

13. **Customer Churn Rate %**
```dax
Churn Rate % = 1 - [Retention Rate %]
```

14. **Repeat Purchase Rate**
```dax
Repeat Purchase Rate = 
VAR CustomersWithMultipleOrders = FILTER(VALUES(orders[customer_id]), CALCULATE(COUNT(orders[order_id])) > 1)
RETURN DIVIDE(COUNTROWS(CustomersWithMultipleOrders), [Total Customers])
```

15. **Average Customer Lifetime Value (CLTV)**
```dax
Avg CLTV = DIVIDE([Total Revenue], [Total Customers])
```

## Fraud & Risk Measures

16. **Total Fraud Transactions**
```dax
Total Fraud Txns = COUNTROWS(fraud_logs)
```

17. **Fraud Rate %**
```dax
Fraud Rate % = DIVIDE([Total Fraud Txns], COUNTROWS(orders), 0)
```

18. **Value at Risk (Blocked Revenue)**
```dax
Value at Risk = CALCULATE(SUM(orders[total_amount]), USERELATIONSHIP(orders[order_id], fraud_logs[order_id]))
```

19. **High Risk Customers Count**
```dax
High Risk Customers = CALCULATE(DISTINCTCOUNT(fraud_logs[customer_id]), fraud_logs[risk_score] >= 80)
```

20. **Average Fraud Risk Score**
```dax
Avg Risk Score = AVERAGE(fraud_logs[risk_score])
```

21. **Total Refund Amount**
```dax
Total Refunds = SUM(refunds[refund_amount])
```

22. **Refund Rate %**
```dax
Refund Rate % = DIVIDE([Total Refunds], [Total Revenue], 0)
```

## Inventory & Product Measures

23. **Total Units Sold**
```dax
Total Units Sold = SUM(order_items[quantity])
```

24. **Total Inventory Value**
```dax
Total Inventory Value = SUMX(products, products[stock_quantity] * products[cost_price])
```

25. **Out of Stock Items**
```dax
Out of Stock Items = CALCULATE(COUNTROWS(products), products[stock_quantity] <= 0)
```

26. **Low Stock Items (Below Reorder Level)**
```dax
Low Stock Items = CALCULATE(COUNTROWS(products), products[stock_quantity] <= products[reorder_level])
```

27. **Inventory Turnover Ratio**
```dax
Inventory Turnover = DIVIDE(SUM(order_items[quantity]), AVERAGE(products[stock_quantity]), 0)
```

28. **Top Selling Product Revenue**
```dax
Top Product Revenue = MAXX(VALUES(products[product_name]), [Total Revenue])
```

## Formatting & UI Helpers (DAX)

29. **MoM Color Indicator**
```dax
MoM Color = IF([MoM Growth %] > 0, "Green", "Red")
```

30. **Risk Score Color (Heatmap)**
```dax
Risk Color = 
SWITCH(
    TRUE(),
    [Avg Risk Score] >= 80, "#FF0000", -- Red
    [Avg Risk Score] >= 50, "#FFA500", -- Orange
    "#00FF00" -- Green
)
```

31. **Dynamic Dashboard Title**
```dax
Dashboard Title = "QuantivaIQ Analytics - " & FORMAT(TODAY(), "MMMM YYYY")
```
