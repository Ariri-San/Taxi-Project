def add_text_sql(text, data):
    check_1 = True
    for objects in data:
        if check_1:
            check_1 = False
        else:
            text += ","
        
        text += "("
        
        check_2 = True
        for object in objects:
            if check_2:
                check_2 = False
            else:
                text += ","
            text += f'"{str(object)}"'
        
        text += ")"
    
    text += ";"
    
    return text


price_mile = [
    [1, "standard", 1]
]

price_day = [
    [1, 3, "23:00:00", "07:00:00"],
    [2, 3, "00:00:00", "00:00:00"],
    [3, 2.5, "07:00:00", "23:00:00"],
]

joined_price = [
    [1, "S", 2, 1],
    [2, "O", 1, 1],
    [3, "O", 3, 1],
]


price_mile_text = add_text_sql("INSERT INTO taxi_pricemile (id, name, is_active) VALUES ", price_mile) 
price_day_text =add_text_sql("INSERT INTO taxi_priceday (id, price, start, finish) VALUES ", price_day) 
joined_price_text = add_text_sql("INSERT INTO taxi_joinedprice (id, day_of_week, priceday_id, pricemile_id) VALUES ", joined_price)


# print(price_mile_text)
# print(price_day_text)
# print(joined_price_text)
