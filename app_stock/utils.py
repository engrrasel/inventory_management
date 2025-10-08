from app_stock.models import Stock, StockHistory

def update_stock(product, quantity, change_type, reference=None, remarks=None):
    stock, created = Stock.objects.get_or_create(product=product)
    previous_quantity = stock.quantity

    if change_type == "IN":
        stock.quantity += quantity
    elif change_type == "OUT":
        stock.quantity -= quantity
    elif change_type == "ADJ":
        stock.quantity = quantity

    stock.save()

    StockHistory.objects.create(
        product=product,
        change_type=change_type,
        quantity=quantity,
        previous_quantity=previous_quantity,
        new_quantity=stock.quantity,
        reference=reference,
        remarks=remarks
    )

    return stock.quantity
