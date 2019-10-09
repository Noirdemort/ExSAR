Taks a JSON-file with right biased tree structure and parses it to produce a final decision.

```
{
    "condition": "AND",
    "rules": [
        {
        "id": "price",
        "field": "price",
        "type": "double",
        "input": "number",
        "operator": "less",
        "value": 10.25
        },
        {
            "id": "in_stock",
            "field": "in_stock",
            "type": "integer",
            "input": "radio",
            "operator": "equal",
            "value": 1
        }
    ],
    "valid": true
    }

```