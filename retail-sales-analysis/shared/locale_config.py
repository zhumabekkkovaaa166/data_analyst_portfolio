"""Locale-specific data and labels for English and Russian."""

LOCALES = {
    "en": {
        "categories": [
            "Beverages", "Condiments", "Confections", "Dairy",
            "Grains", "Meat", "Produce", "Seafood",
        ],
        "supplier_fmt": "Supplier {}",
        "product_fmt": "Product {:02d}",
        "customer_fmt": "Customer {:02d}",
        "employees": [
            (1, "Anna", "Petrova"),
            (2, "Bolat", "Kim"),
            (3, "Chen", "Wei"),
            (4, "Dana", "Sultan"),
            (5, "Erik", "Nurlan"),
        ],
        "chart_monthly_trend": {
            "title": "Monthly Revenue Trend (2023) \u2014 seasonality peaks toward year-end",
            "xlabel": "Month",
            "ylabel": "Revenue",
        },
        "chart_category_revenue": {
            "title": "Category Revenue \u2014 blue = above average (the 'significant' set)",
            "ylabel": "Revenue",
            "avg_label": "average = {avg:,.0f}",
        },
        "chart_clv_segments": {
            "title": "Customer Segments by quantile (top 20% = High, not a round number)",
            "ylabel": "Number of customers",
        },
        "db_ready": "demo database ready",
        "charts_written": "Charts written:",
    },
    "ru": {
        "categories": [
            "\u041d\u0430\u043f\u0438\u0442\u043a\u0438", "\u041f\u0440\u0438\u043f\u0440\u0430\u0432\u044b", "\u041a\u043e\u043d\u0434\u0438\u0442\u0435\u0440\u0441\u043a\u0438\u0435", "\u041c\u043e\u043b\u043e\u0447\u043d\u044b\u0435",
            "\u041a\u0440\u0443\u043f\u044b", "\u041c\u044f\u0441\u043e", "\u041e\u0432\u043e\u0449\u0438", "\u041c\u043e\u0440\u0435\u043f\u0440\u043e\u0434\u0443\u043a\u0442\u044b",
        ],
        "supplier_fmt": "\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a {}",
        "product_fmt": "\u0422\u043e\u0432\u0430\u0440 {:02d}",
        "customer_fmt": "\u041a\u043b\u0438\u0435\u043d\u0442 {:02d}",
        "employees": [
            (1, "\u0410\u043d\u043d\u0430", "\u041f\u0435\u0442\u0440\u043e\u0432\u0430"),
            (2, "\u0411\u043e\u043b\u0430\u0442", "\u041a\u0438\u043c"),
            (3, "\u0427\u044d\u043d\u044c", "\u0412\u044d\u0439"),
            (4, "\u0414\u0430\u043d\u0430", "\u0421\u0443\u043b\u0442\u0430\u043d"),
            (5, "\u042d\u0440\u0438\u043a", "\u041d\u0443\u0440\u043b\u0430\u043d"),
        ],
        "chart_monthly_trend": {
            "title": "\u041c\u0435\u0441\u044f\u0447\u043d\u044b\u0439 \u0442\u0440\u0435\u043d\u0434 \u0432\u044b\u0440\u0443\u0447\u043a\u0438 (2023) \u2014 \u043f\u0438\u043a \u0441\u0435\u0437\u043e\u043d\u043d\u043e\u0441\u0442\u0438 \u043a \u043a\u043e\u043d\u0446\u0443 \u0433\u043e\u0434\u0430",
            "xlabel": "\u041c\u0435\u0441\u044f\u0446",
            "ylabel": "\u0412\u044b\u0440\u0443\u0447\u043a\u0430",
        },
        "chart_category_revenue": {
            "title": "\u0412\u044b\u0440\u0443\u0447\u043a\u0430 \u043f\u043e \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f\u043c \u2014 \u0441\u0438\u043d\u0438\u0435 \u0432\u044b\u0448\u0435 \u0441\u0440\u0435\u0434\u043d\u0435\u0433\u043e (\u00ab\u0437\u043d\u0430\u0447\u0438\u043c\u043e\u0435 \u043c\u043d\u043e\u0436\u0435\u0441\u0442\u0432\u043e\u00bb)",
            "ylabel": "\u0412\u044b\u0440\u0443\u0447\u043a\u0430",
            "avg_label": "\u0441\u0440\u0435\u0434\u043d\u0435\u0435 = {avg:,.0f}",
        },
        "chart_clv_segments": {
            "title": "\u0421\u0435\u0433\u043c\u0435\u043d\u0442\u044b \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432 \u043f\u043e \u043a\u0432\u0430\u043d\u0442\u0438\u043b\u044f\u043c (\u0442\u043e\u043f-20% = High, \u043d\u0435 \u043a\u0440\u0443\u0433\u043b\u043e\u0435 \u0447\u0438\u0441\u043b\u043e)",
            "ylabel": "\u0427\u0438\u0441\u043b\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432",
        },
        "db_ready": "\u0434\u0435\u043c\u043e-\u0431\u0430\u0437\u0430 \u0433\u043e\u0442\u043e\u0432\u0430",
        "charts_written": "\u0413\u0440\u0430\u0444\u0438\u043a\u0438 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u044b:",
    },
}
