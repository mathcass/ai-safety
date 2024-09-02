#!/usr/bin/env python3


get_stock_price = {
    "name": "get_stock_price",
    "description": "Retrieves the current stock price for a given company",
    "input_schema": {
        "type": "object",
        "properties": {
            "company": {
                "type": "string",
                "description": "The company name to fetch stock data for",
            }
        },
        "required": ["company"],
    },
}

send_email = {
    "name": "send_email",
    "description": "Sends an email to the specified recipient with the given subject and body.",
    "input_schema": {
        "type": "object",
        "properties": {
            "to": {
                "type": "string",
                "description": "The email address of the recipient",
            },
            "subject": {
                "type": "string",
                "description": "The subject line of the email",
            },
            "body": {
                "type": "string",
                "description": "The content of the email message",
            },
        },
        "required": ["to", "body"],
    },
}
